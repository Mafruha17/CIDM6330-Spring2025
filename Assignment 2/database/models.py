from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from database.connection import Base  # Keeping original import

# ✅ Many-to-Many Relationship: Patient ↔ Provider
patient_provider_association = Table(
    "patient_provider_association",
    Base.metadata,
    Column("patient_id", Integer, ForeignKey("patients.id", ondelete="CASCADE"), primary_key=True),
    Column("provider_id", Integer, ForeignKey("providers.id", ondelete="CASCADE"), primary_key=True),
)

# ✅ Provider Model
class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    specialty = Column(String, nullable=False)

    # Many-to-Many with Patients
    patients = relationship("Patient", secondary=patient_provider_association, back_populates="providers")

# ✅ Patient Model 
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)

    # ✅ Many-to-Many with Providers (Explicitly Remove on Delete)
    providers = relationship(
        "Provider",
        secondary=patient_provider_association,
        back_populates="patients",
        cascade="all, delete",  # Ensures associated records are removed
        passive_deletes=True    # Helps with foreign key constraints
    )

    # ✅ One-to-Many with Devices (Ensure Correct back_populates)
    devices = relationship(
        "Device",
        back_populates="patient",
        cascade="all, delete",
        passive_deletes=True
    )

# ✅ Device Model (One-to-Many with Patients)
class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String, nullable=False, unique=True)
    active = Column(Boolean, default=True)

    # ✅ Foreign Key to Patient
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    
    patient = relationship("Patient", back_populates="devices")
