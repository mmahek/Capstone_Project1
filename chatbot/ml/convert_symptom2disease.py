import pandas as pd
import os

# ---------------------------
# PATHS
# ---------------------------
BASE_DIR = os.path.dirname(__file__)

input_path = os.path.join(BASE_DIR, "Symptom2Disease.csv")
output_path = os.path.join(BASE_DIR, "dataset.csv")

# ---------------------------
# LOAD DATA
# ---------------------------
df = pd.read_csv(input_path)

# ---------------------------
# HANDLE COLUMN NAMES SAFELY
# ---------------------------
print("Columns found:", df.columns)

# Try common column names
if "text" in df.columns:
    text_col = "text"
elif "symptoms" in df.columns:
    text_col = "symptoms"
else:
    text_col = df.columns[1]   # fallback

if "label" in df.columns:
    disease_col = "label"
elif "disease" in df.columns:
    disease_col = "disease"
else:
    disease_col = df.columns[-1]  # fallback

print("Using:", text_col, "->", disease_col)

# ---------------------------
# EXPANDED SYMPTOM LIST
# ---------------------------
symptom_list = [
    "fever","chills","fatigue","weakness","weight loss","weight gain","sweating",
    "headache","chest pain","abdominal pain","joint pain","body aches","back pain",
    "cough","shortness of breath","wheezing","sore throat","runny nose","congestion",
    "nausea","vomiting","diarrhea","constipation","bloating","loss of appetite",
    "rash","itching","redness","dry skin","swelling","blisters",
    "dizziness","confusion","loss of balance","tingling","numbness",
    "frequent urination","burning urination","thirst",
    "loss of taste","loss of smell","vision problems","palpitations"
]

# ---------------------------
# SYNONYMS (IMPORTANT)
# ---------------------------
symptom_synonyms = {
    "fever": ["fever", "high temperature", "temperature"],
    "cough": ["cough", "coughing"],
    "shortness of breath": ["breathless", "difficulty breathing"],
    "frequent urination": ["urinating often", "pee frequently"],
    "thirst": ["very thirsty", "excessive thirst"],
    "runny nose": ["runny nose", "nasal discharge"],
    "sore throat": ["sore throat", "throat pain"],
    "chest pain": ["chest pain", "chest pressure"],
    "dizziness": ["dizzy", "lightheaded"],
    "fatigue": ["tired", "fatigue", "exhausted"]
}

# ---------------------------
# CONVERT TEXT → FEATURES
# ---------------------------
rows = []

for _, row in df.iterrows():

    text = str(row[text_col]).lower()
    disease = row[disease_col]

    features = {sym: 0 for sym in symptom_list}

    for sym in symptom_list:

        # 1️⃣ Check synonyms first
        if sym in symptom_synonyms:
            if any(v in text for v in symptom_synonyms[sym]):
                features[sym] = 1
                continue

        # 2️⃣ Fallback: word matching
        words = sym.split()
        if any(word in text for word in words):
            features[sym] = 1

    features["disease"] = disease
    rows.append(features)

# ---------------------------
# SAVE DATASET
# ---------------------------
new_df = pd.DataFrame(rows)
new_df.to_csv(output_path, index=False)

print(f"✅ Converted dataset saved with {len(new_df)} rows")