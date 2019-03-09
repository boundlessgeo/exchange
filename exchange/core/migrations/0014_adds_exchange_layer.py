# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0013_exchangelayer"),
        ('remoteservices', '0001_initial'),
    ]

    def create_exchange_layer(apps, schema_editor):
        GeoNodeLayer = apps.get_model("layers", "Layer")
        ExchangeLayer = apps.get_model("core", "exchangelayer")
        ExchangeService = apps.get_model("remoteservices", "exchangeservice")
        for layer in GeoNodeLayer.objects.all():
            if layer.service is not None:
                exchange_layer = ExchangeLayer(geonode_layer=layer)
                exchange_layer.exchange_service = ExchangeService.objects.get(
                    geonode_service=layer.service)
                exchange_layer.save()

    operations = [
        migrations.RunPython(create_exchange_layer),
    ]
