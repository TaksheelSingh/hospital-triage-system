from pydantic import BaseModel
from typing import Optional
from datetime import date

class PatientCreate(BaseModel):
    full_name: str
    age: int
    gender: str
    email: Optional[str]
    phone: Optional[str]


class VisitCreate(BaseModel):
    patient_id: int
    temperature: float
    pulse: int
    respiration: int
    systolic_bp: int
    diastolic_bp: int
    pain_scale: int
    arrival_mode: str
    ambtransfer: bool
    injury: int
    rfv1: int
    rfv2: int
    rfv3: int
    rfv_text: str


class PredictionResponse(BaseModel):
    visit_id: int
    classification: str
    risk_probability: float
    override_triggered: bool


class PrescriptionCreate(BaseModel):
    visit_id: int
    medicine_name: str
    dosage_per_day: int
    tablets_per_dose: int
    start_date: date
    end_date: date
    remarks: Optional[str] = None

class PrescriptionResponse(BaseModel):
    id: int
    visit_id: int
    medicine_name: str
    dosage_per_day: int
    tablets_per_dose: int
    start_date: date
    end_date: date
    total_tablets: int
    remarks: Optional[str]
    status: str

    class Config:
        orm_mode = True