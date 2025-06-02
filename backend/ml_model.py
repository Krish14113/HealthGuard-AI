import pandas as pd
import numpy as np
import joblib
import re

# Load model, label encoder, and symptom list
model = joblib.load("trained_model_full.pkl")
le = joblib.load("label_encoder_full.pkl")
all_symptoms = joblib.load("symptom_features_full.pkl")  # List of ~172 symptoms

# Load description and precaution data
description_df = pd.read_csv("symptom_Description.csv")
precaution_df = pd.read_csv("symptom_precaution.csv")

# Normalize symptom list
all_symptoms_lower = [sym.lower().strip() for sym in all_symptoms]

# NLP Matching function
def extract_symptoms(user_input):
    input_text = user_input.lower()
    matched = []
    for symptom in all_symptoms_lower:
        if re.search(r'\b' + re.escape(symptom) + r'\b', input_text):
            matched.append(symptom)
    return matched

# Main prediction function
def predict_disease(symptom_text):
    print("🔹 Received symptoms from frontend:", symptom_text)

    matched = extract_symptoms(symptom_text)
    print("🔎 Matched symptoms:", matched)

    # Build binary vector of 172 symptoms
    input_vector = np.zeros(len(all_symptoms_lower))
    for symptom in matched:
        if symptom in all_symptoms_lower:
            index = all_symptoms_lower.index(symptom)
            input_vector[index] = 1

    input_vector_np = input_vector.reshape(1, -1)

    # Predict top 5 diseases
    probas = model.predict_proba(input_vector_np)[0]
    top_indices = np.argsort(probas)[::-1][:5]

    predictions = []
    for idx in top_indices:
        disease_name = le.inverse_transform([idx])[0]
        confidence = probas[idx]
        desc = description_df[description_df['Disease'].str.lower() == disease_name.lower()]['Description'].values
        precautions = precaution_df[precaution_df['Disease'].str.lower() == disease_name.lower()].iloc[:, 1:].values.flatten()

        predictions.append({
            "disease": disease_name,
            "confidence": float(confidence),
            "description": desc[0] if len(desc) > 0 else "No description available.",
            "precautions": [p for p in precautions if pd.notna(p)]
        })

    return predictions

# Test block
if __name__ == "__main__":
    test_input = "I have a headache, nausea and back pain"
    result = predict_disease(test_input)
    for i, p in enumerate(result, 1):
        print(f"\n#{i}: {p['disease']} ({p['confidence']*100:.1f}%)")
        print("Description:", p['description'])
        print("Precautions:", p['precautions'])
