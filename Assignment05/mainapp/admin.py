from django.contrib import admin
from .models import Patient, Provider, Device, PatientProvider


class PatientProviderInline(admin.TabularInline):
    """
    Allows you to assign/unassign Providers to a Patient 
    by adding/removing rows in the PatientProvider table.
    Removing a row unassigns, but does NOT delete the Patient or the Provider.
    """
    model = PatientProvider
    extra = 1
    can_delete = True  # True means we can remove the join row (unassign). 
                       # It does NOT delete the Patient or Provider themselves.


class DeviceInline(admin.TabularInline):
    """
    Shows Devices linked to this Patient. 
    We do NOT allow deleting the Device object itself (can_delete = False).
    To unassign, change the 'patient' field to None.
    """
    model = Device
    extra = 1
    can_delete = False  # Prevents deleting the Device entirely.
    fields = ['serial_number', 'active', 'patient']
    # By exposing the 'patient' field, you can set it to 'None' 
    # to unassign the device from the patient. 


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """
    From the Patient detail page, you can:
      - Add/remove rows in the PatientProviderInline (assign/unassign Providers).
      - Edit each Device row to set 'patient' to None (unassign the device).
    """
    list_display = ('id', 'name', 'email', 'age', 'active')
    inlines = [PatientProviderInline, DeviceInline]


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'specialty')
    # to manage "which patients are assigned" from the Provider side,
    # similarly  can add a PatientProviderInline here too.


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'serial_number', 'active', 'patient')
    # edit a Device from here, can directly set/unset the 'patient' field.


@admin.register(PatientProvider)
class PatientProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'provider')

