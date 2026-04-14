from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import ChatMessage, HealthRecord
from .serializers import ChatMessageSerializer
from .forms import HealthRecordForm
from .ml.rag import retriever
from .ml.model import log_ml_validation

import json


# ---------------------------
# SYMPTOM EXTRACTION
# ---------------------------
def extract_symptoms(user_text):
    text = user_text.lower()

    symptom_map = {
        "fever": "fever",
        "chills": "chills",
        "sweating": "sweating",
        "cough": "cough",
        "headache": "headache",
        "fatigue": "fatigue",
        "nausea": "nausea",
        "vomiting": "vomiting",
        "rash": "rash",
        "itching": "itching",
        "dizziness": "dizziness",
        "shortness of breath": "shortness of breath",
        "sore throat": "sore throat",
        "runny nose": "runny nose",
        "thirst": "thirst",
        "urination": "frequent urination",
        "frequent urination": "frequent urination"
    }

    found = []
    for key, value in symptom_map.items():
        if key in text:
            found.append(value)

    return list(set(found))


# ---------------------------
# CHAT VIEWSET
# ---------------------------
class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all().order_by('-timestamp')
    serializer_class = ChatMessageSerializer

    def create(self, request, *args, **kwargs):
        user_text = request.data.get('text')

        user_msg = ChatMessage.objects.create(
            user=request.user if request.user.is_authenticated else None,
            sender='user',
            text=user_text
        )

        bot_msg = ChatMessage.objects.create(
            user=request.user if request.user.is_authenticated else None,
            sender='bot',
            text="💙 I'm here for you. Let me understand your symptoms..."
        )

        return Response({
            "user_message": ChatMessageSerializer(user_msg).data,
            "bot_message": ChatMessageSerializer(bot_msg).data
        }, status=status.HTTP_201_CREATED)


# ---------------------------
# HEALTH RECORDS PAGE
# ---------------------------
@login_required
def health_records(request):
    if request.method == "POST":
        if "delete_id" in request.POST:
            HealthRecord.objects.filter(id=request.POST["delete_id"], user=request.user).delete()
            return redirect("health-records")

        form = HealthRecordForm(request.POST, request.FILES)
        if form.is_valid():
            rec = form.save(commit=False)
            rec.user = request.user
            rec.save()
            return redirect("health-records")
    else:
        form = HealthRecordForm()

    records = HealthRecord.objects.filter(user=request.user).order_by("-uploaded_at")

    return render(request, "chatbot/health_records.html", {
        "form": form,
        "records": records
    })


# ---------------------------
# STATIC PAGES
# ---------------------------
def chat_page(request):
    return render(request, "chatbot/chat.html")


def dashboard(request):
    return render(request, "chatbot/dashboard.html")


def alerts_page(request):
    return render(request, "chatbot/alerts.html")


def chat_history(request):
    return render(request, "chatbot/chat_history.html")


# ---------------------------
# SMART CHAT API
# ---------------------------
@csrf_exempt
@login_required
def chat_api(request):

    if request.method == 'POST':

        data = json.loads(request.body)
        user_text = data.get('text', '').strip()
        user_lower = user_text.lower()

        state = request.session.get("chat_state", "start")
        symptoms = request.session.get("symptoms", [])

        user_msg = ChatMessage.objects.create(
            user=request.user,
            sender='user',
            text=user_text
        )

        # ---------------------------
        # GREETING
        # ---------------------------
        if user_lower in ["hi", "hello", "hey"]:
            bot_text = "Hi 😊 I'm here to help you understand your health concerns. Could you tell me what symptoms you're experiencing?"
            request.session["chat_state"] = "collecting"
            request.session["symptoms"] = []

        # ---------------------------
        # FOLLOW-UP MODE
        # ---------------------------
        elif state == "followup":

            disease = request.session.get("last_disease", "this condition")

            if "treatment" in user_lower:
                bot_text = f"""
💙 I'm glad you asked.

For **{disease}**, here are some general care suggestions:

🩺 **Treatment & Care:**
• Get plenty of rest  
• Stay well hydrated  
• Take medications only if prescribed  
• Avoid self-medication  

⚠️ If symptoms do not improve, please consult a doctor.

I'm here if you'd like prevention or diet advice as well.
"""

            elif "prevent" in user_lower:
                bot_text = f"""
💙 Taking preventive steps is a great idea.

🛡️ **To reduce risk of {disease}:**
• Maintain good hygiene  
• Eat balanced, nutritious food  
• Stay physically active  
• Avoid exposure to infections  

Would you like to know if this condition can become serious?
"""

            elif "serious" in user_lower:
                bot_text = f"""
⚠️ It's important to stay aware.

For **{disease}**, please seek immediate medical help if you notice:

• Difficulty breathing  
• Persistent high fever  
• Severe pain  
• Sudden weakness  

💙 Early medical attention can prevent complications.

Would you like dietary guidance as well?
"""

            elif "diet" in user_lower:
                bot_text = f"🍎 Eat light, nutritious food and avoid oily or processed meals."

            else:
                bot_text = "💬 You can ask about treatment, prevention, seriousness, or diet. I'm here to help."

        else:
            found = extract_symptoms(user_text)

            if state == "collecting":

                if found:
                    symptoms.extend(found)
                    symptoms = list(set(symptoms))
                    request.session["symptoms"] = symptoms

                    bot_text = f"I've noted these symptoms: {', '.join(symptoms)}.\nWould you like me to analyze this?"

                    request.session["chat_state"] = "confirm"

                else:
                    bot_text = "Could you describe your symptoms like fever, cough, or pain?"

            
            
            
            
            elif state == "confirm":

                if user_lower in ["yes", "ok", "analyze", "sure"]:

                    # PRIORITIZE IMPORTANT SYMPTOMS
                    priority = ["fever", "chills", "sweating", "cough", "shortness of breath"]

                    filtered = sorted(symptoms, key=lambda x: 0 if x in priority else 1)

                    query = "symptoms: " + ", ".join(filtered[:4])
                    results = retriever.retrieve(query, k=3)

                    if not results:
                        bot_text = "I'm not fully confident yet. Could you share more symptoms?"
                    else:
                        top, score = results[0]
                        confidence = int(score * 100)

                        precautions = "\n• " + "\n• ".join(top["precautions"])

                        bot_text = f"""
💙 I understand your concern.

Based on your symptoms — {', '.join(symptoms)} — this may be related to {top['disease_name']}, but other conditions may also be possible.

🩺 {top['summary']}

🛡️ What you can do:
{precautions}

⚠️ When to consult a doctor:
{top['when_to_see_doctor']}

📊 Confidence: {confidence}%

💬 You can ask me about treatment, prevention, diet, or seriousness.

---

🚨 Important:
This is only a **suggestion based on symptoms**, not a medical diagnosis.

👉 Health conditions can vary and overlap.

👉 Please consult a qualified doctor for proper diagnosis and treatment.

Your health matters 💙
"""

                        try:
                            log_ml_validation(user_text, top["disease_name"])
                        except:
                            pass

                        request.session["chat_state"] = "followup"
                        request.session["last_disease"] = top["disease_name"]

                else:
                    bot_text = "Would you like me to analyze your symptoms?"

            else:
                bot_text = "Please tell me your symptoms so I can help you better 😊"

        bot_msg = ChatMessage.objects.create(
            user=request.user,
            sender='bot',
            text=bot_text
        )

        return JsonResponse({
            'user_message': ChatMessageSerializer(user_msg).data,
            'bot_message': ChatMessageSerializer(bot_msg).data
        })

    return JsonResponse({'error': 'POST only'}, status=405)