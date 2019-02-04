# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
        ('user_messages', '0002_auto_20180129_1516'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMemberThread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unread', models.BooleanField(default=True)),
                ('deleted', models.BooleanField(default=False)),
                ('group', models.ForeignKey(to='auth.Group')),
            ],
        ),
        migrations.RemoveField(
            model_name='thread',
            name='users',
        ),
        migrations.AddField(
            model_name='thread',
            name='single_users',
            field=models.ManyToManyField(related_name='single_threads', verbose_name='Users', to=settings.AUTH_USER_MODEL, through='user_messages.UserThread', blank=True),
        ),
        migrations.AlterField(
            model_name='userthread',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userthread',
            name='unread',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='groupmemberthread',
            name='thread',
            field=models.ForeignKey(to='user_messages.Thread'),
        ),
        migrations.AddField(
            model_name='groupmemberthread',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='thread',
            name='group_users',
            field=models.ManyToManyField(related_name='group_threads', verbose_name='Group Members', to=settings.AUTH_USER_MODEL, through='user_messages.GroupMemberThread', blank=True),
        ),
    ]
