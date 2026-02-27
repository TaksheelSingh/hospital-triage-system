from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date, Time, Text, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10))
    email = Column(String(100))
    phone = Column(String(20))
    created_at = Column(TIMESTAMP, server_default=func.now())

    visits = relationship("Visit", back_populates="patient")


class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"))

    arrival_mode = Column(String(20))
    ambtransfer = Column(Boolean, default=False)
    arrival_time = Column(Time)

    temperature = Column(Float)
    pulse = Column(Integer)
    respiration = Column(Integer)
    systolic_bp = Column(Integer)
    diastolic_bp = Column(Integer)
    pain_scale = Column(Integer)

    rfv1 = Column(Integer)
    rfv2 = Column(Integer)
    rfv3 = Column(Integer)
    rfv_text = Column(Text)

    status = Column(String(20), default="OPEN")
    doctor_notes = Column(Text)

    created_at = Column(TIMESTAMP, server_default=func.now())

    patient = relationship("Patient", back_populates="visits")
    prediction = relationship("Prediction", back_populates="visit", uselist=False)
    prescriptions = relationship("Prescription", back_populates="visit")


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    visit_id = Column(Integer, ForeignKey("visits.id", ondelete="CASCADE"))

    classification = Column(String(20))
    risk_probability = Column(Float)
    model_version = Column(String(30), default="vFINAL_binary")
    created_at = Column(TIMESTAMP, server_default=func.now())

    visit = relationship("Visit", back_populates="prediction")


class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    visit_id = Column(Integer, ForeignKey("visits.id", ondelete="CASCADE"))

    medicine_name = Column(String(100))
    dosage_per_day = Column(Integer)
    tablets_per_dose = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
    total_tablets = Column(Integer)
    status = Column(String(20), default="ACTIVE")

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    visit = relationship("Visit", back_populates="prescriptions")