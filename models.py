from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    dateofbirth = Column(Date, nullable=False)


class Appointment(Base):
    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)

    purpose = Column(String(255), nullable=False)

    status = Column(String(20), default="BOOKED")
