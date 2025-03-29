from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from mainapp.models import Device, Patient
from mainapp.serializers import DeviceSerializer
from mainapp.repositories.device_repository import DeviceRepository


class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    @action(detail=True, methods=['post'], url_path='assign')
    def assign_to_patient(self, request, pk=None):
        device = self.get_object()
        patient_id = request.data.get('patient_id')
        if not patient_id:
            return Response({"error": "Missing patient_id"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            patient = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        # Assign device to this patient
        device.patient = patient
        device.save()
        return Response(DeviceSerializer(device).data, status=status.HTTP_200_OK)
   
    @action(detail=True, methods=['post'], url_path='unassign')
    def unassign_from_patient(self, request, pk=None):
        device = self.get_object()
        device.patient = None
        device.save()
        return Response(DeviceSerializer(device).data, status=status.HTTP_200_OK)