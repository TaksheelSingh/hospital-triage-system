from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas
from security.crypto import aes_encrypt
from security.crypto import aes_decrypt
from security.crypto import compute_hash
from security.ids import log_security_event
import crud
from services.email_service import send_email
from security_models import SecurityLog
from database import Base
from database import SessionLocal
from models import Patient, Visit, Prediction
from schemas import PatientCreate, VisitCreate, PredictionResponse
from ml import predict
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hospital Triage API Running"}

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

    encrypted_email, email_iv = aes_encrypt(request.email)
    encrypted_phone, phone_iv = aes_encrypt(request.phone)

    patient = Patient(
        full_name=request.full_name,
        age=request.age,
        gender=request.gender,

        email=None,
        phone=None,

        email_encrypted=encrypted_email,
        email_iv=email_iv,
        phone_encrypted=encrypted_phone,
        phone_iv=phone_iv
    )

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

    # Decrypt before returning
    decrypted_email = None
    decrypted_phone = None

    if patient.email_encrypted and patient.email_iv:
        decrypted_email = aes_decrypt(patient.email_encrypted, patient.email_iv)

    if patient.phone_encrypted and patient.phone_iv:
        decrypted_phone = aes_decrypt(patient.phone_encrypted, patient.phone_iv)

    return {
        "id": patient.id,
        "full_name": patient.full_name,
        "age": patient.age,
        "gender": patient.gender,
        "email": decrypted_email,
        "phone": decrypted_phone,
        "created_at": patient.created_at
    }


# ==============================
# CREATE VISIT
# ==============================

@app.post("/visits")
def create_visit(request: VisitCreate, db: Session = Depends(get_db)):

    data = request.dict()

    from security.crypto import aes_encrypt

    encrypted_rfv, rfv_iv = aes_encrypt(data["rfv_text"])

    visit = Visit(
        patient_id=data["patient_id"],
        temperature=data["temperature"],
        pulse=data["pulse"],
        respiration=data["respiration"],
        systolic_bp=data["systolic_bp"],
        diastolic_bp=data["diastolic_bp"],
        pain_scale=data["pain_scale"],
        arrival_mode=data["arrival_mode"],
        ambtransfer=data["ambtransfer"],
        injury=data["injury"],
        rfv1=data["rfv1"],
        rfv2=data["rfv2"],
        rfv3=data["rfv3"],

        rfv_text=None,  # stop storing plaintext
        rfv_text_encrypted=encrypted_rfv,
        rfv_text_iv=rfv_iv,

        status="OPEN"
    )

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

    visit = db.query(Visit).filter(
        Visit.id == visit_id
    ).first()

    if not visit:
        raise HTTPException(
            status_code=404,
            detail="Visit not found"
        )

    patient = db.query(Patient).filter(
        Patient.id == visit.patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # ----------------------
    # Decrypt RFV text before ML
    # ----------------------

    decrypted_rfv = ""

    if visit.rfv_text_encrypted and visit.rfv_text_iv:

        decrypted_rfv = aes_decrypt(
            visit.rfv_text_encrypted,
            visit.rfv_text_iv
        )

    # ----------------------
    # Map DB → ML Input
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
        "RFV_TEXT_ALL": decrypted_rfv
    }

    # ----------------------
    # Run ML Prediction
    # ----------------------

    label, prob, override = predict(ml_input)

    prediction = Prediction(
        visit_id=visit.id,
        classification=label,
        original_classification=label,
        risk_probability=prob,
        override_triggered=override
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    # ----------------------
    # SHA Integrity Hash
    # ----------------------

    hash_data = (
        f"{prediction.visit_id}"
        f"{prediction.classification}"
        f"{prediction.risk_probability}"
        f"{prediction.override_triggered}"
        f"{prediction.model_version}"
    )

    prediction.integrity_hash = compute_hash(hash_data)

    db.commit()

    # ----------------------
    # IDS Logging
    # ----------------------

    if override:

        log_security_event(
            db,
            "SEVERITY_OVERRIDE",
            "prediction",
            prediction.id,
            "INFO",
            "Clinical override triggered before ML decision"
        )

    return {
        "visit_id": visit.id,
        "classification": label,
        "risk_probability": prob,
        "override_triggered": override
    }


# ==============================
# GET PREDICTIONS FOR VISIT
# ==============================

@app.get("/predictions/{visit_id}", response_model=list[PredictionResponse])
def get_predictions(visit_id: int, db: Session = Depends(get_db)):

    preds = db.query(Prediction).filter(
        Prediction.visit_id == visit_id
    ).all()

    for p in preds:

        # Skip records created before SHA was implemented
        if not p.integrity_hash:
            continue

        # Recompute hash
        hash_data = (
            f"{p.visit_id}"
            f"{p.classification}"
            f"{p.risk_probability}"
            f"{p.override_triggered}"
            f"{p.model_version}"
        )

        computed_hash = compute_hash(hash_data)

        # Detect tampering
        if p.integrity_hash != computed_hash:

            existing_event = db.query(SecurityLog).filter(
                SecurityLog.event_type == "HASH_MISMATCH",
                SecurityLog.entity == "prediction",
                SecurityLog.entity_id == p.id
            ).first()

            if not existing_event:

                log_security_event(
                    db,
                    "HASH_MISMATCH",
                    "prediction",
                    p.id,
                    "HIGH",
                    "Prediction data integrity mismatch detected"
                )

    return preds


# ==============================
# Prescriptions
# ==============================

@app.post("/prescriptions", response_model=schemas.PrescriptionResponse)
def add_prescription(
    prescription: schemas.PrescriptionCreate,
    db: Session = Depends(get_db)
):

    # --------------------------------
    # Create Prescription
    # --------------------------------

    new_prescription = crud.create_prescription(
        db,
        prescription.dict()
    )

    print("Prescription endpoint reached")

    # --------------------------------
    # Fetch Visit
    # --------------------------------

    visit = db.query(Visit).filter(
        Visit.id == prescription.visit_id
    ).first()

    if not visit:
        raise HTTPException(
            status_code=404,
            detail="Visit not found"
        )

    # --------------------------------
    # Fetch Patient
    # --------------------------------

    patient = db.query(Patient).filter(
        Patient.id == visit.patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # --------------------------------
    # Decrypt Patient Email
    # --------------------------------

    patient_email = None

    if patient.email_encrypted and patient.email_iv:

        patient_email = aes_decrypt(
            patient.email_encrypted,
            patient.email_iv
        )

        print("Patient email decrypted")
        print(patient_email)

    # --------------------------------
    # Send Prescription Email
    # --------------------------------

    if patient_email:

        email_subject = "CareQueue Prescription Summary"

        email_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">

            <h2 style="color:#2c3e50;">
                CareQueue Prescription Summary
            </h2>

            <p>
                <strong>Patient Name:</strong> {patient.full_name}<br>
                <strong>Visit ID:</strong> {visit.id}<br>
                <strong>Generated On:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M")}
            </p>

            <table 
                border="1" 
                cellpadding="10" 
                cellspacing="0"
                style="border-collapse: collapse; width: 70%;"
            >

                <tr style="background-color:#f2f2f2;">
                    <th align="left">Field</th>
                    <th align="left">Details</th>
                </tr>

                <tr>
                    <td><strong>Medicine Name</strong></td>
                    <td>{new_prescription.medicine_name}</td>
                </tr>

                <tr>
                    <td><strong>Dosage Per Day</strong></td>
                    <td>{new_prescription.dosage_per_day}</td>
                </tr>

                <tr>
                    <td><strong>Tablets Per Dose</strong></td>
                    <td>{new_prescription.tablets_per_dose}</td>
                </tr>

                <tr>
                    <td><strong>Total Tablets</strong></td>
                    <td>{new_prescription.total_tablets}</td>
                </tr>

                <tr>
                    <td><strong>Start Date</strong></td>
                    <td>{new_prescription.start_date}</td>
                </tr>

                <tr>
                    <td><strong>End Date</strong></td>
                    <td>{new_prescription.end_date}</td>
                </tr>

            </table>

            <br>

            <h3>Doctor Remarks</h3>

            <p>
                {new_prescription.remarks}
            </p>

            <hr>

            <p style="font-size: 13px; color: gray;">
                This is an automated prescription summary generated by the
                CareQueue Healthcare Management System.
            </p>

        </body>
        </html>
        """

        print("Sending email now...")

        send_email(
            patient_email,
            email_subject,
            email_body
        )

    return new_prescription


@app.get("/prescriptions/{visit_id}", response_model=list[schemas.PrescriptionResponse])
def fetch_prescriptions(visit_id: int, db: Session = Depends(get_db)):
    return crud.get_prescriptions_by_visit(db, visit_id)


@app.put("/prescriptions/discontinue/{prescription_id}", response_model=schemas.PrescriptionResponse)
def discontinue(prescription_id: int, db: Session = Depends(get_db)):
    return crud.discontinue_prescription(db, prescription_id)