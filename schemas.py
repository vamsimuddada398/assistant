from pydantic import BaseModel
from datetime import date, datetime

class UserCreate(BaseModel):
    name: str
    dateofbirth: date


class AppointmentCreate(BaseModel):
    user_id: int
    appointment_date: datetime
    reason: str
