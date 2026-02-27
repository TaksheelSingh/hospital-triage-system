import os
import joblib
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACT_PATH = os.path.join(BASE_DIR, "artifacts_final")

model = joblib.load(os.path.join(ARTIFACT_PATH, "xgb_binary_model.pkl"))
scaler = joblib.load(os.path.join(ARTIFACT_PATH, "scaler.pkl"))
tfidf = joblib.load(os.path.join(ARTIFACT_PATH, "tfidf.pkl"))
numeric_features = joblib.load(os.path.join(ARTIFACT_PATH, "numeric_features.pkl"))


def compute_derived(data):
    shock_index = data["pulse"] / (data["systolic_bp"] + 1)
    bp_diff = data["systolic_bp"] - data["diastolic_bp"]

    instability_score = 0
    if data["temperature"] > 101: instability_score += 1
    if data["temperature"] < 95: instability_score += 1
    if data["systolic_bp"] < 90: instability_score += 1
    if data["pulse"] > 120: instability_score += 1
    if data["respiration"] > 24: instability_score += 1

    age_shock = data["age"] * shock_index

    return shock_index, bp_diff, instability_score, age_shock


def predict(data):

    shock_index, bp_diff, instability_score, age_shock = compute_derived(data)

    numeric_input = [
        data["age"],
        data["temperature"],
        data["pulse"],
        data["respiration"],
        data["systolic_bp"],
        data["diastolic_bp"],
        data["pain_scale"],
        data["rfv1"] or 0,
        data["rfv2"] or 0,
        data["rfv3"] or 0,
        1 if data["arrival_mode"] == "Ambulance" else 0,
        1 if data["ambtransfer"] else 0,
        shock_index,
        bp_diff,
        instability_score,
        age_shock
    ]

    numeric_scaled = scaler.transform([numeric_input])
    text_vector = tfidf.transform([data["rfv_text"] or ""])

    final_input = np.hstack((numeric_scaled, text_vector.toarray()))

    probability = float(model.predict_proba(final_input)[0][1])

    classification = "Critical" if probability >= 0.5 else "Needs Review"

    return probability, classification