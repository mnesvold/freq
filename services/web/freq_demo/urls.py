from django.conf.urls import url
from django.contrib import admin

from .admin import customize_admin

customize_admin()

urlpatterns = [
    url(r'^', admin.site.urls),
]
