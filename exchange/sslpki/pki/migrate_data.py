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

from __future__ import unicode_literals

import os
import types
import logging


from django.conf import settings
from django.apps.registry import Apps
from django.db.models import Max

try:
    from ssl_pki.utils import get_pki_dir
    from ssl_pki.crypto import Crypto, CryptoInvalidToken
    from ssl_pki.fields import ENCRYPTED_PREFIX
except ImportError:
    get_pki_dir = None
    Crypto = None
    CryptoInvalidToken = None
    ENCRYPTED_PREFIX = None

logger = logging.getLogger(__name__)


def db_table_exists(schema_editor, table_name):
    return table_name in schema_editor.connection.introspection.table_names()


def strip_pki_dir(path):
    if not callable(get_pki_dir):
        return path
    if path and path.strip().startswith(get_pki_dir()):
        path = os.path.relpath(path, get_pki_dir().rstrip(os.sep))
    return path


def decrypt_value(value):
    if not callable(Crypto):
        return value

    if value is None or not isinstance(value, types.StringTypes):
        return value

    if ENCRYPTED_PREFIX and value.startswith(ENCRYPTED_PREFIX):
        value = value[len(ENCRYPTED_PREFIX):]

        crypter = Crypto()
        try:
            value = crypter.decrypt(value)
        except CryptoInvalidToken:
            pass
        except TypeError:
            pass

    return value


def sslconfig_eq(sp_config, pki_config):
    """
    :type sp_config ssl_pki.models.SslConfig
    :type pki_config exchange.sslpki.pki.models.SslConfig
    :return: bool
    """
    return all([
        sp_config.name == pki_config.name,
        sp_config.description == pki_config.description,
        strip_pki_dir(sp_config.ca_custom_certs) == pki_config.ca_custom_certs,
        sp_config.ca_allow_invalid_certs == pki_config.ca_allow_invalid_certs,
        strip_pki_dir(sp_config.client_cert) == pki_config.client_cert,
        strip_pki_dir(sp_config.client_key) == pki_config.client_key,
        sp_config.client_key_pass == decrypt_value(pki_config.client_key_pass),
        sp_config.ssl_version == pki_config.ssl_version,
        sp_config.ssl_verify_mode == pki_config.ssl_verify_mode,
        sp_config.ssl_options == pki_config.ssl_options,
        sp_config.ssl_ciphers == pki_config.ssl_ciphers,
        sp_config.https_retries == pki_config.https_retries,
        sp_config.https_redirects == pki_config.https_redirects,
    ])


def clone_sslconfig(sp_config_model, pki_config):
    """
    :type sp_config_model ssl_pki.models.SslConfig
    :type pki_config exchange.sslpki.pki.models.SslConfig
    :rtype ssl_pki.models.SslConfig
    """
    # noinspection PyCallingNonCallable
    sp_config = sp_config_model()
    """:type: ssl_pki.models.SslConfig"""
    sp_config.name = pki_config.name
    sp_config.description = pki_config.description
    sp_config.ca_custom_certs = pki_config.ca_custom_certs
    sp_config.ca_allow_invalid_certs = pki_config.ca_allow_invalid_certs
    sp_config.client_cert = pki_config.client_cert
    sp_config.client_key = pki_config.client_key
    sp_config.client_key_pass = decrypt_value(pki_config.client_key_pass)
    sp_config.ssl_version = pki_config.ssl_version
    sp_config.ssl_verify_mode = pki_config.ssl_verify_mode
    sp_config.ssl_options = pki_config.ssl_options
    sp_config.ssl_ciphers = pki_config.ssl_ciphers
    sp_config.https_retries = pki_config.https_retries
    sp_config.https_redirects = pki_config.https_redirects

    return sp_config


def clone_hpsslconfig(sp_hpconfig_model, pki_hpconfig):
    """
    :type sp_hpconfig_model ssl_pki.models.HostnamePortSslConfig
    :type pki_hpconfig exchange.sslpki.pki.models.HostnamePortSslConfig
    :rtype ssl_pki.models.HostnamePortSslConfig
    """
    # noinspection PyCallingNonCallable
    sp_hpconfig = sp_hpconfig_model()
    """:type: ssl_pki.models.HostnamePortSslConfig"""
    sp_hpconfig.hostname_port = pki_hpconfig.hostname_port
    sp_hpconfig.enabled = pki_hpconfig.enabled
    sp_hpconfig.proxy = pki_hpconfig.proxy

    return sp_hpconfig


def hpsslconfig_eq(sp_hpconfig, pki_hpconfig):
    """
    :type sp_hpconfig ssl_pki.models.HostnamePortSslConfig
    :type pki_hpconfig exchange.sslpki.pki.models.HostnamePortSslConfig
    :return: bool
    """
    return sp_hpconfig.hostname_port == pki_hpconfig.hostname_port


def migrate_pki_data(proj_apps, schema_editor):
    """
    Migrate data forward to ssl_pki app from any existing exchange.pki tables.
    :returns Reason text on failure or None on success
    """
    if not isinstance(proj_apps, Apps):
        msg = 'Invalid proj_apps parameter for copy_pki_data()'
        logger.error(msg)
        return msg
    if schema_editor is None or not hasattr(schema_editor, 'connection'):
        msg = 'Invalid schema_editor parameter for copy_pki_data()'
        logger.error(msg)
        return msg
    if not (db_table_exists(schema_editor, 'pki_sslconfig') and
            db_table_exists(schema_editor, 'pki_hostnameportsslconfig')):
        # Note: check needed because exchange.sslpki.pki models are not managed
        msg = 'No exchange.pki tables found; no data to migrate'
        logger.info(msg)
        return msg
    if 'ssl_pki' not in settings.INSTALLED_APPS:
        msg = 'No ssl_pki app in INSTALLED_APPS; aborting migration'
        logger.warn(msg)
        return msg
    if 'exchange.sslpki.pki' not in settings.INSTALLED_APPS:
        msg = 'No exchange.sslpki.pki in INSTALLED_APPS; aborting migration'
        logger.warn(msg)
        return msg
    db_alias = schema_editor.connection.alias
    sp_config_model = proj_apps.get_model('ssl_pki', 'SslConfig')
    sp_configs = sp_config_model.objects.using(db_alias).all()
    default_sp_config = sp_config_model.objects.using(db_alias).get(pk=1)
    """:type: ssl_pki.models.SslConfig"""
    # logger.debug('sp_configs: {0}'.format(sp_configs))

    sp_hpconfig_model = proj_apps.get_model('ssl_pki',
                                            'HostnamePortSslConfig')
    sp_hpconfigs = sp_hpconfig_model.objects.using(db_alias).all()
    # logger.debug('sp_hpconfigs: {0}'.format(sp_hpconfigs))

    pki_config_model = proj_apps.get_model('pki', 'SslConfig')
    pki_configs = pki_config_model.objects.using(db_alias).all()
    """:type: list[exchange.sslpki.pki.models.SslConfig]"""
    # logger.debug('pki_configs: {0}'.format(pki_configs))

    pki_cfg_ids = [c.pk for c in pki_configs]

    pki_hpconfig_model = proj_apps.get_model('pki',
                                             'HostnamePortSslConfig')
    pki_hpconfigs = pki_hpconfig_model.objects.using(db_alias).all()
    """:type: list[exchange.sslpki.pki.models.HostnamePortSslConfig]"""
    # logger.debug('pki_hpconfigs: {0}'.format(pki_hpconfigs))

    # Copy over SslConfigs, and map old configs to new configs
    pki_sp_cfg_ids = []
    for pki_config in pki_configs:
        matched = False
        for sp_config in sp_configs:
            if sslconfig_eq(sp_config, pki_config):
                # map to default or existing config
                pki_sp_cfg_ids.append(sp_config.pk)
                matched = True
                break
        if not matched:
                # duplicate config, then map to it
                new_sp_config = clone_sslconfig(sp_config_model, pki_config)
                new_sp_config.save(using=db_alias)
                pki_sp_cfg_ids.append(new_sp_config.pk)

    # logger.debug('pki_cfg_ids: {0}'.format(pki_cfg_ids))
    # logger.debug('pki_sp_cfg_ids: {0}'.format(pki_sp_cfg_ids))

    # Copy over HostnamePort mappings
    sp_hpconfig_order = -1
    if sp_hpconfig_model.objects.using(db_alias).count() > 0:
        sp_hpconfig_order = sp_hpconfig_model.objects.using(db_alias)\
            .all().aggregate(Max('order'))['order__max']

    for pki_hpconfig in pki_hpconfigs:
        matched = False
        for sp_hpconfig in sp_hpconfigs:
            if hpsslconfig_eq(sp_hpconfig, pki_hpconfig):
                matched = True
                break
        if not matched:
            old_sp_cfg_id = pki_hpconfig.ssl_config_id
            if old_sp_cfg_id not in pki_cfg_ids:
                sp_cfg_id = default_sp_config.pk
            else:
                sp_indx = pki_cfg_ids.index(old_sp_cfg_id)
                if len(pki_sp_cfg_ids) - 1 < sp_indx:
                    sp_cfg_id = default_sp_config.pk
                else:
                    sp_cfg_id = pki_sp_cfg_ids[sp_indx]

            new_sp_hpconfig = \
                clone_hpsslconfig(sp_hpconfig_model, pki_hpconfig)
            """:type: ssl_pki.models.HostnamePortSslConfig"""

            # maintain old order and append to existing
            sp_hpconfig_order += 1
            new_sp_hpconfig.order = sp_hpconfig_order
            # reset foreign key to newly copied (or existing) SslConfig
            new_sp_hpconfig.ssl_config = \
                sp_config_model.objects.using(db_alias).get(pk=sp_cfg_id)
            new_sp_hpconfig.save(using=db_alias)

    return None
