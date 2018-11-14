# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20180125_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cswrecord',
            name='classification',
            field=models.CharField(
                blank=True,
                max_length=128,
                choices=[
                    (b'sample 2', b'sample 2'),
                    (b'sample 3', b'sample 3'),
                    (b'sample 1', b'sample 1')]),
        ),
        migrations.AlterField(
            model_name='cswrecord',
            name='releasability',
            field=models.CharField(max_length=128, blank=True),
        ),
    ]
