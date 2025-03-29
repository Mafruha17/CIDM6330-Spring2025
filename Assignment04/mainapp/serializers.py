from rest_framework import serializers
from .models import Patient, Provider, Device, PatientProvider


class DeviceSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()  # shows patient's name if assigned

    class Meta:
        model = Device
        fields = ['id', 'serial_number', 'active', 'patient']


class SimpleProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['id', 'name', 'email', 'specialty']


class SimpleDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'serial_number', 'active']


class PatientSerializer(serializers.ModelSerializer):
    devices = SimpleDeviceSerializer(many=True, read_only=True)
    providers = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ['id', 'name', 'email', 'age', 'active', 'devices', 'providers']

    def get_providers(self, obj):
        patient_providers = PatientProvider.objects.filter(patient=obj)
        providers = [pp.provider for pp in patient_providers]
        return SimpleProviderSerializer(providers, many=True).data
    

class ProviderSerializer(serializers.ModelSerializer):
    # 1. This field allows adding/removing patient IDs
    #    on PUT/PATCH, e.g. "patient_ids": [1, 2]
    patient_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Patient.objects.all(),
        source='patients'   # Tells DRF this field maps to the 'patients' M2M
    )

    # 2. This field just reads the current patients in a friendly format
    patient_details = serializers.SerializerMethodField()

    class Meta:
        model = Provider
        fields = ['id', 'name', 'email', 'specialty', 'patient_ids', 'patient_details']

    def get_patient_details(self, obj):
        # Reuse your old logic or do a nested serializer
        patient_providers = PatientProvider.objects.filter(provider=obj)
        patients = [pp.patient for pp in patient_providers]
        return [str(p) for p in patients]  
        # or use a custom serializer, e.g. PatientSerializer(patients, many=True).data

class PatientProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProvider
        fields = ['id', 'patient', 'provider']
