from django.test import TestCase
from django.urls import reverse
from mainapp.models import Patient

class PatientAPITest(TestCase):
    def setUp(self):
        self.base_url = "/api/patients/"
        self.patient_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30,
            "active": True
        }

    def test_create_patient(self):
        response = self.client.post(self.base_url, self.patient_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Patient.objects.count(), 1)

    def test_list_patients(self):
        Patient.objects.create(**self.patient_data)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
