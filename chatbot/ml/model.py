import pandas as pd
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
