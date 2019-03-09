# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.management import update_contenttypes
from django.apps import apps as django_apps
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0007_auto_20170809_1750'),
    ]

    def update_all_contenttypes(apps, schema_editor):
        for app_config in django_apps.get_app_configs():
            update_contenttypes(app_config)

    def create_group(apps, schema_editor):
        AuthGroup = apps.get_model("auth", "group")
        ContentType = apps.get_model("contenttypes", "contenttype")
        Permission = apps.get_model("auth", "permission")

        # Create the group
        AuthGroup(name='csw_manager').save()
        group = AuthGroup.objects.get(name='csw_manager')
        content_type = ContentType.objects.get(
            app_label='services', model='service')
        permissions = Permission.objects.filter(
            content_type=content_type)

        # Assign the permissions
        for perm in permissions:
            group.permissions.add(perm)

    operations = [
        migrations.RunPython(update_all_contenttypes),
        migrations.RunPython(create_group),
    ]
