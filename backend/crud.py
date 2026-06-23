from sqlalchemy.orm import Session
from models import Visit
from datetime import date
import models
from security.crypto import aes_encrypt, aes_decrypt, compute_hash
from security.ids import log_security_event


def create_visit(db: Session, data: dict, label, prob, override):

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

        rfv_text=None,
        rfv_text_encrypted=encrypted_rfv,
        rfv_text_iv=rfv_iv,

        classification=label,
        risk_probability=prob,
        override_triggered=override,
        status="OPEN"
    )

    db.add(visit)
    db.commit()
    db.refresh(visit)

    # Integrity hash
    hash_string = (
        str(visit.id)
        + label
        + str(prob)
        + str(override)
    )

    visit.integrity_hash = compute_hash(hash_string)
    db.commit()

    if override:
        log_security_event(
            db,
            "SEVERITY_OVERRIDE",
            "visit",
            visit.id,
            "INFO",
            "Clinical override triggered"
        )

    return visit

def create_prescription(db, prescription_data):
    days = (prescription_data["end_date"] - prescription_data["start_date"]).days + 1
    total_tablets = days * prescription_data["dosage_per_day"] * prescription_data["tablets_per_dose"]

    db_prescription = models.Prescription(
        visit_id=prescription_data["visit_id"],
        medicine_name=prescription_data["medicine_name"],
        dosage_per_day=prescription_data["dosage_per_day"],
        tablets_per_dose=prescription_data["tablets_per_dose"],
        start_date=prescription_data["start_date"],
        end_date=prescription_data["end_date"],
        total_tablets=total_tablets,
        remarks=prescription_data.get("remarks"),
        status="ACTIVE"
    )

    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    return db_prescription


def get_prescriptions_by_visit(db, visit_id: int):
    prescriptions = db.query(models.Prescription).filter(
        models.Prescription.visit_id == visit_id
    ).all()

    today = date.today()

    for p in prescriptions:
        if p.status != "DISCONTINUED" and today > p.end_date:
            p.status = "DISCONTINUED"

    return prescriptions


def discontinue_prescription(db, prescription_id: int):
    prescription = db.query(models.Prescription).filter(
        models.Prescription.id == prescription_id
    ).first()

    if prescription:
        prescription.status = "DISCONTINUED"
        db.commit()
        db.refresh(prescription)

    return prescription