from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import spacy

app = Flask(__name__)
CORS(app)

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Load model and encoders
model = joblib.load("trained_model_full.pkl")
label_encoder = joblib.load("label_encoder_full.pkl")
all_symptoms = joblib.load("symptom_features_full.pkl")
symptom_index = {symptom: idx for idx, symptom in enumerate(all_symptoms)}

# Load symptom descriptions and precautions
description_df = pd.read_csv("symptom_Description.csv")
precaution_df = pd.read_csv("symptom_precaution.csv")

# Helper to extract keywords
nlp_symptom_set = set(all_symptoms)
def extract_keywords(text):
    doc = nlp(text.lower())
    return [token.lemma_ for token in doc if token.lemma_ in nlp_symptom_set]

@app.route("/", methods=["GET"])
def home():
    return "HealthGuard AI Backend is running."

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    input_text = data.get("symptoms", "")
    print("\U0001F539 Received symptoms from frontend:", input_text)

    # Extract and match
    keywords = extract_keywords(input_text)
    print("\U0001F9EA Extracted keywords:", keywords)

    matched_symptoms = [kw for kw in keywords if kw in symptom_index]
    print("\U0001F50E Matched symptoms:", matched_symptoms)

    if not matched_symptoms:
        return jsonify({
            "success": False,
            "message": "No recognizable symptoms found.",
            "predictions": []
        }), 200

    input_vector = np.zeros(len(all_symptoms))
    for symptom in matched_symptoms:
        input_vector[symptom_index[symptom]] = 1

    proba = model.predict_proba([input_vector])[0]
    top_indices = proba.argsort()[::-1][:3]

    predictions = []
    for idx in top_indices:
        disease = label_encoder.inverse_transform([idx])[0]
        confidence = round(float(proba[idx]), 2)

        desc_row = description_df[description_df['Disease'].str.lower() == disease.lower()]
        description = desc_row['Description'].values[0] if not desc_row.empty else "Description not available."

        precaution_row = precaution_df[precaution_df['Disease'].str.lower() == disease.lower()]
        precautions = precaution_row.iloc[0, 1:].dropna().tolist() if not precaution_row.empty else ["No precautions listed."]

        predictions.append({
            "disease": disease,
            "confidence": confidence,
            "description": description,
            "precautions": precautions
        })

    return jsonify({
        "success": True,
        "predictions": predictions
    }), 200

if __name__ == "__main__":

    app.run(debug=True)
