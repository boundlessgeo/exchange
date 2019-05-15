# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_messages', '0003_auto_20190419_1024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupmemberthread',
            name='group',
        ),
        migrations.RemoveField(
            model_name='groupmemberthread',
            name='thread',
        ),
        migrations.RemoveField(
            model_name='groupmemberthread',
            name='user',
        ),
        migrations.RemoveField(
            model_name='thread',
            name='group_users',
        ),
        migrations.RemoveField(
            model_name='thread',
            name='single_users',
        ),
        migrations.AddField(
            model_name='thread',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL,
                                         verbose_name='Users',
                                         through='user_messages.UserThread'),
        ),
        migrations.AlterField(
            model_name='userthread',
            name='deleted',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='userthread',
            name='unread',
            field=models.BooleanField(),
        ),
        migrations.DeleteModel(
            name='GroupMemberThread',
        ),
    ]
