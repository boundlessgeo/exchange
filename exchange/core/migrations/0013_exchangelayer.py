# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '0031_constraint'),
        ('remoteservices', '0001_initial'),
        ('core', '0012_adds_content_creator_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeLayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('exchange_service', models.ForeignKey(
                    blank=True, to='remoteservices.ExchangeService',
                    null=True)),
                ('geonode_layer', models.OneToOneField(to='layers.Layer')),
            ],
        ),
    ]
