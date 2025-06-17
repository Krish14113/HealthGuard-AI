🛡️ HealthGuard AI

HealthGuard AI is an offline, AI-powered early diagnosis system that allows users to enter symptoms in natural language (or via voice input) and receive the top predicted diseases with confidence scores. It provides detailed disease descriptions and precautionary measures, making healthcare more accessible.

💡 Features

- Natural language symptom input
- 🎤 Voice-to-text support
- 🔍 Top 5 disease predictions with confidence scores
- 📄 Detailed descriptions and precaution lists for each disease
- 🎯 NLP-based symptom extraction
- 🧠 Trained machine learning model (Random Forest)
- 🧪 Arduino integration ready for heart rate input
- Fully offline-capable deployment

---

🖥️ Tech Stack

- Frontend: HTML, TailwindCSS, JavaScript (Vanilla)
- Backend: Python (Flask)
- Machine Learning: scikit-learn (RandomForest)
- NLP: Custom + spaCy-based processing
- Data Storage: CSV datasets for diseases, symptoms, severity, and precautions
- Voice Input: Web Speech API

---

🚀 How to Run

1. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate on Unix
pip install -r requirements.txt
python app.py
```

2. Frontend Setup
Open the index.html file in the frontend/ folder in your browser.

📦 File Structure
```
HealthGuardAI/
├── backend/
│   ├── app.py
│   ├── ml_model.py
│   ├── train_model_with_severity.py
│   ├── trained_model_with_severity.pkl
│   ├── label_encoder.pkl
│   ├── dataset.csv
│   ├── Symptom-severity.csv
│   ├── symptom_Description.csv
│   └── symptom_precaution.csv
└── frontend/
    ├── index.html
    ├── style.css
    └── script.js
```

🔒 License
This project is developed under an academic setting and is patent-pending. Usage and reproduction without permission is restricted.

👨‍⚕️ Authors
Krish Jain
Rishika Singh Parihar
