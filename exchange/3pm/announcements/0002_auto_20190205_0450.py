# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='dismissal_type',
            field=models.IntegerField(
                default=2,
                verbose_name='dismissal type',
                choices=[
                    (1, 'No Dismissals Allowed'),
                    (2, 'Session Only Dismissal'),
                    (3, 'Permanent Dismissal Allowed')
                ]
            ),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='level',
            field=models.IntegerField(
                default=1,
                verbose_name='level',
                choices=[(1, 'General'), (2, 'Warning'), (3, 'Critical')]
            ),
        ),
        migrations.AlterField(
            model_name='dismissal',
            name='announcement',
            field=models.ForeignKey(
                related_name='dismissals',
                verbose_name='announcement',
                to='announcements.Announcement'
            ),
        ),
        migrations.AlterField(
            model_name='dismissal',
            name='dismissed_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='dismissed at'),
        ),
        migrations.AlterField(
            model_name='dismissal',
            name='user',
            field=models.ForeignKey(
                related_name='announcement_dismissals',
                verbose_name='user',
                to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
