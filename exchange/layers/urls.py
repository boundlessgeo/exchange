from django.conf.urls import patterns, url
from .views import layer_update_bounds

urlpatterns = [
    url(r'^layers/(?P<layername>[^/]*)/recalculate$', layer_update_bounds, name="layer_recalculate_bound"),
]
