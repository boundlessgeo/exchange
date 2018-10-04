from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

try:
    if 'ssl_pki' not in settings.INSTALLED_APPS:
        raise ImportError
    else:
        from ssl_pki.models import (
            uses_proxy_route,
            HostnamePortSslConfig
        )
except ImportError:
    uses_proxy_route = None
    HostnamePortSslConfig = None


@receiver(post_save, sender=HostnamePortSslConfig)
def update_use_proxy_basemap_layers(sender, **kwargs):
    for layer in settings.MAP_BASELAYERS:
        if (callable(uses_proxy_route) and
                "url" in layer["source"] and
                uses_proxy_route(layer["source"]["url"]) and
                settings.PROXY_BASEMAP is True):
            layer["source"]["use_proxy"] = True
