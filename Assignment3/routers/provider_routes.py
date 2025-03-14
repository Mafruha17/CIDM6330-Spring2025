from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from database.models import Provider  # ✅ Ensure this import is present
from database.connection import get_db
from schemas.provider import ProviderSchema
from database.crud.provider_crud import (
    create_provider, get_provider, get_all_providers, update_provider, delete_provider,
    get_patients_by_provider
)

router = APIRouter(prefix="/providers", tags=["Providers"])

def create_provider(session: Session, provider_data: dict):
    """Creates a new provider and saves it to the database"""
    new_provider = Provider(**provider_data)  # ✅ Unpack dictionary correctly
    session.add(new_provider)
    session.commit()
    session.refresh(new_provider)
    return new_provider

@router.post("/", response_model=ProviderSchema, summary="Create a new provider")
def create_provider_route(provider: ProviderSchema, db: Session = Depends(get_db)):
    """Create a new provider using provider schema"""
    return create_provider(db, provider.model_dump())  # ✅ Ensure model_dump() is used

@router.get("/{provider_id}", response_model=ProviderSchema, summary="Get a provider by ID")
def get_provider_route(provider_id: int, db: Session = Depends(get_db)):
    """Retrieve a provider by ID"""
    provider = get_provider(db, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider

@router.get("/", response_model=List[ProviderSchema], summary="Get all providers")
def get_all_providers_route(db: Session = Depends(get_db)):
    """Retrieve all providers"""
    return get_all_providers(db)

@router.put("/{provider_id}", response_model=ProviderSchema, summary="Update a provider")
def update_provider_route(provider_id: int, provider_data: ProviderSchema, db: Session = Depends(get_db)):
    """Update provider details"""
    updated_provider = update_provider(db, provider_id, provider_data)
    if not updated_provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return updated_provider

@router.delete("/{provider_id}", summary="Delete a provider")
def delete_provider_route(provider_id: int, db: Session = Depends(get_db)):
    """Delete a provider by ID"""
    deleted = delete_provider(db, provider_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Provider not found")
    return {"message": "Provider deleted successfully"}

@router.get("/{provider_id}/patients", summary="Get all patients assigned to a provider")
def get_patients_by_provider_route(provider_id: int, db: Session = Depends(get_db)):
    """Retrieve patients linked to a provider"""
    patients = get_patients_by_provider(db, provider_id)
    if patients is None or len(patients) == 0:
        raise HTTPException(status_code=404, detail="No patients found for this provider")
    return patients
