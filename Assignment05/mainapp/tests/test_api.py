
from django.test import TestCase

class BasicAPITest(TestCase):
    def test_api_root(self):
        response = self.client.get("/api/patients/")
        self.assertIn(response.status_code, [200, 401, 403])

        response = self.client.get("/api/providers/")
        self.assertIn(response.status_code, [200, 401, 403])

        response = self.client.get("/api/devices/")
        self.assertIn(response.status_code, [200, 401, 403])