from sqlalchemy import Column, Integer, Float, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    email = Column(String(100))
    phone = Column(String(20))

    created_at = Column(DateTime, server_default=func.now())

    visits = relationship("Visit", back_populates="patient")


class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)

    temperature = Column(Float, nullable=False)
    pulse = Column(Integer, nullable=False)
    respiration = Column(Integer, nullable=False)
    systolic_bp = Column(Integer, nullable=False)
    diastolic_bp = Column(Integer, nullable=False)
    pain_scale = Column(Integer)

    arrival_mode = Column(String(20), nullable=False)
    ambtransfer = Column(Boolean, default=False)
    injury = Column(Integer, default=0)

    rfv1 = Column(Integer)
    rfv2 = Column(Integer)
    rfv3 = Column(Integer)
    rfv_text = Column(Text)

    status = Column(String(20), default="OPEN")
    doctor_notes = Column(Text)

    created_at = Column(DateTime, server_default=func.now())

    patient = relationship("Patient", back_populates="visits")
    predictions = relationship("Prediction", back_populates="visit")


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    visit_id = Column(Integer, ForeignKey("visits.id", ondelete="CASCADE"), nullable=False)

    classification = Column(String(20), nullable=False)
    risk_probability = Column(Float, nullable=False)
    override_triggered = Column(Boolean, nullable=False)

    model_version = Column(String(30), default="vFINAL_binary")
    created_at = Column(DateTime, server_default=func.now())

    visit = relationship("Visit", back_populates="predictions")