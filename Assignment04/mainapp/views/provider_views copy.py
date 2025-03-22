from rest_framework import viewsets, status
from rest_framework.response import Response
from mainapp.serializers import ProviderSerializer
from rest_framework.decorators import action
from mainapp.models import Patient, PatientProvider
from mainapp.repositories.provider_repository import ProviderRepository

class ProviderViewSet(viewsets.ViewSet):
    def list(self, request):
        providers = ProviderRepository.get_all()
        serializer = ProviderSerializer(providers, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        provider = ProviderRepository.get_by_id(pk)
        serializer = ProviderSerializer(provider)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProviderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = ProviderRepository.create(serializer.validated_data)
        return Response(ProviderSerializer(provider).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        provider = ProviderRepository.get_by_id(pk)
        serializer = ProviderSerializer(provider, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_provider = ProviderRepository.update(provider, serializer.validated_data)
        return Response(ProviderSerializer(updated_provider).data)

    def destroy(self, request, pk=None):
        provider = ProviderRepository.get_by_id(pk)
        ProviderRepository.delete(provider)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # ... Extended CRUD methods ...

    @action(detail=True, methods=['post'], url_path='assign_patient')
    def assign_patient(self, request, pk=None):
        provider = ProviderRepository.get_by_id(pk)
        patient_id = request.data.get("patient_id")

        if not patient_id:
            return Response({"error": "Missing patient_id"}, status=status.HTTP_400_BAD_REQUEST)

        patient = Patient.objects.filter(id=patient_id).first()
        if not patient:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        PatientProvider.objects.get_or_create(patient=patient, provider=provider)
        return Response({"message": "Patient assigned to provider."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='remove_patient')
    def remove_patient(self, request, pk=None):
        provider = ProviderRepository.get_by_id(pk)
        patient_id = request.data.get("patient_id")

        if not patient_id:
            return Response({"error": "Missing patient_id"}, status=status.HTTP_400_BAD_REQUEST)

        patient = Patient.objects.filter(id=patient_id).first()
        if not patient:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        deleted, _ = PatientProvider.objects.filter(patient=patient, provider=provider).delete()
        if deleted:
            return Response({"message": "Patient removed from provider."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No such patient assignment."}, status=status.HTTP_404_NOT_FOUND)
