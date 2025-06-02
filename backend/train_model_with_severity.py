import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv("dataset.csv")
df.fillna("", inplace=True)

# Normalize disease names
df["Disease"] = df["Disease"].str.strip().str.lower()

# Extract only symptom columns (skip 'Disease')
symptom_columns = df.columns[1:]

# Clean all symptom entries
for col in symptom_columns:
    df[col] = df[col].str.strip().str.lower()

# Build symptom index
all_symptoms_set = set()
for col in symptom_columns:
    all_symptoms_set.update(df[col].unique())

# Remove blank and misclassified entries
all_symptoms_set.discard("")
all_symptoms_set.discard("disease")
all_symptoms = sorted(all_symptoms_set)

# Map symptom -> index
symptom_index = {symptom: i for i, symptom in enumerate(all_symptoms)}

# Encode each row into binary vector
def encode_row(row):
    vector = np.zeros(len(all_symptoms))
    for symptom in row[symptom_columns]:
        if symptom in symptom_index:
            vector[symptom_index[symptom]] = 1
    return vector

X = np.array([encode_row(row) for _, row in df.iterrows()])

# Encode disease labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["Disease"])

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model and encoders
joblib.dump(model, "trained_model_full.pkl")
joblib.dump(label_encoder, "label_encoder_full.pkl")
joblib.dump(all_symptoms, "symptom_features_full.pkl")

print("✅ Full model trained and saved with", len(all_symptoms), "cleaned symptom features.")
