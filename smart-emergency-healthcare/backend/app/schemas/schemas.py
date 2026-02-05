from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    role: str
    full_name: str
    blood_type: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class LoginRequest(BaseModel):
    username: str
    password: str

class HospitalBase(BaseModel):
    name: str
    latitude: float
    longitude: float
    address: str
    icu_beds_total: int
    icu_beds_available: int
    doctors_available: int
    oxygen_cylinders: int
    ventilators: int

class HospitalCreate(HospitalBase):
    pass

class HospitalResponse(HospitalBase):
    id: int
    readiness_score: float
    class Config:
        from_attributes = True

class EmergencyCreate(BaseModel):
    latitude: float
    longitude: float
    emergency_type: str

class EmergencyResponse(BaseModel):
    id: int
    status: str
    assigned_hospital_id: Optional[int]
    assigned_ambulance_id: Optional[int]
    class Config:
        from_attributes = True

class AmbulanceUpdate(BaseModel):
    latitude: float
    longitude: float
    is_busy: bool
    current_eta: Optional[str] = None
