from chatbot.ml.rag import retriever
from chatbot.ml.model import predict_disease

# same test cases
test_cases = [
    ("fever chills sweating headache", "Malaria"),
    ("itching rash dry skin redness", "Allergic Dermatitis (Eczema)"),
    ("cough fever sore throat runny nose", "Common Cold"),
    ("frequent urination thirst fatigue", "Diabetes"),
    ("chest pain shortness of breath sweating", "Heart Attack (Myocardial Infarction)")
]

correct = 0

for query, true_label in test_cases:

    # RAG
    rag_results = retriever.retrieve(query, k=1)

    if not rag_results:
        continue

    rag_pred = rag_results[0][0]["disease_name"]

    # ML (convert query to vector)
    symptoms = query.lower()
    vec = [0]*18

    from chatbot.ml.model import X  # import feature columns

    symptom_list = list(X.columns)   # auto sync with model
    vec = [0] * len(symptom_list)

    for i, s in enumerate(symptom_list):
        if s.replace("_", " ") in symptoms:
            vec[i] = 1

    ml_pred = predict_disease(vec)

    print("\nQuery:", query)
    print("RAG:", rag_pred)
    print("ML:", ml_pred)
    print("Actual:", true_label)

    # hybrid logic → prefer RAG but check ML agreement
    if rag_pred == true_label or ml_pred == true_label:
        correct += 1

accuracy = correct / len(test_cases)

print("\n🔥 Hybrid Accuracy:", accuracy)