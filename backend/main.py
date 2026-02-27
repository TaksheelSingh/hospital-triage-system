from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal

import models  # move this to top with other imports
import crud, schemas
from ml import predict
from datetime import datetime

app = FastAPI(title="MediCare AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# DATABASE DEPENDENCY
# =====================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/")
def health():
    return {"status": "Backend running"}


# =====================================================
# PATIENT ENDPOINTS
# =====================================================

@app.post("/patients", response_model=schemas.PatientResponse)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db, patient.dict())


@app.get("/patients/search-by-name")
def search_patient(patient_name: str, db: Session = Depends(get_db)):
    patients = db.query(models.Patient).filter(
        models.Patient.full_name.ilike(f"%{patient_name}%")
    ).all()

    return patients


@app.get("/patients/{patient_id}")
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# =====================================================
# VISIT + ML PREDICTION
# =====================================================

@app.post("/visits/predict")
def create_visit_and_predict(
    visit: schemas.VisitCreate,
    db: Session = Depends(get_db)
):

    # 1️⃣ Verify patient exists
    patient = crud.get_patient(db, visit.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # 2️⃣ Create visit record
    db_visit = crud.create_visit(db, visit.dict())

    # 3️⃣ Prepare ML input (merge patient age)
    ml_input = visit.dict()
    ml_input["age"] = patient.age

    # 4️⃣ Run prediction
    probability, classification = predict(ml_input)

    # 5️⃣ Store prediction
    crud.create_prediction(
        db,
        db_visit.id,
        classification,
        probability
    )

    return {
        "visit_id": db_visit.id,
        "classification": classification,
        "risk_probability": probability,
        "status": "OPEN"
    }


# =====================================================
# UPDATE VISIT STATUS
# =====================================================

@app.patch("/visits/{visit_id}/status")
def update_visit_status(
    visit_id: int,
    new_status: str,
    db: Session = Depends(get_db)
):

    if new_status not in ["OPEN", "IN_REVIEW", "COMPLETED"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    visit = crud.update_visit_status(db, visit_id, new_status)

    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")

    return {
        "visit_id": visit_id,
        "new_status": new_status
    }


# =====================================================
# UPDATE CLASSIFICATION (FLAG CRITICAL)
# =====================================================

@app.patch("/visits/{visit_id}/classification")
def update_classification(
    visit_id: int,
    classification: str,
    db: Session = Depends(get_db)
):

    if classification not in ["Critical", "Needs Review"]:
        raise HTTPException(status_code=400, detail="Invalid classification")

    prediction = crud.update_classification(db, visit_id, classification)

    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")

    return {
        "visit_id": visit_id,
        "classification": classification
    }


# =====================================================
# ADD PRESCRIPTION
# =====================================================

@app.post("/prescriptions")
def add_prescription(
    visit_id: int,
    medicine_name: str,
    dosage_per_day: int,
    tablets_per_dose: int,
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db)
):

    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()

    days = (end - start).days + 1
    total_tablets = days * dosage_per_day * tablets_per_dose

    prescription_data = {
        "visit_id": visit_id,
        "medicine_name": medicine_name,
        "dosage_per_day": dosage_per_day,
        "tablets_per_dose": tablets_per_dose,
        "start_date": start,
        "end_date": end,
        "total_tablets": total_tablets
    }

    prescription = crud.add_prescription(db, prescription_data)

    return {
        "prescription_id": prescription.id,
        "total_tablets": total_tablets,
        "status": prescription.status
    }


# =====================================================
# DISCONTINUE PRESCRIPTION
# =====================================================

@app.patch("/prescriptions/{prescription_id}/discontinue")
def discontinue_prescription(
    prescription_id: int,
    db: Session = Depends(get_db)
):

    prescription = crud.discontinue_prescription(db, prescription_id)

    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")

    return {
        "prescription_id": prescription_id,
        "status": "DISCONTINUED"
    }

# =====================================================
# GET PRESCRIPTIONS BY VISIT
# =====================================================

@app.get("/prescriptions")
def get_prescriptions(
    visit_id: int,
    db: Session = Depends(get_db)
):
    prescriptions = (
        db.query(models.Prescription)
        .filter(models.Prescription.visit_id == visit_id)
        .all()
    )

    return prescriptions

# =====================================================
# GET ALL VISITS (Dashboard)
# =====================================================

from sqlalchemy.orm import joinedload
import models

@app.get("/visits")
def get_all_visits(db: Session = Depends(get_db)):
    visits = (
        db.query(models.Visit)
        .options(joinedload(models.Visit.prediction))
        .all()
    )

    result = []

    for v in visits:
        result.append({
            "id": v.id,
            "status": v.status,
            "created_at": v.created_at,
            "classification": v.prediction.classification if v.prediction else None,
            "risk_probability": v.prediction.risk_probability if v.prediction else None,
        })

    return result