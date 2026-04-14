import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

import os

# ---------------------------
# LOAD DATASET
# ---------------------------
BASE_DIR = os.path.dirname(__file__)
dataset_path = os.path.join(BASE_DIR, "dataset.csv")

df = pd.read_csv(dataset_path)

X = df.drop("disease", axis=1)
y = df["disease"]

# ---------------------------
# TRAIN-TEST SPLIT
# ---------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=42,
    stratify=y   # ✅ VERY IMPORTANT
)

# ---------------------------
# TRAIN MODEL
# ---------------------------
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# ---------------------------
# PREDICT
# ---------------------------
y_pred = model.predict(X_test)

# ---------------------------
# METRICS
# ---------------------------
accuracy = accuracy_score(y_test, y_pred)

print("\n✅ Accuracy:", accuracy)

print("\n📊 Classification Report:\n")
print(classification_report(y_test, y_pred))

print("\n🔍 Confusion Matrix:\n")
print(confusion_matrix(y_test, y_pred))