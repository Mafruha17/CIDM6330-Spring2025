from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from database.connection import get_db
from schemas.provider import ProviderSchema
from database.crud.provider_crud import (
    create_provider, get_provider, get_all_providers, update_provider, delete_provider,
    get_patients_by_provider
)

router = APIRouter(prefix="/providers", tags=["Providers"])

@router.post("/", response_model=ProviderSchema, summary="Create a new provider")
def create_provider_route(provider: ProviderSchema, db: Session = Depends(get_db)):
    """Create a new provider"""
    return create_provider(db, provider)

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
