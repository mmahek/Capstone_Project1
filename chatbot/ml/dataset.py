import json
import pandas as pd
import random
import os

BASE_DIR = os.path.dirname(__file__)
json_path = os.path.join(BASE_DIR, "knowledge.json")

with open(json_path) as f:
    diseases = json.load(f)

# Master symptom list
all_symptoms = [
    # General
    "fever","chills","fatigue","weakness","weight loss","weight gain","sweating",

    # Pain
    "headache","chest pain","abdominal pain","joint pain","body aches","back pain",

    # Respiratory
    "cough","shortness of breath","wheezing","sore throat","runny nose","congestion",

    # Digestive
    "nausea","vomiting","diarrhea","constipation","bloating","loss of appetite",

    # Skin
    "rash","itching","redness","dry skin","swelling","blisters",

    # Neurological
    "dizziness","confusion","loss of balance","tingling","numbness",

    # Urinary / metabolic
    "frequent urination","burning urination","thirst",

    # Special
    "loss of taste","loss of smell","vision problems","palpitations"
]

rows = []

# 🔥 GENERATE MULTIPLE VARIATIONS
for disease in diseases:

    disease_name = disease["disease_name"]
    symptoms = [s.lower() for s in disease["symptoms"]]

    for _ in range(30):   # 👉 generate 30 samples per disease

        row = {sym: 0 for sym in all_symptoms}

        # Pick random subset of symptoms (simulate real patient)
        selected = random.sample(symptoms, k=min(len(symptoms), random.randint(2, 5)))

        for sym in selected:
            for master in all_symptoms:
                if master in sym:
                    row[master] = 1

        # Add small noise (real-world effect)
        if random.random() < 0.2:
            noise_symptom = random.choice(all_symptoms)
            row[noise_symptom] = 1

        row["disease"] = disease_name
        rows.append(row)

# Create dataframe
df = pd.DataFrame(rows)

# Save dataset
dataset_path = os.path.join(BASE_DIR, "dataset.csv")
df.to_csv(dataset_path, index=False)

print(f"✅ Generated dataset with {len(df)} rows")