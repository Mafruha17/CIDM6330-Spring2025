from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from models import Provider
from schemas.provider import ProviderSchema  # Import corrected schema

router = APIRouter()

@router.post("/", response_model=ProviderSchema)
def create_provider(provider: ProviderSchema, db: Session = Depends(get_db)):
    """Create a new provider"""
    new_provider = Provider(
        name=provider.name,
        email=provider.email,
        specialty=provider.specialty
    )
    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)  # Ensure the ID is returned properly
    return new_provider


@router.get("/{provider_id}", response_model=ProviderSchema)
def get_provider(provider_id: int, db: Session = Depends(get_db)):
    """Retrieve a provider by ID"""
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider


@router.put("/{provider_id}", response_model=ProviderSchema)
def update_provider(provider_id: int, provider_update: ProviderSchema, db: Session = Depends(get_db)):
    """Update an existing provider"""
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    # Update fields only if they are provided
    provider.name = provider_update.name or provider.name
    provider.email = provider_update.email or provider.email
    provider.specialty = provider_update.specialty or provider.specialty

    db.commit()
    db.refresh(provider)
    return provider


@router.delete("/{provider_id}")
def delete_provider(provider_id: int, db: Session = Depends(get_db)):
    """Delete a provider by ID"""
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    db.delete(provider)
    db.commit()
    return {"message": "Deleted"}
