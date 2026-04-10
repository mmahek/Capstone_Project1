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

import json


# ---------------------------
# CHAT API
# ---------------------------
class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all().order_by('-timestamp')
    serializer_class = ChatMessageSerializer

    def create(self, request, *args, **kwargs):
        user_text = request.data.get('text')

        # Save user's message
        user_msg = ChatMessage.objects.create(
            user=request.user if request.user.is_authenticated else None,
            sender='user',
            text=user_text
        )

        # Dummy bot response
        bot_text = "Thank you! I am analyzing your symptoms..."

        bot_msg = ChatMessage.objects.create(
            user=request.user if request.user.is_authenticated else None,
            sender='bot',
            text=bot_text
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

        # DELETE
        if "delete_id" in request.POST:
            HealthRecord.objects.filter(id=request.POST["delete_id"], user=request.user).delete()
            return redirect("health-records")

        # UPLOAD
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


@csrf_exempt
@login_required
def chat_api(request):
    if not request.session.session_key:
        request.session.save()
    step = request.session.get('chat_step', 0)
    known_symptoms = request.session.get('symptoms', [])
    
    if request.method == 'POST':
        data = json.loads(request.body)
        user_text = data.get('text', '').strip()
        
        user_msg = ChatMessage.objects.create(
            user=request.user,
            sender='user',
            text=user_text
        )
        
        symptom_keywords = ['fever', 'cough', 'headache', 'fatigue', 'nausea', 'joint pain', 'thirst', 'urination']
        
        if step == 0:
            bot_text = "Hi! I'm Dr. HealthBot your friendly health assistant 😊. Tell me what symptoms you're experiencing today? (fever, cough, headache, fatigue, nausea, joint pain, thirst, frequent urination)"
            step = 1
        else:
            user_lower = user_text.lower()
            found_new = []
            for kw in symptom_keywords:
                if kw in user_lower and kw not in known_symptoms:
                    found_new.append(kw)
            
            if found_new:
                known_symptoms.extend(found_new)
                bot_text = f"Sorry to hear about {', '.join(found_new)}. "
                if len(known_symptoms) > 1:
                    bot_text += "Any other symptoms? Type 'analyze' or 'predict' when ready for diagnosis."
                else:
                    bot_text += "Do you have any other symptoms? Type 'analyze' when ready."
            elif 'analyze' in user_lower or 'predict' in user_lower or 'done' in user_lower:
                # Predict
                symptoms_map = {'fever': 0, 'cough': 1, 'headache': 2, 'fatigue': 3, 'nausea': 4, 'joint pain': 5, 'thirst': 6, 'urination': 7}
                symptoms_vec = [0] * 8
                for sym in known_symptoms:
                    for k, i in symptoms_map.items():
                        if k in sym.lower():
                            symptoms_vec[i] = 1
                            break
                from .ml.model import predict_disease, get_disease_info
                disease = predict_disease(symptoms_vec)
                info = get_disease_info(disease)
                bot_text = f"🔬 **Diagnosis Analysis**\n\\nPossible Disease: **{disease}**\\n\\n📝 {info.get('description', 'No details')}\\n\\n💊 **Precautions:** {', '.join(info.get('precautions', ['Rest and consult doctor']))}\\n\\n🚨 **Seek immediate help if:** {info.get('when_to_see_doctor', 'Symptoms worsen')}\\n\\n⚠️ *AI prediction only - see a real doctor!*\\n\\nNew symptoms? Just start typing.\\n"
                known_symptoms = []
                step = 0
            else:
                bot_text = "Understood. Please share your symptoms (e.g. 'I have fever and cough') or type 'analyze' for prediction."
        
        request.session['chat_step'] = step
        request.session['symptoms'] = known_symptoms
        
        bot_msg = ChatMessage.objects.create(
            user=request.user,
            sender='bot',
            text=bot_text.replace('\\\\n', '\\n')
        )
        
        return JsonResponse({
            'user_message': ChatMessageSerializer(user_msg).data,
            'bot_message': ChatMessageSerializer(bot_msg).data
        })
    return JsonResponse({'error': 'POST only'}, status=405)
