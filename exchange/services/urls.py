from django.conf.urls import url
from geonode.services.urls import urlpatterns

from exchange.services import views

urlpatterns = [url(r'^(?P<service_id>\d+)/edit$', views.edit_service, name='edit_service')] + urlpatterns
