# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2018 Boundless Spatial
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
from geonode.services.models import Service
from django.db.models import signals


class ExchangeService(models.Model):
    geonode_service = models.OneToOneField(Service)
    poc_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    poc_position = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    poc_email = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    poc_phone = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    poc_address = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )


def exchange_service_post_save(instance, sender, **kwargs):
    # Get all ExchangeLayers associated with this ExchangeService and
    # update their license to correspond to the Service license
    for layer in instance.exchangelayer_set.all():
        layer.geonode_layer.license = instance.geonode_service.license
        layer.geonode_layer.save()


signals.post_save.connect(exchange_service_post_save, sender=ExchangeService)
