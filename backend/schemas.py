from pydantic import BaseModel
from typing import Optional


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