from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal, engine
import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Healthcare Dashboard API",
    description="API for managing users and appointments",
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    data = user.model_dump() if hasattr(user, "model_dump") else user.dict()
    db_user = models.User(**data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        "status": "success",
        "user_id": db_user.id,
        "name": db_user.name,
        "dateofbirth": str(db_user.dateofbirth)
    }


@app.post("/book")
def book_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    data = appointment.model_dump() if hasattr(appointment, "model_dump") else appointment.dict()
    db_appointment = models.Appointment(**data)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return {
        "status": "success",
        "appointment_id": db_appointment.id,
        "appointment_date": str(db_appointment.appointment_date),
        "appointment_time": str(db_appointment.appointment_time),
        "purpose": db_appointment.purpose
    }


@app.get("/status/{appointment_id}")
def check_status(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {
        "status": "success",
        "appointment_id": appointment.id,
        "appointment_date": str(appointment.appointment_date),
        "appointment_time": str(appointment.appointment_time),
        "purpose": appointment.purpose
    }


@app.put("/cancel/{appointment_id}")
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.status = "CANCELLED"
    db.commit()
    return {"message": "Appointment cancelled successfully"}


