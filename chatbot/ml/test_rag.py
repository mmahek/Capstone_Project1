import sys
sys.path.insert(0, '..')
from rag import retriever
from model import log_ml_validation

print("=== RAG + ML Test Suite === ")

tests = [
    ("fever chills headache", "Malaria or Dengue"),
    ("cough breathing issue", "Asthma"),
    ("burning urination", "UTI"),
    ("abc random", "Fallback")
]

for query, expected in tests:
    print(f"\n--- Query: '{query}' ---")
    results = retriever.retrieve(query, k=3, threshold=0.5)
    if results:
        disease = results[0][0]['disease_name']
        score = results[0][1]
        print(f"RAG: {disease} (score: {score:.3f}) - Expected ~{expected}")
        log_ml_validation(disease, query)
    else:
        print("Fallback (low confidence) - Correct for poor query")
    
print("\nTests complete - Check server logs for RAG/ML output!")

