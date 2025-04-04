from django.test import TestCase
from mainapp.models import Device, Patient

class DeviceAPITest(TestCase):
    def setUp(self):
        self.base_url = "/api/devices/"
        self.patient = Patient.objects.create(name="Jane Doe", email="jane@example.com", age=25)
        self.device_data = {
            "serial_number": "ABC123",
            "patient_id": self.patient.id,
            "active": True
        }

    def test_create_device(self):
        response = self.client.post(self.base_url, self.device_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Device.objects.count(), 1)

    def test_assign_unassign_device(self):
        device = Device.objects.create(serial_number="XYZ789")
        assign_url = f"{self.base_url}{device.id}/assign/?patient_id={self.patient.id}"
        unassign_url = f"{self.base_url}{device.id}/unassign/"

        assign_resp = self.client.post(assign_url)
        self.assertEqual(assign_resp.status_code, 200)
        self.assertEqual(assign_resp.json()["patient_id"], self.patient.id)

        unassign_resp = self.client.post(unassign_url)
        self.assertEqual(unassign_resp.status_code, 200)
        self.assertIsNone(unassign_resp.json()["patient_id"])
