from pydantic import BaseModel,field_validator
from datetime import date, datetime
from dateutil import parser

class UserCreate(BaseModel):
    name: str
    dateofbirth: date
    
    @field_validator("dateofbirth", mode="before")
    @classmethod
    def parse_dob(cls, value):
        if isinstance(value, date):
            return value
        try:
            return parser.parse(value, dayfirst=True).date()
        except Exception:
            raise ValueError("Invalid date format")


class AppointmentCreate(BaseModel):
    user_id: int
    appointment_date: datetime
    reason: str
    
    @field_validator("appointment_date", mode="before")
    @classmethod
    def parse_appointment_date(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            return parser.parse(value, fuzzy=True)
        except Exception:
            raise ValueError("Invalid appointment date format")
