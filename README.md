# 🩺 AI Public Health Assistant

*A Context-Aware, Bilingual Health Chatbot with Environmental Intelligence*

---

## 📌 Overview

AI Public Health Assistant is a **Django-based intelligent health chatbot** designed to provide **context-aware, safe, and non-diagnostic health guidance**.

Unlike traditional health bots, this system integrates:

* 🧠 Machine Learning (disease prediction)
* 🌍 Environmental risk analysis
* 📊 Symptom severity classification
* 🌐 Bilingual interaction (Hindi + English)
* 🔐 Privacy-first design

The system is inspired by our **patent proposal** focusing on **environment-aware public health intelligence**.

---

## 🚀 Key Features

### 🤖 Conversational AI Chatbot

* Multi-turn conversation using Django sessions
* Symptom collection via natural interaction
* Guided diagnosis flow (ask → collect → analyze → respond)

---

### 🧠 Machine Learning Prediction

* Model: **TF-IDF + Logistic Regression**
* Input: Natural language symptoms (e.g., "fever and headache")
* Output:

  * Predicted disease
  * Confidence score

---

### 🌍 Environmental Risk Intelligence

* Uses:

  * Temperature 🌡️
  * Humidity 💧
  * Air Quality Index (AQI) 🌫️
* Provides contextual risk like:

  * Respiratory risk
  * Heat/dehydration risk

---

### 📊 Symptom Severity Classification

* Rule-based severity levels:

  * 🟢 Low
  * 🟡 Moderate
  * 🔴 High
* Ensures **safe, non-diagnostic guidance**

---

### 🌐 Bilingual Support

* Supports:

  * English 🇬🇧
  * Hindi 🇮🇳
* Improves accessibility for wider audience

---

### 📡 Low Network Mode

* Provides **short and essential responses**
* Works in **low connectivity / rural environments**

---

### 🔐 Privacy-First Architecture

* No long-term storage of sensitive health data
* Session-based processing
* Designed for **user trust and safety**

---

### 📁 Health Records Management

* Upload and manage medical files
* User-specific secure storage

---

## 🏗️ Tech Stack

| Layer    | Technology                        |
| -------- | --------------------------------- |
| Backend  | Django 5.x, Django REST Framework |
| Database | SQLite                            |
| ML       | scikit-learn                      |
| NLP      | TF-IDF Vectorizer                 |
| Frontend | TailwindCSS, HTMX, JavaScript     |
| Others   | Web Speech API (voice input)      |

---

## 🧠 System Architecture

User Input
↓
Symptom Extraction
↓
ML Prediction (TF-IDF + Logistic Regression)
↓

* Environmental Risk Engine
  ↓
* Severity Classifier
  ↓
* Language Module
  ↓
  Final Response Generation

---

## 📂 Project Structure

```
healthbot/
│
├── chatbot/
│   ├── ml/
│   │   ├── model.py
│   │   ├── dataset.csv
│   │   └── knowledge.json
│   ├── views.py
│   ├── models.py
│   └── templates/
│
├── accounts/
├── reports/
├── alerts/
├── simulation/
│
├── static/
├── templates/
└── manage.py
```

---

## ⚙️ Installation & Setup

```bash
# Clone repository
git clone <your-repo-url>

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

---

## 💡 Usage

1. Login / Signup
2. Open Dashboard
3. Start Chat

Example:

```
User: I have fever and headache  
Bot: Any other symptoms?  
User: fatigue  
User: analyze  
```

Output includes:

* Disease prediction
* Severity level
* Environmental risk
* Precautions

---

## ⚠️ Disclaimer

This system **does NOT provide medical diagnosis**.
It is intended for **awareness and preliminary guidance only**.
Always consult a healthcare professional.

---

## 🧪 Future Enhancements

* 🔍 FAISS-based medical knowledge retrieval
* 📡 Real-time environmental API integration
* ⌚ Wearable device (IoT) integration
* 📊 Health analytics dashboard
* 🌐 Deployment (Render / AWS)

---

## 🏆 Innovation Highlights

* Context-aware health guidance using environmental data
* Privacy-first chatbot design
* Bilingual accessibility
* Safe severity-based recommendations
* Designed for both **urban and rural use cases**

---

## 👩‍💻 Contributors

* Mahek Yadav (and team)

---

## 📜 License

This project is for academic and research purposes.

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
