# ai_services/tests/test_gemini.py

from django.test import TestCase
from ninja.testing import TestClient
from mainapp.api import api  # Ensure this imports your NinjaAPI instance

class GeminiApiTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)

    def test_gemini_summary(self):
        """
        Simulates a patient note summary request via Gemini API.
        """
        response = self.client.post("/ai/summaries", {
            "text": "Patient is experiencing mild headaches and fatigue.",
            "language": "en"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("summary", response.json())

    def test_gemini_device_anomaly(self):
        """
        Simulates anomaly detection in device data using Gemini API.
        """
        response = self.client.post("/ai/device-anomalies", {
            "readings": [88, 86, 85, 63, 40, 39, 38]
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("anomaly", response.json())
        self.assertIsInstance(response.json()["anomaly"], bool)
