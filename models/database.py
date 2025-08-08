from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime


Base = declarative_base()

# =====================================================
# MODÈLES DATABASE
# =====================================================

class Medecin(Base):
    __tablename__ = "medecins"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    
    patients = relationship("Patient", back_populates="doctor", cascade="all, delete-orphan")

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    doctorid = Column(Integer, ForeignKey("medecins.id"))
    name = Column(String)
    age = Column(Integer)
    sex = Column(String)
    glucose = Column(Float)
    bmi = Column(Float)
    bloodpressure = Column(Float)
    pedigree = Column(Float)
    result = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    
    doctor = relationship("Medecin", back_populates="patients")
    predictions = relationship("Prediction", back_populates="patient", cascade="all, delete-orphan")

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    patientid = Column(Integer, ForeignKey("patients.id"))
    result = Column(Integer)  # 0 ou 1
    confidence = Column(Float)  # Pourcentage de confiance
    created_at = Column(DateTime, default=datetime.now)
    
    patient = relationship("Patient", back_populates="predictions")
