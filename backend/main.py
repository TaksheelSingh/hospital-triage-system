from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Patient, Visit, Prediction
from schemas import PatientCreate, VisitCreate, PredictionResponse
from ml import predict

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==============================
# CREATE PATIENT
# ==============================

@app.post("/patients")
def create_patient(request: PatientCreate, db: Session = Depends(get_db)):

    patient = Patient(**request.dict())

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient


# ==============================
# GET PATIENT
# ==============================

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int, db: Session = Depends(get_db)):

    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patient


# ==============================
# CREATE VISIT
# ==============================

@app.post("/visits")
def create_visit(request: VisitCreate, db: Session = Depends(get_db)):

    visit = Visit(**request.dict())

    db.add(visit)
    db.commit()
    db.refresh(visit)

    return visit


# ==============================
# GET VISIT
# ==============================

@app.get("/visits/{visit_id}")
def get_visit(visit_id: int, db: Session = Depends(get_db)):

    visit = db.query(Visit).filter(Visit.id == visit_id).first()

    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")

    return visit


# ==============================
# RUN TRIAGE
# ==============================

@app.post("/triage/{visit_id}", response_model=PredictionResponse)
def run_triage(visit_id: int, db: Session = Depends(get_db)):

    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")

    patient = db.query(Patient).filter(Patient.id == visit.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # ----------------------
    # Map DB → ML input
    # ----------------------

    ml_input = {
        "AGE": patient.age,
        "SEX": 1 if patient.gender.lower() == "male" else 2,
        "TEMPF": visit.temperature,
        "PULSE": visit.pulse,
        "RESPR": visit.respiration,
        "BPSYS": visit.systolic_bp,
        "BPDIAS": visit.diastolic_bp,
        "PAINSCALE": visit.pain_scale,
        "ARREMS": 1 if visit.arrival_mode == "Ambulance" else 0,
        "AMBTRANSFER": 1 if visit.ambtransfer else 0,
        "INJURY": visit.injury,
        "RFV1": visit.rfv1,
        "RFV2": visit.rfv2,
        "RFV3": visit.rfv3,
        "RFV_TEXT_ALL": visit.rfv_text
    }

    label, prob, override = predict(ml_input)

    prediction = Prediction(
        visit_id=visit.id,
        classification=label,
        risk_probability=prob,
        override_triggered=override
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return {
        "visit_id": visit.id,
        "classification": label,
        "risk_probability": prob,
        "override_triggered": override
    }


# ==============================
# GET PREDICTIONS FOR VISIT
# ==============================

@app.get("/predictions/{visit_id}")
def get_predictions(visit_id: int, db: Session = Depends(get_db)):

    preds = db.query(Prediction).filter(Prediction.visit_id == visit_id).all()

    return preds