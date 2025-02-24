from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String, unique=True, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=True)

    # ✅ Fix: Ensure `back_populates` matches `models/patient.py`
    patient = relationship("Patient", back_populates="devices")
