from django.shortcuts import render
from mainapp.models import Patient, Provider, Device

def dashboard_view(request):
    context = {
        "total_patients": Patient.objects.count(),
        "total_providers": Provider.objects.count(),
        "total_devices": Device.objects.count(),
    }
    return render(request, "dashboard/dashboard.html", context)

