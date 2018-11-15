# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20181022_1413'),
    ]

    def change_name(apps, schema_editor):
        AuthGroup = apps.get_model("auth", "group")

        # Changing terminology: csw_manager -> service_manager
        group = AuthGroup.objects.get(name='csw_manager')
        group.name = 'service_manager'
        group.save()

    def create_group(apps, schema_editor):
        AuthGroup = apps.get_model("auth", "group")
        ContentType = apps.get_model("contenttypes", "contenttype")
        Permission = apps.get_model("auth", "permission")

        # Create the group
        AuthGroup(name='content_creator').save()
        group = AuthGroup.objects.get(name='content_creator')

        # Add layer, document, and map
        # Layer
        content_type = ContentType.objects.get(
            app_label='layers', model='layer')
        permissions = Permission.objects.filter(
            content_type=content_type)

        # Assign the permissions
        for perm in permissions:
            group.permissions.add(perm)

        # Map
        content_type = ContentType.objects.get(
            app_label='maps', model='map')
        permissions = Permission.objects.filter(
            content_type=content_type)

        # Assign the permissions
        for perm in permissions:
            group.permissions.add(perm)

        # Document
        content_type = ContentType.objects.get(
            app_label='documents', model='document')
        permissions = Permission.objects.filter(
            content_type=content_type)

        # Assign the permissions
        for perm in permissions:
            group.permissions.add(perm)

    def add_default_group_permissions(apps, schema_editor):
        AuthGroup = apps.get_model("auth", "group")
        Profile = apps.get_model("people", "Profile")
        all_users = [profile for profile in Profile.objects.all()
                     if profile.is_staff is False and
                     profile.is_superuser is False and
                     profile.username != 'AnonymousUser']

        # Adding the default auth groups to all users
        for user in all_users:
            for group_name in settings.DEFAULT_USER_AUTH_GROUPS:
                auth_group = AuthGroup.objects.get(name=group_name)
                user.groups.add(auth_group)

    operations = [
        migrations.RunPython(create_group),
        migrations.RunPython(change_name),
        migrations.RunPython(add_default_group_permissions)
    ]
