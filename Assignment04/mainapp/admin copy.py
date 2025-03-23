
from django.contrib import admin
from .models import Patient, Provider, Device, PatientProvider

class PatientProviderInline(admin.TabularInline):
    model = PatientProvider
    extra = 1  # How many empty slots to show by default for new entries
    can_delete = True  # default is True anyway

class DeviceInline(admin.TabularInline):
    model = Device
    extra = 1  # For creating new devices here if needed

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'age', 'active')
    inlines = [PatientProviderInline, DeviceInline]
    #inlines = [PatientProviderInline]  # Add the inline to the Patient admin


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'specialty')


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'serial_number', 'active', 'patient')


@admin.register(PatientProvider)
class PatientProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'provider')
  

