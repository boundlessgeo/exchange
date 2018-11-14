# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0005_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='custom_analytics',
            field=models.TextField(null=True, blank=True),
        ),
    ]
