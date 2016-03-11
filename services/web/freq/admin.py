from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from freq.models import *

admin.site.register(Client)
admin.site.register(ProductArea)

class FeatureRequestAdminForm(ModelForm):
    def clean_priority(self):
        priority = self.cleaned_data['priority']
        if priority < 1:
            raise ValidationError(
                    _('Priority values must be positive.'),
                    code='invalid')
        client = self.cleaned_data['client']
        req_count = FeatureRequest.objects.filter(client=client).count()
        if not self.instance.pk:
            req_count += 1
        if priority > req_count:
            raise ValidationError(
                    _('This client only has %(count)s feature request(s);'
                      ' priority values may not exceed that number.'),
                    code='invalid',
                    params={'count': req_count})
        return priority

@admin.register(FeatureRequest)
class FeatureRequestAdmin(admin.ModelAdmin):
    date_hierarchy = 'target_date'
    form = FeatureRequestAdminForm
    list_display = ('title', 'client', 'priority', 'target_date',
            'product_area')
    list_filter = ('client', 'product_area')
    search_fields = ('title', 'description', 'url')
