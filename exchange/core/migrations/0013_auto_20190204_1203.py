# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import exchange.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_adds_content_creator_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thumbnailimage',
            name='thumbnail_image',
            field=models.ImageField(
                upload_to=exchange.core.models.get_thumb_image_path),
        ),
    ]
