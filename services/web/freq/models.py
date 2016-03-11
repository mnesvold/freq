from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.db.models import F

__all__ = ('Client', 'FeatureRequest', 'ProductArea')

class Client(models.Model):
    title = models.CharField(max_length=128, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

class ProductArea(models.Model):
    title = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

class FeatureRequest(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    client = models.ForeignKey(Client, models.CASCADE)
    priority = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    target_date = models.DateField(blank=True, null=True)
    url = models.URLField(blank=True, verbose_name='URL')
    product_area = models.ForeignKey(ProductArea, models.PROTECT)

    class Meta:
        ordering = ('priority', 'client')
#       This uniqueness constraint is *NOT* enforced at the database level!
#       Asking the database to enforce this constraint seems to break the bulk
#       updates on `priority` when shifting records around.
#       unique_together = ('client', 'priority')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            old_req = (FeatureRequest.objects
                    .only('priority', 'client')
                    .get(pk=self.pk))
        except FeatureRequest.DoesNotExist:
            old_client = old_priority = None
        else:
            old_priority = old_req.priority
            old_client = old_req.client
        priority = self.priority
        self.priority = 0
        client = self.client

        with transaction.atomic():
            super().save(*args, **kwargs)
            self.refresh_from_db()

            if old_client and old_client != client:
                self._shift_priorities(old_client, old_priority, None, -1)
                self._shift_priorities(client, priority, None, 1)
            elif old_priority is None:
                self._shift_priorities(client, priority, None, 1)
            elif old_priority > priority:
                self._shift_priorities(client, priority, old_priority, 1)
            else:
                self._shift_priorities(client, old_priority, priority, -1)

            FeatureRequest.objects.filter(pk=self.pk).update(priority=priority)
            self.refresh_from_db()

    def delete(self, *args, **kwargs):
        priority = self.priority
        client = self.client
        with transaction.atomic():
            super().delete(*args, **kwargs)
            self._shift_priorities(client, priority, None, -1)

    def _shift_priorities(self, client, gte, lte, delta):
        conditions = {
            'client': client,
            'priority__gte': gte,
        }
        if lte is not None:
            conditions['priority__lte'] = lte
        reqs = FeatureRequest.objects.filter(**conditions)
        reqs.update(priority=F('priority') + delta)
