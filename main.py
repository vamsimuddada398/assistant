from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal, engine
import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Healthcare Dashboard API",
    description="API for managing users and appointments",
)

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


# ✅ REGISTER
@app.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # prevent duplicates
    existing = db.query(models.User).filter(
        func.lower(models.User.name) == user.name.lower(),
        models.User.dateofbirth == user.dateofbirth
    ).first()

    if existing:
        return {
            "status": "existing",
            "user_id": existing.id,
            "name": existing.name,
            "dateofbirth": str(existing.dateofbirth)
        }

    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "status": "success",
        "user_id": db_user.id,
        "name": db_user.name,
        "dateofbirth": str(db_user.dateofbirth)
    }


# ✅ BOOK APPOINTMENT
@app.post("/book")
def book_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == appointment.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_appointment = models.Appointment(**appointment.model_dump())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)

    return {
        "status": "success",
        "appointment_id": db_appointment.id,
        "appointment_date": str(db_appointment.appointment_date),
        "appointment_time": str(db_appointment.appointment_time),
        "purpose": db_appointment.purpose,
        "appointment_status": db_appointment.status
    }


# ✅ CHECK STATUS
@app.get("/status/{appointment_id}")
def check_status(appointment_id: int, db: Session = Depends(get_db)):

    appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return {
        "status": "success",
        "appointment_id": appointment.id,
        "appointment_date": str(appointment.appointment_date),
        "appointment_time": str(appointment.appointment_time),
        "purpose": appointment.purpose,
        "appointment_status": appointment.status
    }


# ✅ CANCEL
@app.put("/cancel/{appointment_id}")
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):

    appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.status = "CANCELLED"
    db.commit()

    return {
        "status": "success",
        "message": "Appointment cancelled successfully"
    }
