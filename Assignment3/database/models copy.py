from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

# Many-to-Many Relationship: Patient ↔ Provider
class PatientProviderLink(SQLModel, table=True):
    patient_id: int = Field(foreign_key="patient.id", primary_key=True)
    provider_id: int = Field(foreign_key="provider.id", primary_key=True)
 

# Provider Model
class Provider(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    specialty: str

    # Many-to-Many with Patients
    patients: List["Patient"] = Relationship(
        back_populates="providers",
        link_model=PatientProviderLink
    )

# Patient Model
class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    age: int
    active: bool = Field(default=True)

    # Many-to-Many with Providers
    providers: List["Provider"] = Relationship(
        back_populates="patients",
        link_model=PatientProviderLink
    )

    # One-to-Many with Devices
    devices: List["Device"] = Relationship("Device",back_populates="patient",
                                           cascade_delete= "all, delete",
                                           passive_deletes= True)

# Device Model (One-to-Many with Patient)
class Device(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    serial_number: str = Field(unique=True)
    active: bool = Field(default=True)

    #patient_id: int = Field(foreign_key="patient.id")
    # from typing import Optional
    # After: allow device creation without an associated patient
    patient_id: Optional[int] = Field(default=None, foreign_key="patient.id", ondelete="CASCADE",nullable=False)
    patient: Optional["Patient"] = Relationship(back_populates="devices")

    
