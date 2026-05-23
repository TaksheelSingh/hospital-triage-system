import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt
from scipy.sparse import hstack
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

print("🚀 SHAP EXPLAINABILITY ANALYSIS")

# ============================================
# LOAD DATASET
# ============================================

DATA_PATH = r"C:\Users\Taksheel Rawat\Downloads\mp\3_labels\dataset_cleaned_final_binary.csv"

df = pd.read_csv(DATA_PATH)

# ============================================
# TARGET
# ============================================

df["CRITICAL_FLAG"] = df["IMMEDR"].apply(
    lambda x: 1 if x in [1, 2] else 0
)

y = df["CRITICAL_FLAG"]

# ============================================
# DERIVED FEATURES
# ============================================

df["Shock_Index"] = df["PULSE"] / (df["BPSYS"] + 1)
df["BP_DIFF"] = df["BPSYS"] - df["BPDIAS"]

df["Temp_High"] = (df["TEMPF"] > 100.4).astype(int)
df["Temp_Low"] = (df["TEMPF"] < 95).astype(int)

df["BP_Low"] = (df["BPSYS"] < 90).astype(int)

df["BP_High"] = (
    (df["BPSYS"] >= 180) |
    (df["BPDIAS"] >= 120)
).astype(int)

df["Resp_Abnormal"] = (
    (df["RESPR"] < 12) |
    (df["RESPR"] > 24)
).astype(int)

df["Pulse_Abnormal"] = (
    (df["PULSE"] < 50) |
    (df["PULSE"] > 120)
).astype(int)

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

# ============================================
# NUMERIC FEATURES
# ============================================

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

# ============================================
# SCALING
# ============================================

scaler = StandardScaler()

X_num_scaled = scaler.fit_transform(X_num)

# ============================================
# TF-IDF
# ============================================

tfidf = TfidfVectorizer(
    max_features=6000,
    ngram_range=(1, 2),
    token_pattern=r'(?u)\b[a-zA-Z][a-zA-Z]+\b'
)

X_text = tfidf.fit_transform(
    df["RFV_TEXT_ALL"].fillna("").astype(str)
)

# ============================================
# COMBINE FEATURES
# ============================================

X = hstack([X_text, X_num_scaled]).toarray()

# ============================================
# TRAIN TEST SPLIT
# ============================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# ============================================
# LOAD TRAINED MODEL
# ============================================

MODEL_PATH = r"C:\Users\Taksheel Rawat\Downloads\mp\artifacts_binary_final_v2\xgb_binary_model.pkl"

model = joblib.load(MODEL_PATH)

print("✅ Model loaded successfully")

# ============================================
# FEATURE NAMES
# ============================================

tfidf_feature_names = tfidf.get_feature_names_out()

all_feature_names = list(tfidf_feature_names) + numeric_features

# ============================================
# CREATE SHAP EXPLAINER
# ============================================

print("Creating SHAP explainer...")

explainer = shap.TreeExplainer(model)

# ============================================
# GENERATE SHAP VALUES
# ============================================

print("Generating SHAP values...")

shap_values = explainer.shap_values(X_test)

# ============================================
# SHAP SUMMARY PLOT
# ============================================

print("Displaying SHAP summary plot...")

shap.summary_plot(
    shap_values,
    X_test,
    feature_names=all_feature_names
)

# ============================================
# SHAP FEATURE IMPORTANCE BAR PLOT
# ============================================

print("Displaying SHAP feature importance plot...")

shap.summary_plot(
    shap_values,
    X_test,
    feature_names=all_feature_names,
    plot_type="bar"
)

# ============================================
# SINGLE PATIENT EXPLANATION
# ============================================

sample_index = 0

print(f"Explaining patient index: {sample_index}")

shap.force_plot(
    explainer.expected_value,
    shap_values[sample_index],
    X_test[sample_index],
    feature_names=all_feature_names,
    matplotlib=True
)

print("✅ SHAP analysis completed")