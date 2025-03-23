from django.db import models
from django.core.exceptions import ValidationError


class Patient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Provider(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    specialty = models.CharField(max_length=100)
    
    # New: ManyToManyField that uses your join model
    patients = models.ManyToManyField(
        'Patient',                  # or Patient if it's already defined above
        through='PatientProvider',  # reference your join table
        related_name='providers',   # so Patient can do .providers
        blank=True
    )

    def __str__(self):
        return self.name


class Device(models.Model):
    serial_number = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='devices'
    )

    def delete(self, *args, **kwargs):
        if self.patient is not None:
            raise ValidationError("Cannot delete a device assigned to a patient.")
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Device {self.serial_number}"


class PatientProvider(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('patient', 'provider')

    def __str__(self):
        return f"{self.patient} ↔ {self.provider}"

# Create your models here.
