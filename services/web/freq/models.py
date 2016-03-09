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
            old_priority = (FeatureRequest.objects
                    .only('priority')
                    .get(pk=self.pk)
                    .priority)
        except FeatureRequest.DoesNotExist:
            old_priority = None
        priority = self.priority
        self.priority = 0

        with transaction.atomic():
            super().save(*args, **kwargs)
            self.refresh_from_db()

            conditions = {
                'client': self.client,
                'priority__gte': priority
            }
            if old_priority is None:
                delta = 1
            elif old_priority > priority:
                conditions['priority__lte'] = old_priority
                delta = 1
            else:
                conditions['priority__lte'] = conditions['priority__gte']
                conditions['priority__gte'] = old_priority
                delta = -1
            shifters = FeatureRequest.objects.filter(**conditions)
            shifters.update(priority=F('priority') + delta)

            FeatureRequest.objects.filter(pk=self.pk).update(priority=priority)
            self.refresh_from_db()
