from pydantic import BaseModel, field_validator
from datetime import date, datetime, time
from dateutil import parser


# ------------------ USER ------------------

class UserCreate(BaseModel):
    name: str
    dateofbirth: date

    @field_validator("dateofbirth", mode="before")
    @classmethod
    def parse_dob(cls, value):
        if isinstance(value, date):
            return value
        return parser.parse(value, dayfirst=True).date()


class UserResponse(BaseModel):
    id: int
    name: str
    dateofbirth: date

    class Config:
        from_attributes = True


# ------------------ APPOINTMENT ------------------

class AppointmentCreate(BaseModel):
    user_id: int
    appointment_date: date
    appointment_time: time
    purpose: str

    @field_validator("appointment_date", mode="before")
    @classmethod
    def parse_appointment_date(cls, value):
        if isinstance(value, date):
            return value
        return parser.parse(value, fuzzy=True).date()

    @field_validator("appointment_time", mode="before")
    @classmethod
    def parse_appointment_time(cls, value):
        if isinstance(value, time):
            return value
        return parser.parse(value, fuzzy=True).time()


class AppointmentResponse(BaseModel):
    id: int
    user_id: int
    appointment_date: date
    appointment_time: time
    purpose: str
    status: str

    class Config:
        from_attributes = True


# ------------------ EXTRA ------------------

class UserWithAppointments(UserResponse):
    appointments: list[AppointmentResponse] = []


class DashboardStats(BaseModel):
    total_users: int
    total_appointments: int
    booked: int
    cancelled: int


class AppointmentWithUser(AppointmentResponse):
    user_name: str = ""
