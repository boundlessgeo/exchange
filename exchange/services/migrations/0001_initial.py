# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0040_auto_20181018_1236'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('service_ptr',
                 models.OneToOneField(parent_link=True,
                                      auto_created=True,
                                      primary_key=True,
                                      serialize=False,
                                      to='services.Service')),
                ('classification', models.CharField(
                    max_length=255, null=True, blank=True)),
                ('provenance', models.CharField(
                    max_length=255, null=True, blank=True)),
                ('caveat', models.CharField(max_length=255,
                                            null=True, blank=True)),
                ('poc_name', models.CharField(max_length=255,
                                              null=True, blank=True)),
                ('poc_position', models.CharField(
                    max_length=255, null=True, blank=True)),
                ('poc_email', models.CharField(
                    max_length=255, null=True, blank=True)),
                ('poc_phone', models.CharField(
                    max_length=255, null=True, blank=True)),
                ('poc_address', models.CharField(
                    max_length=255, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('services.service',),
        ),
    ]
