# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0030_auto_20171212_0518'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('poc_name', models.CharField(max_length=255, null=True,
                                              blank=True)),
                ('poc_position', models.CharField(max_length=255, null=True,
                                                  blank=True)),
                ('poc_email', models.CharField(max_length=255, null=True,
                                               blank=True)),
                ('poc_phone', models.CharField(max_length=255, null=True,
                                               blank=True)),
                ('poc_address', models.CharField(max_length=255, null=True,
                                                 blank=True)),
                ('geonode_service', models.OneToOneField(
                    to='services.Service')),
            ],
        ),
    ]
