# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from ..pki.migrate_data import migrate_pki_data


class Migration(migrations.Migration):

    dependencies = [
        ('ssl_pki', '0002_default_config'),
    ]

    operations = [
        migrations.RunPython(migrate_pki_data, migrations.RunPython.noop),
    ]
