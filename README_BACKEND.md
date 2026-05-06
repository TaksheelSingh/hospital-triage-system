# Secure AI-Driven Emergency Assistance Framework – Backend

## Overview

This backend system powers the AI-assisted emergency triage platform.  
It provides REST APIs for patient management, visit handling, severity prediction, prescription generation, and cybersecurity monitoring.

The backend integrates:
- Machine Learning–based severity prediction
- Clinical safety override logic
- AES-256 encryption for sensitive patient data
- SHA-256 integrity verification
- Intrusion detection and security logging

---

# Technologies Used

- FastAPI
- Python 3.11+
- PostgreSQL
- SQLAlchemy
- XGBoost
- Scikit-learn
- Cryptography
- Uvicorn

---

# Project Structure

```text
backend/
│
├── main.py
├── crud.py
├── database.py
├── models.py
├── schemas.py
├── ml.py
├── requirements.txt
│
├── security/
│   ├── encryption.py
│   ├── hashing.py
│   └── ids.py
│
├── artifacts_binary_final_v2/
│   ├── xgb_binary_model.pkl
│   ├── tfidf.pkl
│   ├── scaler.pkl
│   └── numeric_features.pkl
│
└── routers/
```

---

# Backend Setup Instructions

## 1. Create Virtual Environment

```bash
python -m venv venv
```

Activate virtual environment:

### Windows
```bash
venv\Scripts\activate
```

### Linux / Mac
```bash
source venv/bin/activate
```

---

# 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 3. Configure PostgreSQL Database

Create PostgreSQL database:

```sql
CREATE DATABASE hospital_triage;
```

Update database configuration in:

```text
database.py
```

Example:

```python
DATABASE_URL = "postgresql://postgres:password@localhost/hospital_triage"
```

---

# 4. Run Backend Server

```bash
uvicorn main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

Swagger API Documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Machine Learning Pipeline

The backend uses an XGBoost-based binary classification model.

## Features Used
- Vital signs
- Pain scale
- RFV codes
- TF-IDF processed complaint text
- Engineered instability indicators

## Final Classification
- Critical
- Needs Review

Threshold tuning is used to improve recall for critical patients.

---

# Cybersecurity Features

## AES-256 Encryption
Sensitive patient fields such as:
- Email
- Phone number
- RFV text

are encrypted before database storage.

---

## SHA-256 Integrity Verification

Prediction outputs are hashed using SHA-256.

If prediction data is modified:
- Hash mismatch is detected
- Security event is logged

---

## Intrusion Detection System (IDS)

The IDS monitors:
- Prediction tampering
- Severity overrides
- Abnormal access behavior

Events are stored in:
```text
security_logs
```

---

# API Modules

| Module | Purpose |
|---|---|
| Patient API | Patient registration and retrieval |
| Visit API | Visit and vitals handling |
| Prediction API | ML severity prediction |
| Prescription API | Prescription generation |
| Security API | Logging and monitoring |

---

# Sample Security Events

- HASH_MISMATCH
- SEVERITY_OVERRIDE

---

# Output

The backend provides:
- Real-time patient severity prediction
- Secure patient data storage
- Clinical override support
- Security event monitoring
- Prescription management

---

# Authors

- Taksheel Rawat
- Aryan Arora