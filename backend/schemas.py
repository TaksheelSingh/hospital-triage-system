from pydantic import BaseModel
from typing import Optional
from datetime import date, time


# -----------------------
# PATIENT
# -----------------------

class PatientCreate(BaseModel):
    full_name: str
    age: int
    gender: Optional[str]
    email: Optional[str]
    phone: Optional[str]


class PatientResponse(BaseModel):
    id: int
    full_name: str
    age: int

    class Config:
        from_attributes = True


# -----------------------
# VISIT + PREDICTION
# -----------------------

class VisitCreate(BaseModel):
    patient_id: int
    arrival_mode: str
    ambtransfer: bool
    arrival_time: Optional[time]

    temperature: float
    pulse: int
    respiration: int
    systolic_bp: int
    diastolic_bp: int
    pain_scale: int

    rfv1: Optional[int]
    rfv2: Optional[int]
    rfv3: Optional[int]
    rfv_text: Optional[str]


class PredictionResponse(BaseModel):
    visit_id: int
    classification: str
    risk_probability: float