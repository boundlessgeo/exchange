# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2016 Boundless Spatial
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from django.db import models
from solo.models import SingletonModel
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from resizeimage import resizeimage
from django import forms
import os
import uuid
import datetime
from django.db.models import Q
from geonode.base.models import TopicCategory, License
from geonode.base.enumerations import UPDATE_FREQUENCIES
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import Group


class ThumbnailImage(SingletonModel):
    thumbnail_image = models.ImageField(
        upload_to=os.path.join(settings.MEDIA_ROOT, 'thumbs'),
    )

    def save(self, *args, **kwargs):
        pil_image_obj = Image.open(self.thumbnail_image)
        new_image = resizeimage.resize_cover(
            pil_image_obj,
            [250, 150],
            validate=False
        )

        new_image_io = BytesIO()
        new_image.save(new_image_io, format='PNG')

        temp_name = self.thumbnail_image.name
        self.thumbnail_image.delete(save=False)

        self.thumbnail_image.save(
            temp_name,
            content=ContentFile(new_image_io.getvalue()),
            save=False
        )

        super(ThumbnailImage, self).save(*args, **kwargs)


class ThumbnailImageForm(forms.Form):
    thumbnail_image = forms.FileField(
        label='Select a file',
    )


def get_classifications():
        return [(x, str(x)) for x in getattr(
            settings, 'CLASSIFICATION_LEVELS', [])]


def get_caveats():
        return [(x, str(x)) for x in getattr(settings, 'CAVEATS', [])]


def get_provenances():
        default = [('Commodity', 'Commodity'),
                   ('Crowd-sourced data', 'Crowd-sourced data'),
                   ('Derived by trusted agents ',
                    'Derived by trusted agents '),
                   ('Open Source', 'Open Source'),
                   ('Structured Observations (SOM)',
                    'Structured Observations (SOM)'),
                   ('Unknown', 'Unknown')]

        provenance_choices = [(x, str(x)) for x in getattr(
            settings, 'PROVENANCE_CHOICES', [])]

        return provenance_choices + default


class CSWRecord(models.Model):
    # Registry requires a UUID for all new records
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=128, default='Unknown')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name="csw_records_created")

    category_choices = (
        ('Air', 'Air (Aero)'),
        ('Intelligence', 'Intelligence'),
        ('Elevation', 'Elevation'),
        ('HumanGeog', 'Human Geography'),
        ('Basemaps', 'Basemaps'),
        ('Space', 'Space'),
        ('Land', 'Land (Topo)'),
        ('Targeting', 'Targeting'),
        ('NamesBoundaries', 'Names & Boundaries'),
        ('MapsCharts', 'NGA Standard Maps & Charts'),
        ('Sea', 'Sea (Maritime)'),
        ('Imagery', 'Imagery/Collections'),
        ('Geomatics', 'Geodesy/Geodetics Geomatics'),
        ('Weather', 'Weather')
    )

    classification = models.CharField(
        max_length=128, blank=True, choices=get_classifications())
    releasability = models.CharField(
        max_length=128, blank=True, choices=get_caveats())
    title = models.CharField(max_length=328, blank=False)
    short_name = models.CharField(max_length=328, blank=True)
    modified = models.DateField(default=datetime.date.today, blank=False)
    created = models.DateField(default=datetime.date.today, blank=False)
    registered = models.DateField(default=datetime.date.today, blank=False)
    # 'creator' is assumed to be distinct from logged-in User here
    creator = models.CharField(
        max_length=328, blank=True, verbose_name='Agency')
    record_type = models.CharField(max_length=128, blank=True)
    alternative = models.CharField(max_length=128, blank=True)
    abstract = models.TextField(blank=True)
    source = models.URLField(
        max_length=512, blank=False, verbose_name='Service Endpoint')
    relation = models.CharField(max_length=128, blank=True)
    record_format = models.CharField(max_length=128, blank=True)
    srid = models.CharField(max_length=255, default='EPSG:4326')
    bbox_upper_corner = models.CharField(max_length=128,
                                         default="85.0 180",
                                         blank=True)
    bbox_lower_corner = models.CharField(max_length=128,
                                         default="-85.0 -180",
                                         blank=True)
    contact_email = models.CharField(max_length=128, blank=True)
    contact_phone = models.CharField(max_length=128, blank=True)
    contact_position = models.CharField(max_length=128, blank=True)
    contact_address_type = models.CharField(
        max_length=128, blank=True, choices=(
            ('Physical', 'Physical'), ('Postal', 'Postal')))
    contact_address = models.CharField(max_length=128, blank=True)
    contact_city = models.CharField(max_length=128, blank=True)
    contact_state = models.CharField(max_length=2, blank=True)
    contact_country = models.CharField(max_length=128, blank=True)
    contact_zip = models.CharField(max_length=128, blank=True)
    provenance = models.CharField(
        max_length=100, blank=True, choices=get_provenances())
    gold = models.BooleanField(max_length=128, default=False, blank=True)
    category = models.CharField(max_length=128, choices=category_choices,
                                blank=True)
    maintenance_frequency = models.CharField(
        'maintenance frequency', max_length=255, choices=UPDATE_FREQUENCIES,
        blank=True, null=True,
        help_text='Frequency with which modifications and deletions are made '
                  'to the data after it is first produced')
    license = models.ForeignKey(License, null=True, blank=True,
                                verbose_name='License',
                                help_text='License of the dataset')
    keywords = models.CharField(max_length=128, blank=True)

    fees = models.CharField(max_length=1000, null=True, blank=True)
    topic_category = models.ForeignKey(
        TopicCategory, null=True, blank=True, limit_choices_to=Q(
            is_choice=True))
    status_message = models.TextField(blank=True)

    @property
    def contact_information(self):
        """Returns formatted contact information."""
        return "Email: {}\nPhone: {}".format(
            self.contact_email, self.contact_phone)

    class Meta(object):
        verbose_name = 'CSW Record'
        verbose_name_plural = 'CSW Records'
        ordering = ['-modified', 'status', 'title']


class CSWRecordReference(models.Model):
    scheme_choices = (('ESRI:AIMS--http-get-map', 'MapServer'),
                      ('ESRI:AIMS--http-get-feature', 'FeatureServer'),
                      ('ESRI:AIMS--http-get-image', 'ImageServer'),
                      ('WWW:LINK-1.0-http--json', 'JSON'),
                      ('OGC:KML', 'KML'),
                      ('WWW:LINK-1.0-http--rss', 'RSS'),
                      ('WWW:DOWNLOAD', 'SHAPE'),
                      ('WWW:LINK-1.0-http--soap', 'SOAP'),
                      ('OGC:WCS', 'WCS'),
                      ('OGC:WFS', 'WFS'),
                      ('OGC:CS-W', 'CSW'),
                      ('OGC:WMS', 'WMS'),
                      ('OGC:WPS', 'WPS'))
    record = models.ForeignKey(CSWRecord, related_name="references")
    scheme = models.CharField(
        verbose_name='Service Type', choices=scheme_choices, max_length=100)
    url = models.URLField(max_length=512, blank=False)


def add_default_permissions(sender, **kwargs):
    user = kwargs['instance']
    if kwargs['created']:
        for group_name in settings.DEFAULT_USER_AUTH_GROUPS:
            auth_group = Group.objects.get(name=group_name)
            user.groups.add(auth_group)


post_save.connect(add_default_permissions, sender=settings.AUTH_USER_MODEL)
