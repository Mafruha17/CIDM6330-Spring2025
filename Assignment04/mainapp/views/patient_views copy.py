from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from mainapp.models import Provider, PatientProvider
from mainapp.serializers import PatientSerializer
from mainapp.repositories.patient_repository import PatientRepository


class PatientViewSet(viewsets.ViewSet):
    def list(self, request):
        patients = PatientRepository.get_all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        patient = PatientRepository.get_by_id(pk)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    def create(self, request):
        serializer = PatientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = PatientRepository.create(serializer.validated_data)
        return Response(PatientSerializer(patient).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        patient = PatientRepository.get_by_id(pk)
        serializer = PatientSerializer(patient, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_patient = PatientRepository.update(patient, serializer.validated_data)
        return Response(PatientSerializer(updated_patient).data)

    def destroy(self, request, pk=None):
        patient = PatientRepository.get_by_id(pk)
        PatientRepository.delete(patient)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    ######### 

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

