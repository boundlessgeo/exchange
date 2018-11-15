# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('base', '24_to_26'),
        ('core', '0008_adds_content_manager_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='cswrecord',
            name='contact_address',
            field=models.CharField(max_length=128, blank=True),
        ),
        migrations.AddField(
            model_name='cswrecord',
            name='contact_address_type',
            field=models.CharField(
                blank=True, max_length=128, choices=[
                    (b'Physical', b'Physical'), (b'Postal', b'Postal')]),
        ),
        migrations.AddField(
            model_name='cswrecord',
            name='contact_city',
            field=models.CharField(max_length=128, blank=True),
        ),
        migrations.AddField(
            model_name='cswrecord',
            name='contact_country',
            field=models.CharField(max_length=128, blank=True),
        ),
        migrations.AddField(
            model_name='cswrecord',
            name='contact_position',
            field=models.CharField(max_length=128, blank=True),
        ),
        migrations.AddField(
            model_name='cswrecord',
            name='contact_state',
            field=models.CharField(max_length=2, blank=True),
        ),
        migrations.AddField(
            model_name='cswrecord',
            name='contact_zip',
            field=models.CharField(max_length=128, blank=True),
        ),
        migrations.AddField(
            model_name='cswrecord',
            name='created',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='cswrecord',
            name='fees',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='cswrecord',
            name='keywords',
            field=models.CharField(max_length=128, blank=True),
        ),
        migrations.AddField(
            model_name='cswrecord',
            name='license',
            field=models.ForeignKey(
                blank=True, to='base.License',
                help_text=b'License of the dataset',
                null=True, verbose_name=b'License'),
        ),
        migrations.AddField(
            model_name='cswrecord',
            name='maintenance_frequency',
            field=models.CharField(
                choices=[
                    (b'unknown',
                     'frequency of maintenance for the data is not known'),
                    (b'continual',
                     'data is repeatedly and frequently updated'),
                    (b'notPlanned',
                     'there are no plans to update the data'),
                    (b'daily', 'data is updated each day'),
                    (b'annually', 'data is updated every year'),
                    (b'asNeeded', 'data is updated as deemed necessary'),
                    (b'monthly', 'data is updated each month'),
                    (b'fortnightly', 'data is updated every two weeks'),
                    (b'irregular',
                     'data is updated in intervals that are uneven '
                     'in duration'),
                    (b'weekly', 'data is updated on a weekly basis'),
                    (b'biannually', 'data is updated twice each year'),
                    (b'quarterly', 'data is updated every three months')],
                max_length=255, blank=True,
                help_text=b'Frequency with which modifications and deletions '
                          b'are made to the data after it is first produced',
                null=True, verbose_name=b'maintenance frequency'),
        ),
        migrations.AddField(
            model_name='cswrecord',
            name='provenance',
            field=models.CharField(
                blank=True, max_length=100,
                choices=[
                    (b'Commodity', b'Commodity'),
                    (b'Crowd-sourced data', b'Crowd-sourced data'),
                    (b'Derived by trusted agents ',
                     b'Derived by trusted agents '),
                    (b'Open Source', b'Open Source'),
                    (b'Structured Observations (SOM)',
                     b'Structured Observations (SOM)'),
                    (b'Unknown', b'Unknown')]),
        ),
        migrations.AddField(
            model_name='cswrecord',
            name='registered',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='cswrecord',
            name='releasability',
            field=models.CharField(
                blank=True, max_length=128, choices=[(b'FOUO', b'FOUO')]),
        ),
        migrations.AddField(
            model_name='cswrecord',
            name='short_name',
            field=models.CharField(max_length=328, blank=True),
        ),
        migrations.AddField(
            model_name='cswrecord',
            name='srid',
            field=models.CharField(default=b'EPSG:4326', max_length=255),
        ),
        migrations.AlterField(
            model_name='cswrecord',
            name='classification',
            field=models.CharField(
                blank=True, max_length=128, choices=[
                    (b'UNCLASSIFIED', b'UNCLASSIFIED')]),
        ),
    ]
