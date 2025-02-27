from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.crud.provider_crud import (
    create_provider, get_provider, update_provider, delete_provider, get_patients_by_provider
)
from schemas.provider import ProviderSchema

router = APIRouter(prefix="/providers", tags=["Providers"])

# ✅ Create a new Provider
@router.post("/", response_model=ProviderSchema)
def create_provider_route(provider: ProviderSchema, db: Session = Depends(get_db)):
    return create_provider(db, provider)

# ✅ Get a Provider by ID
@router.get("/{provider_id}", response_model=ProviderSchema)
def get_provider_route(provider_id: int, db: Session = Depends(get_db)):
    provider = get_provider(db, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider

# ✅ Update a Provider
@router.put("/{provider_id}", response_model=ProviderSchema)
def update_provider_route(provider_id: int, provider_data: ProviderSchema, db: Session = Depends(get_db)):
    updated_provider = update_provider(db, provider_id, provider_data)
    if not updated_provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return updated_provider

# ✅ Delete a Provider (Only removes association, keeps Patients)
@router.delete("/{provider_id}")
def delete_provider_route(provider_id: int, db: Session = Depends(get_db)):
    if not delete_provider(db, provider_id):
        raise HTTPException(status_code=404, detail="Provider not found")
    return {"message": "Provider deleted successfully"}

# ✅ Get all Patients assigned to a Provider
@router.get("/{provider_id}/patients")
def get_patients(provider_id: int, db: Session = Depends(get_db)):
    patients = get_patients_by_provider(db, provider_id)
    if not patients:
        raise HTTPException(status_code=404, detail="No patients found for this provider")
    return patients
