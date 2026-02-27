from sqlalchemy.orm import Session
import models
import schemas

# -----------------------
# PATIENT CRUD
# -----------------------

def create_patient(db: Session, patient):

    # If patient is dict
    phone = patient.get("phone")

    existing_patient = (
        db.query(models.Patient)
        .filter(models.Patient.phone == phone)
        .first()
    )

    if existing_patient:
        return existing_patient

    db_patient = models.Patient(**patient)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)

    return db_patient


def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()


# -----------------------
# VISIT CRUD
# -----------------------

def create_visit(db: Session, visit_data):
    visit = models.Visit(**visit_data)
    db.add(visit)
    db.commit()
    db.refresh(visit)
    return visit


def update_visit_status(db: Session, visit_id: int, new_status: str):
    visit = db.query(models.Visit).filter(models.Visit.id == visit_id).first()
    if visit:
        visit.status = new_status
        db.commit()
        db.refresh(visit)
    return visit


# -----------------------
# PREDICTION CRUD
# -----------------------

def create_prediction(db: Session, visit_id: int, classification: str, probability: float):
    prediction = models.Prediction(
        visit_id=visit_id,
        classification=classification,
        risk_probability=probability
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction


def update_classification(db: Session, visit_id: int, classification: str):
    prediction = db.query(models.Prediction).filter(
        models.Prediction.visit_id == visit_id
    ).first()

    if prediction:
        prediction.classification = classification
        db.commit()
        db.refresh(prediction)

    return prediction


# -----------------------
# PRESCRIPTION CRUD
# -----------------------

def add_prescription(db: Session, prescription_data):
    prescription = models.Prescription(**prescription_data)
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    return prescription


def discontinue_prescription(db: Session, prescription_id: int):
    prescription = db.query(models.Prescription).filter(
        models.Prescription.id == prescription_id
    ).first()

    if prescription:
        prescription.status = "DISCONTINUED"
        db.commit()
        db.refresh(prescription)

    return prescription