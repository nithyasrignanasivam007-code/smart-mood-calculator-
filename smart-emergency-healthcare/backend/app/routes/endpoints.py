from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import models
from ..schemas import schemas
from ..auth import get_current_user, create_access_token, verify_password, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES
from ..services.websocket_manager import manager
from ..ai_engine.coordinator import find_best_hospital
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
        full_name=user.full_name,
        blood_type=user.blood_type
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}

@router.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.post("/hospitals", response_model=schemas.HospitalResponse)
def create_hospital(hospital: schemas.HospitalCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role not in ["super_admin", "hospital_admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    db_hospital = models.Hospital(**hospital.dict())
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)
    return db_hospital

@router.get("/hospitals", response_model=List[schemas.HospitalResponse])
def read_hospitals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    hospitals = db.query(models.Hospital).offset(skip).limit(limit).all()
    return hospitals

@router.post("/emergency", response_model=schemas.EmergencyResponse)
async def create_emergency(emergency: schemas.EmergencyCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # 1. Create Emergency
    db_emergency = models.EmergencyRequest(
        patient_id=current_user.id,
        latitude=emergency.latitude,
        longitude=emergency.longitude,
        emergency_type=emergency.emergency_type,
        status="PENDING"
    )
    
    # 2. AI Assignment
    hospitals = db.query(models.Hospital).all()
    best_hospital = find_best_hospital(emergency.latitude, emergency.longitude, hospitals)
    
    if best_hospital:
        db_emergency.assigned_hospital_id = best_hospital.id
        db_emergency.status = "ASSIGNED"
    
    db.add(db_emergency)
    db.commit()
    db.refresh(db_emergency)
    
    # 3. WebSocket Broadcast
    await manager.broadcast(f"NEW_EMERGENCY: {db_emergency.id} at {emergency.latitude}, {emergency.longitude}")
    
    return db_emergency

@router.get("/my-emergency", response_model=List[schemas.EmergencyResponse])
def get_my_emergency(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.EmergencyRequest).filter(models.EmergencyRequest.patient_id == current_user.id).all()
