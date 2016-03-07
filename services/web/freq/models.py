from django.core.validators import MinValueValidator
from django.db import models

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
        unique_together = ('client', 'priority')

    def __str__(self):
        return self.title
