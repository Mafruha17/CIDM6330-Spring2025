from rest_framework.viewsets import ModelViewSet
from mainapp.models import Provider
from mainapp.serializers import ProviderSerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from mainapp.models import Patient, PatientProvider
from mainapp.repositories.provider_repository import ProviderRepository

class ProviderViewSet(ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

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
