from django.db.models.signals import post_save
from django.dispatch import receiver
from mainapp.tasks import notify_new_patient_created
from .models import Patient

@receiver(post_save, sender=Patient)
def patient_created_signal(sender, instance, created, **kwargs):
    if created:
         # Call your Celery tasks
        notify_new_patient_created.delay(instance.id)

