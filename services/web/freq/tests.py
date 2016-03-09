from django.core.exceptions import ValidationError
from django.test import TestCase

from freq.models import Client, ProductArea, FeatureRequest

class ModelTests(TestCase):
    def setUp(self):
        self.dummy_client = Client.objects.create(title='Anodyne Industries')
        self.dummy_area = ProductArea.objects.create(title='Reports')

    def test_priority_collision_new(self):
        originals = (self._create_request(1), self._create_request(2))
        collision = self._create_request(1)

        tuple(o.refresh_from_db() for o in originals)
        collision.refresh_from_db()

        self.assertEqual(originals[0].priority, 2)
        self.assertEqual(originals[1].priority, 3)
        self.assertEqual(collision.priority, 1)

    def test_priority_collision_higher_priority(self):
        originals = tuple(self._create_request(p + 1) for p in range(5))

        # sanity check
        priorities = tuple(o.priority for o in originals)
        self.assertEqual(priorities, (1, 2, 3, 4, 5))

        originals[3].priority = 1
        originals[3].save()

        tuple(o.refresh_from_db() for o in originals)

        priorities = tuple(o.priority for o in originals)
        self.assertEqual(priorities, (2, 3, 4, 1, 5))

    def test_priority_collision_lower_priority(self):
        originals = tuple(self._create_request(p + 1) for p in range(5))

        # sanity check
        priorities = tuple(o.priority for o in originals)
        self.assertEqual(priorities, (1, 2, 3, 4, 5))

        originals[1].priority = 4
        originals[1].save()

        tuple(o.refresh_from_db() for o in originals)

        priorities = tuple(o.priority for o in originals)
        self.assertEqual(priorities, (1, 4, 2, 3, 5))

    def _create_request(self, priority):
        n = FeatureRequest.objects.count()
        return FeatureRequest.objects.create(
                title='Request #%d' % (n + 1,),
                client=self.dummy_client,
                priority=priority,
                product_area=self.dummy_area)
