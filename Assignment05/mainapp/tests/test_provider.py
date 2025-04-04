from django.test import TestCase
from mainapp.models import Provider

class ProviderAPITest(TestCase):
    def setUp(self):
        self.base_url = "/api/providers/"
        self.provider_data = {
            "name": "Dr. Smith",
            "email": "smith@example.com",
            "specialty": "Cardiology"
        }

    def test_create_provider(self):
        response = self.client.post(self.base_url, self.provider_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Provider.objects.count(), 1)

    def test_list_providers(self):
        Provider.objects.create(**self.provider_data)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
