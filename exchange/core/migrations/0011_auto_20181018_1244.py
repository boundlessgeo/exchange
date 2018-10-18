# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20180125_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thumbnailimage',
            name='thumbnail_image',
            field=models.ImageField(upload_to=b'/uploaded/thumbs'),
        ),
    ]
