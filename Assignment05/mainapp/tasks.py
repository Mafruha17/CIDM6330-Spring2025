from celery import shared_task
from django.core.mail import send_mail

@shared_task
def notify_new_patient_created(patient_id):
    from mainapp.models import Patient  # imported here, inside the function

    try:
        patient = Patient.objects.get(id=patient_id)
        send_mail(
            subject="New Patient Created",
            message=f"Patient {patient.name} with ID {patient.id} was created.",
            from_email="noreply@myclinic.org",
            recipient_list=["admin@myclinic.org"],
        )
    except Patient.DoesNotExist:
        pass
