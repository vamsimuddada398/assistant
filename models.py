from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    dateofbirth = Column(Date)


class Appointment(Base):
    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    appointment_date = Column(DateTime)
    reason = Column(String(255))
    status = Column(String(20), default="BOOKED")
