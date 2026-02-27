# 🏥 Hospital Triage System – Backend & ML

This is the backend service for the Hospital Triage and Doctor Consultation System.

Built using **FastAPI**, **SQLAlchemy**, and **PostgreSQL**, it integrates a Machine Learning model for visit risk classification.

---

# 🚀 Tech Stack

- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Pydantic
- Uvicorn
- Custom ML binary classification model

---

# 🧠 ML Model

The ML model predicts visit severity:

- Critical
- Needs Review

Output includes:
- classification
- risk_probability (0–1)
- model_version

Prediction is automatically triggered during visit creation.

---

# 🗄 Database Schema

## Patients

| Column | Type |
|--------|------|
| id | SERIAL PRIMARY KEY |
| full_name | VARCHAR(100) |
| age | INT |
| gender | VARCHAR(10) |
| email | VARCHAR(100) |
| phone | VARCHAR(20) UNIQUE |
| created_at | TIMESTAMP |

---

## Visits

| Column | Type |
|--------|------|
| id | SERIAL PRIMARY KEY |
| patient_id | FK → patients(id) |
| temperature | FLOAT |
| pulse | INT |
| systolic_bp | INT |
| diastolic_bp | INT |
| pain_scale | INT |
| rfv_text | TEXT |
| status | OPEN / IN_REVIEW / COMPLETED |
| doctor_notes | TEXT |
| created_at | TIMESTAMP |

---

## Predictions

| Column | Type |
|--------|------|
| id | SERIAL PRIMARY KEY |
| visit_id | FK → visits(id) |
| classification | Critical / Needs Review |
| risk_probability | FLOAT |
| model_version | VARCHAR |
| created_at | TIMESTAMP |

---

## Prescriptions

| Column | Type |
|--------|------|
| id | SERIAL PRIMARY KEY |
| visit_id | FK → visits(id) |
| medicine_name | VARCHAR |
| dosage_per_day | INT |
| tablets_per_dose | INT |
| start_date | DATE |
| end_date | DATE |
| total_tablets | INT |
| status | ACTIVE / DISCONTINUED |
| created_at | TIMESTAMP |

---

# 🔌 API Endpoints

## Patients


POST /patients
GET /patients/search-by-name?patient_name=
GET /patients/{patient_id}


---

## Visits


POST /visits/predict
GET /visits?patient_id=
PATCH /visits/{visit_id}/status?new_status=
PATCH /visits/{visit_id}/classification?classification=


---

## Prescriptions


POST /prescriptions
GET /prescriptions?visit_id=
PATCH /prescriptions/{id}/discontinue


---

# ⚙ Setup Instructions

## 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
2️⃣ Run Server
uvicorn main:app --reload

Backend runs at:

http://127.0.0.1:8000

🧪 Features Implemented
Patient search (fixed routing conflict)
ML severity prediction integration
Visit status update
Classification toggle
Prescription creation & discontinuation
Foreign key cascade integrity
Query filtering by patient_id and visit_id

📌 Notes
All calculations for total_tablets are done server-side.
Classification updates are validated.
Visit must exist before prediction is stored.
Phone number uniqueness enforced.