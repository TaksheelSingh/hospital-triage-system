import pandas as pd
import numpy as np
from scipy.sparse import hstack
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from xgboost import XGBClassifier

print("🔎 OVERRIDE SAFETY EVALUATION")

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

# ---------------- NUMERIC FEATURES ----------------
numeric_features = [
    "Is_Child","Is_Elderly","SEX",
    "TEMPF","PULSE","RESPR","BPSYS","BPDIAS","PAINSCALE",
    "Shock_Index","BP_DIFF",
    "Temp_High","Temp_Low","BP_Low","BP_High",
    "Resp_Abnormal","Pulse_Abnormal",
    "Instability_Score","High_Pain","Extreme_Phys",
    "ARREMS","AMBTRANSFER","INJURY",
    "RFV1","RFV2","RFV3"
]

X_num = df[numeric_features].fillna(0)

scaler = StandardScaler()
X_num_scaled = scaler.fit_transform(X_num)

tfidf = TfidfVectorizer(
    max_features=6000,
    ngram_range=(1, 2),
    token_pattern=r'(?u)\b[a-zA-Z][a-zA-Z]+\b'
)

X_text = tfidf.fit_transform(df["RFV_TEXT_ALL"].fillna("").astype(str))

X = hstack([X_text, X_num_scaled])  # keep sparse

# ---------------- TRAIN / TEST ----------------
X_train, X_test, y_train, y_test, df_train, df_test = train_test_split(
    X, y, df,
    test_size=0.2,
    stratify=y,
    random_state=42
)

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

# ---------------- EVALUATION @ 0.30 ----------------
threshold = 0.30

y_prob = model.predict_proba(X_test)[:, 1]
y_pred = (y_prob >= threshold).astype(int)

print("\nConfusion Matrix @ 0.30")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report @ 0.30")
print(classification_report(y_test, y_pred))
print("\nROC AUC:", roc_auc_score(y_test, y_prob))

# ---------------- FALSE NEGATIVES ----------------
false_negative_mask = (y_test == 1) & (y_pred == 0)
false_negatives = df_test[false_negative_mask]

print("\nTotal False Negatives:", false_negatives.shape[0])

# ---------------- OVERRIDE CHECK ----------------
override_mask = (
    (false_negatives["BPSYS"] < 80) |
    (false_negatives["PULSE"] > 150) |
    (false_negatives["RESPR"] > 35) |
    (false_negatives["Instability_Score"] >= 4)
)

override_caught = override_mask.sum()

print("Override would catch:", override_caught)

if false_negatives.shape[0] > 0:
    print("Override catch %:",
          override_caught / false_negatives.shape[0])

real_world_miss = false_negatives.shape[0] - override_caught
print("Real-world misses after override:", real_world_miss)