# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("remoteservices", "0001_initial")
    ]

    def create_exchange_service(apps, schema_editor):
        RemoteService = apps.get_model("services", "service")
        ExchangeService = apps.get_model("remoteservices", "exchangeservice")
        for service in RemoteService.objects.all():
            exchange_service = ExchangeService(geonode_service=service)
            exchange_service.save()

    operations = [
        migrations.RunPython(create_exchange_service),
    ]
