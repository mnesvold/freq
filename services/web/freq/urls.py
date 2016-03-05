from django.conf.urls import url

from freq import views

urlpatterns = [
   url('^$', views.index),
]
