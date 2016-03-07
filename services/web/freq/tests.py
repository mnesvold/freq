from django.core.exceptions import ValidationError
from django.test import TestCase

from freq.models import Client, ProductArea, FeatureRequest

class ModelTests(TestCase):
    def setUp(self):
        self.dummy_client = Client.objects.create(title='Anodyne Industries')
        self.dummy_area = ProductArea.objects.create(title='Reports')

    def test_min_priority(self):
        with self.assertRaises(ValidationError):
            req = FeatureRequest.objects.create(
                    title='Implement feature',
                    client=self.dummy_client,
                    priority=0,
                    product_area=self.dummy_area)
            req.full_clean()
