from django.core.exceptions import ValidationError
from django.test import TestCase

from freq.models import Client, ProductArea, FeatureRequest

class ModelTests(TestCase):
    def setUp(self):
        self.dummy_client = Client.objects.create(title='Anodyne Industries')
        self.dummy_area = ProductArea.objects.create(title='Reports')

    def test_priority_collision_new(self):
        originals = self._create_requests(2)
        collision = self._create_request(1)

        tuple(o.refresh_from_db() for o in originals)
        collision.refresh_from_db()

        self.assertEqual(originals[0].priority, 2)
        self.assertEqual(originals[1].priority, 3)
        self.assertEqual(collision.priority, 1)

    def test_priority_collision_higher_priority(self):
        originals = self._create_requests(5)

        # sanity check
        priorities = self._priorities_of(originals)
        self.assertEqual(priorities, (1, 2, 3, 4, 5))

        originals[3].priority = 1
        originals[3].save()

        self._refresh(originals)

        priorities = self._priorities_of(originals)
        self.assertEqual(priorities, (2, 3, 4, 1, 5))

    def test_priority_collision_lower_priority(self):
        originals = self._create_requests(5)

        # sanity check
        priorities = self._priorities_of(originals)
        self.assertEqual(priorities, (1, 2, 3, 4, 5))

        originals[1].priority = 4
        originals[1].save()

        self._refresh(originals)

        priorities = self._priorities_of(originals)
        self.assertEqual(priorities, (1, 4, 2, 3, 5))

    def test_priority_on_delete(self):
        requests = self._create_requests(5)
        requests[2].delete()
        requests[2] = None

        self._refresh(requests)

        priorities = self._priorities_of(requests)
        self.assertEqual(priorities, (1, 2, None, 3, 4))

    def test_priority_change_client(self):
        a_client = self.dummy_client
        b_client = Client.objects.create(title='Banana Corp.')
        a_reqs = self._create_requests(5, a_client)
        b_reqs = self._create_requests(5, b_client)

        # sanity check
        self._refresh(a_reqs)
        self.assertEqual(self._priorities_of(a_reqs), (1, 2, 3, 4, 5))
        self.assertEqual(self._priorities_of(b_reqs), (1, 2, 3, 4, 5))

        a_reqs[2].client = b_client
        a_reqs[2].save()

        self._refresh(a_reqs)
        self._refresh(b_reqs)

        self.assertEqual(self._priorities_of(a_reqs), (1, 2, 3, 3, 4))
        self.assertEqual(self._priorities_of(b_reqs), (1, 2, 4, 5, 6))

    def test_priority_change_client_and_priority(self):
        a_client = self.dummy_client
        b_client = Client.objects.create(title='Banana Corp.')
        a_reqs = self._create_requests(5, a_client)
        b_reqs = self._create_requests(5, b_client)

        a_reqs[1].client = b_client
        a_reqs[1].priority = 4
        a_reqs[1].save()

        self._refresh(a_reqs)
        self._refresh(b_reqs)

        self.assertEqual(self._priorities_of(a_reqs), (1, 4, 2, 3, 4))
        self.assertEqual(self._priorities_of(b_reqs), (1, 2, 3, 5, 6))

    def _create_request(self, priority, client=None):
        client = client or self.dummy_client
        n = FeatureRequest.objects.count()
        return FeatureRequest.objects.create(
                title='Request #%d' % (n + 1,),
                client=client,
                priority=priority,
                product_area=self.dummy_area)

    def _create_requests(self, n, client=None):
        return [self._create_request(p + 1, client) for p in range(n)]

    def _refresh(self, reqs):
        tuple(r.refresh_from_db() for r in reqs if r)

    def _priorities_of(self, reqs):
        return tuple(r.priority if r else None for r in reqs)
