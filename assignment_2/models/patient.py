from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship  # ✅ Fix: Import `relationship`
from database.connection import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    age = Column(Integer, nullable=True)

    # ✅ Fix: Ensure `back_populates` matches the attribute in `Device`
    devices = relationship("Device", back_populates="patient")
