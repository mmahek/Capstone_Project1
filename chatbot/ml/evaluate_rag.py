from chatbot.ml.rag import retriever

# Test queries (realistic)
test_cases = [
    ("fever chills sweating headache", "Malaria"),
    ("itching rash dry skin redness", "Allergic Dermatitis (Eczema)"),
    ("cough fever sore throat runny nose", "Common Cold"),
    ("frequent urination thirst fatigue", "Diabetes"),
    ("chest pain shortness of breath sweating", "Heart Attack (Myocardial Infarction)")
]

top1_correct = 0
top3_correct = 0

for query, true_label in test_cases:
    results = retriever.retrieve(query, k=3)

    predictions = [r[0]["disease_name"] for r in results]

    print("\nQuery:", query)
    print("Predicted:", predictions)
    print("Actual:", true_label)

    if len(predictions) > 0 and predictions[0] == true_label:
        top1_correct += 1

    if true_label in predictions:
        top3_correct += 1

n = len(test_cases)

print("\nTop-1 Accuracy:", top1_correct / n)
print("Top-3 Accuracy:", top3_correct / n)