import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .rag import retriever
from .model import log_ml_validation


@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
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
