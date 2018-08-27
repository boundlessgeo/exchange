# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0010_auto_20180125_1314'),
    ]

    def create_exchange_profiles(apps, schema_editor):
        ExchangeProfile = apps.get_model('core', 'ExchangeProfile')
        Profile = apps.get_model('people', 'Profile')
        for profile in Profile.objects.all():
            ep = ExchangeProfile.objects.create(user=profile)
            ep.save()

    operations = [
        migrations.CreateModel(
            name='ExchangeProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('content_creator', models.BooleanField(
                    default=True,
                    help_text='User can upload layers and documents',
                    verbose_name='Content Creator')),
                ('content_manager', models.BooleanField(
                    default=True,
                    help_text='User can register remote services',
                    verbose_name='Content Manager')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                           null=True)),
            ],
        ),
        migrations.RunPython(create_exchange_profiles)
    ]
