import pandas as pd
import numpy as np
import os
import joblib
from scipy.sparse import hstack
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from xgboost import XGBClassifier

print("🚀 FINAL PRODUCTION BINARY TRIAGE MODEL")

DATA_PATH = r"C:\Users\Taksheel Rawat\Downloads\mp\3_labels\dataset_cleaned_final_binary.csv"
df = pd.read_csv(DATA_PATH)

# ---------------- TARGET ----------------
df["CRITICAL_FLAG"] = df["IMMEDR"].apply(lambda x: 1 if x in [1, 2] else 0)
y = df["CRITICAL_FLAG"]

# ---------------- DERIVED FEATURES ----------------
df["Shock_Index"] = df["PULSE"] / (df["BPSYS"] + 1)
df["BP_DIFF"] = df["BPSYS"] - df["BPDIAS"]

df["Temp_High"] = (df["TEMPF"] > 100.4).astype(int)
df["Temp_Low"] = (df["TEMPF"] < 95).astype(int)
df["BP_Low"] = (df["BPSYS"] < 90).astype(int)
df["BP_High"] = ((df["BPSYS"] >= 180) | (df["BPDIAS"] >= 120)).astype(int)
df["Resp_Abnormal"] = ((df["RESPR"] < 12) | (df["RESPR"] > 24)).astype(int)
df["Pulse_Abnormal"] = ((df["PULSE"] < 50) | (df["PULSE"] > 120)).astype(int)

df["Instability_Score"] = (
    df["Temp_High"] +
    df["Temp_Low"] +
    df["BP_Low"] +
    df["BP_High"] +
    df["Resp_Abnormal"] +
    df["Pulse_Abnormal"]
)

df["Is_Child"] = (df["AGE"] < 18).astype(int)
df["Is_Elderly"] = (df["AGE"] >= 65).astype(int)
df["High_Pain"] = (df["PAINSCALE"] >= 7).astype(int)

df["Extreme_Phys"] = (
    (df["BPSYS"] < 80) |
    (df["PULSE"] > 150) |
    (df["RESPR"] > 35)
).astype(int)

# ---------------- NUMERIC FEATURES (LOCKED ORDER) ----------------
numeric_features = [
    "Is_Child",
    "Is_Elderly",
    "SEX",

    "TEMPF",
    "PULSE",
    "RESPR",
    "BPSYS",
    "BPDIAS",
    "PAINSCALE",

    "Shock_Index",
    "BP_DIFF",

    "Temp_High",
    "Temp_Low",
    "BP_Low",
    "BP_High",
    "Resp_Abnormal",
    "Pulse_Abnormal",

    "Instability_Score",
    "High_Pain",
    "Extreme_Phys",

    "ARREMS",
    "AMBTRANSFER",
    "INJURY",

    "RFV1",
    "RFV2",
    "RFV3"
]

X_num = df[numeric_features].fillna(0)

scaler = StandardScaler()
X_num_scaled = scaler.fit_transform(X_num)

# ---------------- TEXT FEATURES ----------------
tfidf = TfidfVectorizer(
    max_features=6000,
    ngram_range=(1, 2),
    token_pattern=r'(?u)\b[a-zA-Z][a-zA-Z]+\b'
)

X_text = tfidf.fit_transform(df["RFV_TEXT_ALL"].fillna("").astype(str))

# LOCK ORDER: TEXT FIRST
X = hstack([X_text, X_num_scaled]).toarray()

# ---------------- TRAIN / TEST ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Stronger boost for Critical recall
sample_weights = np.where(y_train == 1, 3.0, 1.0)

model = XGBClassifier(
    objective="binary:logistic",
    n_estimators=1000,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.9,
    colsample_bytree=0.9,
    reg_lambda=2,
    reg_alpha=1,
    random_state=42,
    tree_method="hist",
    eval_metric="logloss"
)

model.fit(X_train, y_train, sample_weight=sample_weights)

# ---------------- EVALUATION ----------------
y_prob = model.predict_proba(X_test)[:, 1]

for threshold in [0.5, 0.4, 0.3]:
    print(f"\nThreshold = {threshold}")
    y_pred = (y_prob >= threshold).astype(int)
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

print("\nROC AUC:", roc_auc_score(y_test, y_prob))

# ---------------- SAVE ARTIFACTS ----------------
art = r"C:\Users\Taksheel Rawat\Downloads\mp\artifacts_binary_final_v2"
os.makedirs(art, exist_ok=True)

joblib.dump(model, os.path.join(art, "xgb_binary_model.pkl"))
joblib.dump(tfidf, os.path.join(art, "tfidf.pkl"))
joblib.dump(scaler, os.path.join(art, "scaler.pkl"))
joblib.dump(numeric_features, os.path.join(art, "numeric_features.pkl"))

print("\nModel saved successfully.")