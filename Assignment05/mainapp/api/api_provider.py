
# mainapp/api/api_provider.py
from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from mainapp.models import Provider
from mainapp.schemas.provider_schema import ProviderIn, ProviderOut

router = Router()

@router.get("/", response=List[ProviderOut])
def list_providers(request):
    return Provider.objects.prefetch_related("patients").all()

@router.get("/{provider_id}", response=ProviderOut)
def get_provider(request, provider_id: int):
    return get_object_or_404(Provider.objects.prefetch_related("patients"), id=provider_id)

@router.post("/", response=ProviderOut)
def create_provider(request, data: ProviderIn):
    return Provider.objects.create(**data.dict())

@router.put("/{provider_id}", response=ProviderOut)
def update_provider(request, provider_id: int, data: ProviderIn):
    provider = get_object_or_404(Provider, id=provider_id)
    for field, value in data.dict().items():
        setattr(provider, field, value)
    provider.save()
    return provider

@router.delete("/{provider_id}")
def delete_provider(request, provider_id: int):
    provider = get_object_or_404(Provider, id=provider_id)
    provider.delete()
    return {"message": "Provider deleted"}
