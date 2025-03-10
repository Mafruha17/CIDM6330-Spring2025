from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
#from database.connection import Base  # Keeping original import

# ✅ Many-to-Many Relationship: Patient ↔ Provider
class PatientProviderLink(SQLModel, table=True):
    patient_id: int = Field(foreign_key="patient.id", primary_key=True)
    provider_id: int = Field(foreign_key="provider.id", primary_key=True)

# ✅ Provider Model
class Provider(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    specialty: str

    # Many-to-Many with Patients
    patients: List["Patient"] = Relationship(back_populates="providers", link_model=PatientProviderLink)

# ✅ Patient Model 
class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    age: int
    active: bool = Field(default=True)

    # ✅ Many-to-Many with Providers
    providers: List["Provider"] = Relationship(back_populates="patients", link_model=PatientProviderLink)

    # ✅ One-to-Many with Devices
    devices: List["Device"] = Relationship(back_populates="patient")

# ✅ Device Model (One-to-Many with Patients)
class Device(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    serial_number: str = Field(unique=True)
    active: bool = Field(default=True)
    
    patient_id: int = Field(foreign_key="patient.id")
    patient: Optional["Patient"] = Relationship(back_populates="devices")
