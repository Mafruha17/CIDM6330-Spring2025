from sqlalchemy.orm import Session
from database.models import Provider, patient_provider_association
from schemas.provider import ProviderSchema

# ✅ Create a new provider
def create_provider(db: Session, provider: ProviderSchema):
    new_provider = Provider(**provider.dict())
    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)
    return new_provider

# ✅ Get a provider by ID
def get_provider(db: Session, provider_id: int):
    return db.query(Provider).filter(Provider.id == provider_id).first()
# ✅ Update an existing provider (No patient association needed)
def update_provider(db: Session, provider_id: int, provider_data: ProviderSchema):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    
    if not provider:
        return None  # Provider not found

    for key, value in provider_data.model_dump(exclude_unset=True).items():
        setattr(provider, key, value)

    db.commit()
    db.refresh(provider)
    return provider

# ✅ Delete a provider (Removes association, keeps patients)
def delete_provider(db: Session, provider_id: int):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if provider:
        db.query(patient_provider_association).filter(
            patient_provider_association.c.provider_id == provider_id
        ).delete()

        db.delete(provider)
        db.commit()
        return True
    return False

# ✅ Get all patients assigned to a provider
def get_patients_by_provider(db: Session, provider_id: int):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    return provider.patients if provider else None
