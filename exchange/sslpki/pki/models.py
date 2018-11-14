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

import logging

from django.db import models

logger = logging.getLogger(__name__)


class SslConfig(models.Model):

    name = models.CharField(
        max_length=128,
        blank=False,
    )
    description = models.TextField(
        blank=True,
    )
    ca_custom_certs = models.CharField(
        max_length=100,
        blank=True,
    )
    ca_allow_invalid_certs = models.BooleanField(
        default=False,
        blank=False,
    )
    client_cert = models.CharField(
        max_length=100,
        blank=True,
    )
    client_key = models.CharField(
        max_length=100,
        blank=True,
    )
    client_key_pass = models.CharField(
        max_length=255,
        blank=True,
    )
    ssl_version = models.CharField(
        max_length=18,
        default='PROTOCOL_SSLv23',
        blank=False,
    )
    ssl_verify_mode = models.CharField(
        max_length=16,
        default='CERT_REQUIRED',
        blank=False,
    )
    ssl_options = models.CharField(
        max_length=255,
        blank=True,
    )
    ssl_ciphers = models.TextField(
        blank=True,
    )
    https_retries = models.CharField(
        max_length=6,
        default='3',
        blank=False,
    )
    https_redirects = models.CharField(
        max_length=6,
        default='3',
        blank=False,
    )

    class Meta:
        managed = False


class HostnamePortSslConfig(models.Model):
    enabled = models.BooleanField(
        default=True,
        blank=False,
    )
    hostname_port = models.CharField(
        max_length=255,
        blank=False,
        primary_key=True,
        unique=True,
    )
    # ssl_config = models.ForeignKey(
    #     SslConfig,
    #     related_name='+',
    #     null=True,
    # )
    ssl_config_id = models.IntegerField(
        null=True,
    )
    proxy = models.BooleanField(
        default=True,
        blank=False,
    )
    order = models.PositiveIntegerField(
        editable=False,
    )

    class Meta:
        managed = False
        ordering = ('order',)
