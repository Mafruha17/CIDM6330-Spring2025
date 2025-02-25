from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    age = Column(Integer, nullable=True)

    devices = relationship("Device", back_populates="patient")


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String, unique=True, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)

    patient = relationship("Patient", back_populates="devices")
