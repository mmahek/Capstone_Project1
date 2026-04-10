import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .model import predict_disease, get_disease_info

@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_text = data.get("text", "").lower()

        # 🔥 SIMPLE NLP (keyword-based)
        symptoms_map = {
            "fever": 0,
            "cough": 1,
            "headache": 2,
            "fatigue": 3,
            "nausea": 4,
            "joint pain": 5,
            "thirst": 6,
            "urination": 7
        }

        symptoms = [0]*8

        for word in symptoms_map:
            if word in user_text:
                symptoms[symptoms_map[word]] = 1

        # Predict disease
        disease = predict_disease(symptoms)

        # Get info
        info = get_disease_info(disease)

        response = f"""
Possible Disease: {disease}

Description: {info.get('description')}

Precautions: {", ".join(info.get('precautions', []))}

Advice: {info.get('when_to_see_doctor')}

⚠️ This is not a medical diagnosis. Please consult a doctor.
"""

        return JsonResponse({"bot_message": response})