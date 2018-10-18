from django.conf.urls import url

from exchange.services import views
from geonode.services.urls import urlpatterns as geonode_services_urls

urlpatterns = [url(r'^(?P<service_id>\d+)/edit$',
                   views.edit_service, name='edit_service')]
urlpatterns += geonode_services_urls
