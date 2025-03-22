
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from mainapp.models import Patient
from mainapp.models import Provider, PatientProvider
from mainapp.serializers import PatientSerializer
from mainapp.repositories.patient_repository import PatientRepository



class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    @action(detail=True, methods=['post'], url_path='assign_provider')
    def assign_provider(self, request, pk=None):
        patient = PatientRepository.get_by_id(pk)
        provider_id = request.data.get('provider_id')

        if not provider_id:
            return Response({"error": "Missing provider_id"}, status=status.HTTP_400_BAD_REQUEST)

        provider = Provider.objects.filter(id=provider_id).first()
        if not provider:
            return Response({"error": "Provider not found"}, status=status.HTTP_404_NOT_FOUND)

        PatientProvider.objects.get_or_create(patient=patient, provider=provider)
        return Response({"message": "Provider assigned successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='remove_provider')
    def remove_provider(self, request, pk=None):
        patient = PatientRepository.get_by_id(pk)
        provider_id = request.data.get('provider_id')

        if not provider_id:
            return Response({"error": "Missing provider_id"}, status=status.HTTP_400_BAD_REQUEST)

        provider = Provider.objects.filter(id=provider_id).first()
        if not provider:
            return Response({"error": "Provider not found"}, status=status.HTTP_404_NOT_FOUND)

        deleted, _ = PatientProvider.objects.filter(patient=patient, provider=provider).delete()
        if deleted:
            return Response({"message": "Provider removed."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No such provider assignment."}, status=status.HTTP_404_NOT_FOUND)
