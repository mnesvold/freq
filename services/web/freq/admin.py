from django.contrib import admin

from freq.models import *

admin.site.register(Client)
admin.site.register(ProductArea)

@admin.register(FeatureRequest)
class FeatureRequestAdmin(admin.ModelAdmin):
    date_hierarchy = 'target_date'
    list_display = ('title', 'client', 'priority', 'target_date',
            'product_area')
    list_filter = ('client', 'product_area')
    search_fields = ('title', 'description', 'url')
