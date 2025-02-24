from sqlalchemy import Column, Integer, String
from database.connection import Base

class HealthcareProvider(Base):
    __tablename__ = "healthcare_providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=True)
