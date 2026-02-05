from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String) # patient, ambulance, hospital_admin, blood_bank_admin, donor, super_admin
    full_name = Column(String)
    blood_type = Column(String, nullable=True) # For donors/patients

class Hospital(Base):
    __tablename__ = "hospitals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String)
    icu_beds_total = Column(Integer, default=0)
    icu_beds_available = Column(Integer, default=0)
    doctors_available = Column(Integer, default=0)
    oxygen_cylinders = Column(Integer, default=0)
    ventilators = Column(Integer, default=0)
    readiness_score = Column(Float, default=0.0)

class BloodInventory(Base):
    __tablename__ = "blood_inventory"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    blood_type = Column(String) # A+, O-, etc.
    quantity = Column(Integer, default=0) # Users
    last_updated = Column(DateTime, default=datetime.utcnow)

class Ambulance(Base):
    __tablename__ = "ambulances"
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("users.id"))
    vehicle_number = Column(String)
    latitude = Column(Float, default=0.0)
    longitude = Column(Float, default=0.0)
    is_busy = Column(Boolean, default=False)
    current_eta = Column(String, nullable=True)

class EmergencyRequest(Base):
    __tablename__ = "emergency_requests"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    latitude = Column(Float)
    longitude = Column(Float)
    status = Column(String, default="PENDING") # PENDING, ASSIGNED, COMPLETED
    assigned_hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=True)
    assigned_ambulance_id = Column(Integer, ForeignKey("ambulances.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    emergency_type = Column(String, default="General") # Accident, Cardiac, etc.
