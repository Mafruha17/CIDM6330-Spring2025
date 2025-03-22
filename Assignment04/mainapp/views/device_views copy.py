from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from mainapp.models import Patient, Device
from mainapp.serializers import DeviceSerializer
from mainapp.repositories.device_repository import DeviceRepository


class DeviceViewSet(viewsets.ViewSet):
    def list(self, request):
        devices = DeviceRepository.get_all()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        device = DeviceRepository.get_by_id(pk)
        serializer = DeviceSerializer(device)
        return Response(serializer.data)

    def create(self, request):
        serializer = DeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        device = DeviceRepository.create(serializer.validated_data)
        return Response(DeviceSerializer(device).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        device = DeviceRepository.get_by_id(pk)
        serializer = DeviceSerializer(device, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_device = DeviceRepository.update(device, serializer.validated_data)
        return Response(DeviceSerializer(updated_device).data)

    def destroy(self, request, pk=None):
        device = DeviceRepository.get_by_id(pk)
        if device.patient:
            return Response(
                {"error": "Cannot delete a device assigned to a patient."},
                status=status.HTTP_400_BAD_REQUEST
            )
        DeviceRepository.delete(device)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'], url_path='assign')
    def assign_to_patient(self, request, pk=None):
        device = DeviceRepository.get_by_id(pk)
        patient_id = request.data.get('patient_id')

        if not patient_id:
            return Response({"error": "Missing patient_id"}, status=status.HTTP_400_BAD_REQUEST)

        patient = Patient.objects.filter(id=patient_id).first()
        if not patient:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        device.patient = patient
        device.save()
        return Response(DeviceSerializer(device).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='unassign')
    def unassign_from_patient(self, request, pk=None):
        device = DeviceRepository.get_by_id(pk)
        device.patient = None
        device.save()
        return Response(DeviceSerializer(device).data, status=status.HTTP_200_OK)