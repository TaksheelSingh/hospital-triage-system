import joblib
import numpy as np
from scipy.sparse import hstack

model = joblib.load("artifacts_binary_final_v2/xgb_binary_model.pkl")
tfidf = joblib.load("artifacts_binary_final_v2/tfidf.pkl")
scaler = joblib.load("artifacts_binary_final_v2/scaler.pkl")
numeric_features = joblib.load("artifacts_binary_final_v2/numeric_features.pkl")

THRESHOLD = 0.30


def derive_features(data: dict):

    data["Shock_Index"] = data["PULSE"] / (data["BPSYS"] + 1)
    data["BP_DIFF"] = data["BPSYS"] - data["BPDIAS"]

    data["Temp_High"] = int(data["TEMPF"] > 100.4)
    data["Temp_Low"] = int(data["TEMPF"] < 95)
    data["BP_Low"] = int(data["BPSYS"] < 90)
    data["BP_High"] = int(data["BPSYS"] >= 180 or data["BPDIAS"] >= 120)
    data["Resp_Abnormal"] = int(data["RESPR"] < 12 or data["RESPR"] > 24)
    data["Pulse_Abnormal"] = int(data["PULSE"] < 50 or data["PULSE"] > 120)

    data["Instability_Score"] = (
        data["Temp_High"]
        + data["Temp_Low"]
        + data["BP_Low"]
        + data["BP_High"]
        + data["Resp_Abnormal"]
        + data["Pulse_Abnormal"]
    )

    data["Is_Child"] = int(data["AGE"] < 18)
    data["Is_Elderly"] = int(data["AGE"] >= 65)
    data["High_Pain"] = int(data["PAINSCALE"] >= 7)

    data["Extreme_Phys"] = int(
        data["BPSYS"] < 80
        or data["PULSE"] > 150
        or data["RESPR"] > 35
    )

    return data


def override_logic(data: dict):
    return (
        data["BPSYS"] < 80
        or data["PULSE"] > 150
        or data["RESPR"] > 35
        or data["Instability_Score"] >= 4
    )


def predict(data: dict):

    data = derive_features(data)

    if override_logic(data):
        return "Critical", 1.0, True

    numeric_input = np.array([[data[f] for f in numeric_features]])
    numeric_scaled = scaler.transform(numeric_input)

    text_input = tfidf.transform([data["RFV_TEXT_ALL"]])

    # IMPORTANT: match training dense format
    X = hstack([text_input, numeric_scaled]).toarray()

    prob = model.predict_proba(X)[0][1]
    label = "Critical" if prob >= THRESHOLD else "Needs Review"

    return label, float(prob), False