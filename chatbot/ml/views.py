import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
<<<<<<< HEAD
from .rag import retriever
from .model import log_ml_validation

=======
from .model import predict_disease, get_disease_info
>>>>>>> 9e596f7b11a33f607ee0c1ee5bb61b3661a45d9f

@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
<<<<<<< HEAD
        query = data.get("text", "").strip()
        
        results = retriever.retrieve(query, k=3, threshold=0.5)
        
        if not results:
            response = "I'm not confident about this. Please consult a doctor.\n\n⚠️ This is not a medical diagnosis."
        else:
            top_meta, score = results[0]
            disease = top_meta['disease_name']
            summary = top_meta['summary']
            precautions = '; '.join(top_meta['precautions'])
            when_to_see = top_meta.get('when_to_see_doctor', 'symptoms persist or worsen.')
            
            log_ml_validation(disease, query)
            
            response = f"""Based on your symptoms, this may be related to {disease}.

{summary}

Precautions:
{precautions}

Consult a doctor if:
{when_to_see}

⚠️ This is not a medical diagnosis. Please consult a healthcare professional."""
        
        return JsonResponse({{"bot_message": response}})
    return JsonResponse({{"error": "POST only"}}, status=405)
=======
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
>>>>>>> 9e596f7b11a33f607ee0c1ee5bb61b3661a45d9f
