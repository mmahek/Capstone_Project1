import pandas as pd
<<<<<<< HEAD
from sklearn.ensemble import RandomForestClassifier
import os

# ---------------------------
# LOAD DATA
# ---------------------------
BASE_DIR = os.path.dirname(__file__)
dataset_path = os.path.join(BASE_DIR, "dataset.csv")

df = pd.read_csv(dataset_path)

# Dynamic features
X = df.drop("disease", axis=1)
y = df["disease"]

# ---------------------------
# TRAIN MODEL
# ---------------------------
model = RandomForestClassifier(
    n_estimators=150,
    max_depth=12,
    class_weight="balanced",
    random_state=42
)

model.fit(X, y)

# ---------------------------
# ML PREDICTION
# ---------------------------
def predict_disease(symptoms):
    input_df = pd.DataFrame([symptoms], columns=X.columns)
    return model.predict(input_df)[0]

# ---------------------------
# ML CONFIDENCE
# ---------------------------
def predict_with_confidence(symptoms):
    input_df = pd.DataFrame([symptoms], columns=X.columns)
    probs = model.predict_proba(input_df)[0]

    max_prob = max(probs)
    pred = model.classes_[probs.argmax()]

    return pred, max_prob

# ---------------------------
# ML VALIDATION (LOG ONLY)
# ---------------------------
def log_ml_validation(query: str, rag_disease: str):
    try:
        q_lower = query.lower()
        symptoms = [0] * len(X.columns)

        for i, col in enumerate(X.columns):
            if col.replace("_", " ") in q_lower:
                symptoms[i] = 1

        ml_disease, confidence = predict_with_confidence(symptoms)

        if confidence < 0.4:
            print("ML not confident → ignoring")
            return

        if ml_disease.lower() == rag_disease.lower():
            print(f"ML agrees → {ml_disease} ({confidence:.2f})")
        else:
            print(f"ML mismatch → RAG: {rag_disease}, ML: {ml_disease} ({confidence:.2f})")

    except Exception as e:
        print("ML validation error:", e)
=======
from sklearn.tree import DecisionTreeClassifier
import os
import json

# Get file paths
BASE_DIR = os.path.dirname(__file__)
dataset_path = os.path.join(BASE_DIR, "dataset.csv")

# Load dataset
df = pd.read_csv(dataset_path)

X = df.drop("disease", axis=1)
X.columns = ['fever','cough','headache','fatigue','nausea','joint_pain','thirst','frequent_urination']
y = df["disease"]

# Train model once
model = DecisionTreeClassifier()
model.fit(X, y)

# Prediction function
def predict_disease(symptoms):
    return model.predict([symptoms])[0]

def get_disease_info(disease):
    with open(os.path.join(BASE_DIR, "knowledge.json"), 'r') as f:
        knowledge = json.load(f)
    return knowledge.get(disease, {"name": disease, "description": "No info available"})
>>>>>>> 9e596f7b11a33f607ee0c1ee5bb61b3661a45d9f
