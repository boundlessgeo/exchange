#!/usr/bin/env python
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

import json
import logging
# noinspection PyPackageRequirements
import pytest
import django
import mock

from urllib import quote, quote_plus
from requests import get, Request
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, SSLError, InvalidSchema

from django.conf import settings
from django.core import management
from django.core.exceptions import ImproperlyConfigured, AppRegistryNotReady
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from django.http import HttpResponse

try:
    # Do this before geonode.services.serviceprocessors, so that apps are ready
    django.setup()
except (RuntimeError, ImproperlyConfigured,
        AppRegistryNotReady, LookupError, ValueError):
    raise

from geonode.base import models as base_models
from geonode.maps import models as maps_models
from geonode.services import enumerations
from geonode.services.models import Service

from . import ExchangeTest

from ssl_pki.settings import get_pki_dir, SSL_DEFAULT_CONFIG
from ssl_pki.models import (
    SslConfig,
    HostnamePortSslConfig,
    hostnameport_pattern_cache,
    hostnameport_pattern_proxy_cache,
    rebuild_hostnameport_pattern_cache,
    ssl_config_for_url,
    has_ssl_config,
    hostnameport_pattern_for_url,
    uses_proxy_route,
)
from ssl_pki.crypto import Crypto
from ssl_pki.validate import (
    PkiValidationError,
    pki_dir_path,
    pki_file_exists_readable,
    pki_file_contents,
    pki_acceptable_format,
    cert_date_not_yet_valid,
    cert_date_expired,
    is_ca_cert,
    is_client_cert,
    cert_subject_common_name,
    load_certs,
    load_first_cert,
    load_private_key,
    validate_cert_matches_private_key,
    validate_cert_file_matches_key_file,
    validate_ca_certs,
    validate_client_cert,
    validate_client_key,
)
from ssl_pki.ssl_adapter import SslContextAdapter
from ssl_pki.ssl_session import SslContextSession, https_client
from ssl_pki.utils import (
    protocol_relative_url,
    protocol_relative_to_scheme,
    relative_to_absolute_url,
    hostname_port,
    normalize_hostname,
    requests_base_url,
    pki_prefix,
    pki_file,
    pki_site_prefix,
    has_pki_prefix,
    pki_route,
    pki_route_reverse,
    has_proxy_prefix,
    proxy_route,
    proxy_route_reverse,
    pki_to_proxy_route,
)

logger = logging.getLogger(__name__)


# bury these warnings for testing
class RemovedInDjango19Warning(Exception):
    pass


def has_mapproxy():
    try:
        mp_http = get('http://mapproxy.boundless.test:8088')
        assert mp_http.status_code == 200
        return True
    except (ConnectionError, AssertionError):
        return False


class PkiTestCase(ExchangeTest):

    # Note use of cls.local_fixtures, not cls.fixtures; see setUpTestData
    # local_fixtures = ['test_ssl_configs.json']
    local_fixtures = ['test_ssl_configs_no_default.json']

    @classmethod
    def setUpClass(cls):
        # django.setup()
        management.call_command('rebuild_index')
        super(PkiTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(PkiTestCase, cls).tearDownClass()

    @classmethod
    def load_local_fixtures(cls, fixture_list):
        """Load fixtures independent of Django's TestCase"""
        if not isinstance(fixture_list, list):
            raise Exception('fixture_list is not a list')

        for db_name in cls._databases_names(include_mirrors=False):
            # Let this raise upon failure, so db rollback is triggered
            management.call_command(
                'loaddata', *fixture_list, **{
                    'verbosity': 0,
                    'commit': False,
                    'database': db_name,
                })

    @classmethod
    def setUpTestData(cls):
        """Load initial data for the TestCase"""

        # Delete any custom SslConfigs, but leave default added during
        # initial data migration.
        SslConfig.objects.all().delete()
        ssl_def_config = SslConfig.objects.get_create_default()

        if (SslConfig.objects.count() != 1 or
                str(ssl_def_config.name) != SSL_DEFAULT_CONFIG['name']):
            raise Exception('Problem setting up default SslConfig')

        # We load fixtures here, because we need to ensure our test tables are
        # clean of any existing non-default data, since this method is called
        # *after* atomic rollback snapshot and fixtures loaded, which makes it
        # tricky to clean the tables after snapshot, but prior to loading data.
        if cls.local_fixtures:
            cls.load_local_fixtures(cls.local_fixtures)

        # No custom SslConfigs should exist; clean data state only
        assert SslConfig.objects.count() == 8
        cls.ssl_config_1 = SslConfig.objects.get(pk=1)
        assert cls.ssl_config_1.name == \
            u"Default: TLS-only"
        cls.ssl_config_2 = SslConfig.objects.get(pk=2)
        assert cls.ssl_config_2.name == \
            u"Just custom CAs"
        cls.ssl_config_3 = SslConfig.objects.get(pk=3)
        assert cls.ssl_config_3.name == \
            u"PKI: key with no password"
        cls.ssl_config_4 = SslConfig.objects.get(pk=4)
        assert cls.ssl_config_4.name == \
            u"PKI: key with password"
        cls.ssl_config_5 = SslConfig.objects.get(pk=5)
        assert cls.ssl_config_5.name == \
            u"PKI: key with password; TLSv1_2-only; alt root CA chain"
        cls.ssl_config_6 = SslConfig.objects.get(pk=6)
        assert cls.ssl_config_6.name == u"PKI: key with password; TLSv1_2-only"
        cls.ssl_config_7 = SslConfig.objects.get(pk=7)
        assert cls.ssl_config_7.name == \
            u"PKI: key with no password; custom CAs with no validation"
        cls.ssl_config_8 = SslConfig.objects.get(pk=8)
        assert cls.ssl_config_8.name == \
            u"PKI: key with no password; TLSv1_2-only (via ssl_options)"

        # Clear out all preexisting table and cache data that needs tested
        https_client.clear_https_adapters()

        HostnamePortSslConfig.objects.all().delete()
        rebuild_hostnameport_pattern_cache()
        assert hostnameport_pattern_cache == []
        assert hostnameport_pattern_proxy_cache == []

        # Data associated with internal MapProxy test server
        # This needs to be mixed case, to ensure SslContextAdapter handles
        # server cert matching always via lowercase hostname (bug in urllib3)
        cls.mp_root = u'https://maPproxy.Boundless.test:8344/'

        cls.mp_root_http = u'http://mapproxy.boundless.test:8088/'

        # Already know what the lookup table key should be like
        cls.mp_host_port = hostname_port(cls.mp_root)

        cls.mp_txt = 'Welcome to MapProxy'

        # Some debug output for sanity check on default data state
        logger.debug("SslConfig.objects:\n{0}"
                     .format(repr(SslConfig.objects.all())))

        logger.debug("HostnamePort.objects:\n{0}"
                     .format(repr(SslConfig.objects.all())))

        logger.debug("PKI_DIRECTORY: {0}".format(get_pki_dir()))

    def create_hostname_port_mapping(self, ssl_config, ptn=None):
        if ptn is None:
            ptn = self.mp_host_port
        logger.debug("Attempt Hostname:Port mapping for SslConfig: {0}"
                     .format(ssl_config))
        if isinstance(ssl_config, int):
            ssl_config = SslConfig.objects.get(pk=ssl_config)
        if not isinstance(ssl_config, SslConfig):
            raise Exception('ssl_config not an instance of SslConfig')
        hp_map = HostnamePortSslConfig.objects.create_hostnameportsslconfig(
            ptn, ssl_config)
        logger.debug("Hostname:Port mappings:\n{0}"
                     .format(HostnamePortSslConfig.objects.all()))
        return hp_map


class TestSslContextSessionAdapter(PkiTestCase):

    def setUp(self):
        HostnamePortSslConfig.objects.all().delete()
        self.assertEqual(HostnamePortSslConfig.objects.count(), 0)

        self.p1 = u'{0}*'.format(self.mp_host_port)

        self.getcaps_url = \
            '{0}/service?version=1.1.1&service=WMS&request=GetCapabilities'\
            .format(self.mp_root.rstrip('/').lower())

    def tearDown(self):
        pass

    def testSslContextAdapter(self):
        config = self.ssl_config_4
        self.create_hostname_port_mapping(config, self.p1)
        self.assertEqual(HostnamePortSslConfig.objects.count(), 1)

        ssla = SslContextAdapter(self.mp_root)

        # SslConfig options should round-trip. This indicates a hostname port
        # mapping match has occurred within adapter and that the returned
        # config's context options are the same as a direct conversion of
        # expected SslConfig
        self.assertEqual(
            ssla.get_ssl_context_opts(normalize_hostname(self.mp_root)),
            SslContextAdapter.ssl_config_to_context_opts(config))
        # Same, but via dump-to-tuple method
        self.assertEqual(
            ssla.context_options(),
            SslContextAdapter.ssl_config_to_context_opts(config))

        # Ensure adapter's Retry object matches passed-in settings
        _, _, adptr_opts = SslContextAdapter.ssl_config_to_context_opts(config)
        self.assertEqual(ssla.max_retries.total, adptr_opts['retries'])
        self.assertEqual(ssla.max_retries.redirect, adptr_opts['redirects'])

        # Request does not normalize URL
        req = Request(method='GET', url=self.mp_root)
        self.assertEqual(req.url, self.mp_root)

        # PreparedRequest does normalize URL
        p_req = req.prepare()
        self.assertEqual(p_req.url, normalize_hostname(self.mp_root))

        # SslContextAdapter should always normalize the URL, because urllib3's
        # SSL cert hostname matching is case-sensitive (and shouldn't be)
        self.assertEqual(SslContextAdapter._normalize_hostname(self.mp_root),
                         normalize_hostname(self.mp_root))
        self.assertEqual(SslContextAdapter._normalize_hostname(self.mp_root),
                         p_req.url)

        # Sending solely via adapter (outside of session) should work for
        # connections that do not require cookies, etc.
        resp = ssla.send(p_req)
        self.assertEqual(resp.status_code, 200)

    def testSslContextSession(self):
        def clear_adapters():
            https_client.clear_https_adapters()
            self.assertEqual(len(https_client.adapters), 1)  # just 'http://'

        self.assertIsInstance(https_client, SslContextSession)

        self.assertEqual(len(https_client.adapters), 1)  # for 'http://'

        https_client.mount('https://', HTTPAdapter())
        self.assertEqual(len(https_client.adapters), 2)
        clear_adapters()

        resp = https_client.get(self.mp_root_http)
        self.assertEqual(resp.status_code, 200)
        # No new adapters should have been created
        self.assertEqual(len(https_client.adapters), 1)

        resp = https_client.get('https://example.com')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(https_client.adapters), 2)

        # Should not delete any http adapters
        clear_adapters()

        resp2 = None
        try:
            resp2 = https_client.get(self.mp_root)
        except SSLError:
            pass  # needs PKI
        if resp2:
            self.assertEqual(resp2.status_code, 400)  # needs PKI
        mp_adptr = https_client.get_adapter(requests_base_url(self.mp_root))
        self.assertIsNotNone(mp_adptr)
        self.assertIsInstance(mp_adptr, HTTPAdapter)
        self.assertEqual(len(https_client.adapters), 2)

        clear_adapters()

        # Now add it back, so we can verify adding a mapping clears bad adapter
        resp2 = None
        try:
            resp2 = https_client.get(self.mp_root)
        except SSLError:
            pass  # still needs PKI
        if resp2:
            self.assertEqual(resp2.status_code, 400)  # still needs PKI
        self.assertEqual(len(https_client.adapters), 2)

        # Add a PKI SslConfig mapping for the MapProxy endpoint
        config = self.ssl_config_4
        self.create_hostname_port_mapping(config)
        self.assertEqual(HostnamePortSslConfig.objects.count(), 1)
        # Signal should have updated any adapter that now matches a mapping
        logging.debug('https_client.adapters: {0}'
                      .format(https_client.adapters))
        self.assertEqual(len(https_client.adapters), 2)
        # Adapter should now be SslContextAdapter (not HTTPAdapter), and have
        # same SslConfig opts
        mp_adptr1 = https_client.get_adapter(requests_base_url(self.mp_root))
        self.assertIsNotNone(mp_adptr1)
        self.assertIsInstance(mp_adptr1, SslContextAdapter)
        self.assertEqual(
            mp_adptr1.get_ssl_context_opts(normalize_hostname(self.mp_root)),
            SslContextAdapter.ssl_config_to_context_opts(config))

        HostnamePortSslConfig.objects.all().delete()
        # Signal should have deleted any SslContextAdapter that no longer
        # matches a mapping
        self.assertEqual(len(https_client.adapters), 1)  # just 'http://'

        # Add the mapping again, but leave adapters cleared for next test
        self.create_hostname_port_mapping(config)
        self.assertEqual(HostnamePortSslConfig.objects.count(), 1)
        # Adding a mapping does not create an adapter, only connections do
        self.assertEqual(len(https_client.adapters), 1)

        # Mount the URL's adapter directly
        https_client.mount_sslcontext_adapter(self.mp_root)
        self.assertEqual(len(https_client.adapters), 2)
        # Adapter should be SslContextAdapter and have same SslConfig opts
        mp_adptr2 = https_client.get_adapter(requests_base_url(self.mp_root))
        self.assertIsNotNone(mp_adptr2)
        self.assertIsInstance(mp_adptr2, SslContextAdapter)
        self.assertEqual(
            mp_adptr2.get_ssl_context_opts(normalize_hostname(self.mp_root)),
            SslContextAdapter.ssl_config_to_context_opts(config))

        resp2 = https_client.get(self.mp_root)
        self.assertEqual(resp2.status_code, 200)
        # No new adapters should have been created
        self.assertEqual(len(https_client.adapters), 2)

        clear_adapters()

        # Mount the URL's adapter dynamically during a connection
        resp3 = https_client.get(self.mp_root)
        self.assertEqual(resp3.status_code, 200)
        # A new adapter should have been auto-created, via mapping match
        self.assertEqual(len(https_client.adapters), 2)
        mp_adptr3 = https_client.get_adapter(requests_base_url(self.mp_root))
        self.assertIsNotNone(mp_adptr3)
        self.assertIsInstance(mp_adptr3, SslContextAdapter)
        self.assertEqual(
            mp_adptr3.get_ssl_context_opts(normalize_hostname(self.mp_root)),
            SslContextAdapter.ssl_config_to_context_opts(config))


@pytest.mark.skip(reason="Because it's fixture loading needs fixed")
class TestHostnamePortSslConfig(PkiTestCase):

    def setUp(self):
        self.login()

        # Service.objects.all().delete()

        HostnamePortSslConfig.objects.all().delete()
        self.assertEqual(HostnamePortSslConfig.objects.count(), 0)

        self.ssl_configs = [
            self.ssl_config_1,  # Default: TLS-only
            self.ssl_config_4,  # PKI: key with password
            self.ssl_config_2   # Just custom CAs
        ]

        self.p1 = u'*.arcgisonline.com*'
        self.p2 = u'*.boundless.test*'
        self.p3 = u'*.*'
        self.ptrns = [self.p1, self.p2, self.p3]

        ptrns_l = []
        self.hp_maps = []
        for config, p in zip(self.ssl_configs, self.ptrns):
            hp_map = self.create_hostname_port_mapping(config, p)
            ptrns_l.append(p)
            self.assertEqual(hostnameport_pattern_cache, ptrns_l)

            hp_map_query = HostnamePortSslConfig.objects.get(hostname_port=p)
            self.assertEqual(hp_map, hp_map_query)
            self.hp_maps.append(hp_map)

        self.assertTrue(all(self.hp_maps))

    def tearDown(self):
        pass

    def testHostnamePortSslConfigSignals(self):
        https_client.clear_https_adapters()
        self.assertEqual(len(https_client.adapters), 1)  # for http://

        url1 = u'https://services.arcgisonline.com/arcgis/rest/' \
               u'services/topic/layer/?f=pjson'
        url2 = u'https://maPproxy.Boundless.test:8344/service?' \
               u'service=WMS&request=GetCapabilities&version=1.1.1'
        url3 = u'https://data-test.boundlessgeo.io/some/path?key=value#frag'
        # u'https://привет.你好.çéàè.example.com/some/path?key=value#frag'
        urls = [url1, url2, url3]

        for p, config, url in zip(self.ptrns, self.ssl_configs, urls):
            self.assertTrue(has_ssl_config(url))
            ssl_config = ssl_config_for_url(url)
            self.assertIsNotNone(ssl_config)
            self.assertEqual(ssl_config, config)
            self.assertEqual(
                SslContextAdapter.ssl_config_to_context_opts(ssl_config),
                SslContextAdapter.ssl_config_to_context_opts(config)
            )
            self.assertEqual(hostnameport_pattern_for_url(url), p)

        # Load hostnameport mappings
        # Done in setUp()

        # Load https_client adapters
        for url, ssl_config in zip(urls, self.ssl_configs):
            base_url = requests_base_url(url)
            https_client.mount_sslcontext_adapter(url)
            adptr = https_client.adapters[base_url]
            """:type: SslContextAdapter"""
            self.assertIsInstance(adptr, SslContextAdapter)
            self.assertEqual(
                adptr.context_options(),
                SslContextAdapter.ssl_config_to_context_opts(ssl_config))

        self.assertEqual(len(https_client.adapters), 4)  # https* + http://

        # Ensure *.* pattern is not enabled (to match loaded test data state)
        wild_hp_map = HostnamePortSslConfig.objects.get(hostname_port='*.*')
        wild_hp_map.enabled = False
        wild_hp_map.save()

        self.assertEqual(len(https_client.adapters), 3)  # https* + http://
        # https://data-test.boundlessgeo.io should now not match; so deleted

        # Load layer legend links
        base_models.Link.objects.all().delete()
        self.load_local_fixtures(['test_geonode_base_legend_link.json'])

        # Load map links
        maps_models.MapLayer.objects.all().delete()
        self.load_local_fixtures(['test_geonode_maps_maplayer.json'])

        base_urls = [
            u'https://services.arcgisonline.com',     # proxied
            u'https://mapproxy.boundless.test:8344',  # proxied
            u'https://data-test.boundlessgeo.io',     # not proxied
            u'//data-test.boundlessgeo.io',           # not proxied ()
            # u'https://привет.你好.çéàè.example.com',   # not proxied
            # u'//привет.你好.çéàè.example.com',         # not proxied
        ]

        def test_base_urls(b_urls, url_specs):
            """
            :param b_urls: List of base URLs to test
            :param url_specs: list[dict] indicating whether a url should match
            a pattern and whether that pattern is enabled or should use a proxy
            :return: None
            """
            if not url_specs:
                raise Exception('No pattern boolean map to test against')
            for b in range(0, len(b_urls)):
                url_spec = url_specs[b]
                b_url = b_urls[b]
                print('url_specs[{0}]: {1}'.format(b, url_spec))
                print('b_urls[{0}]   : {1}'.format(b, b_url))
                hp_map = None
                hp_ptn = hostnameport_pattern_for_url(b_url)
                hp_ptn_match = hp_ptn is not None
                self.assertEqual(hp_ptn_match, url_spec['match'])
                if hp_ptn_match:
                    hp_map = HostnamePortSslConfig.objects\
                        .get(hostname_port=hp_ptn)
                    self.assertIsNotNone(hp_map)

                    self.assertEqual(url_spec['match'], hp_map.enabled)
                    self.assertEqual(url_spec['proxy'], hp_map.proxy)

                    # Verify sync of rebuild_hostnameport_pattern_cache()
                    self.assertEqual(
                        hp_map.enabled,
                        hp_ptn in hostnameport_pattern_cache)
                    self. assertEqual(
                        hp_map.enabled and hp_map.proxy,
                        uses_proxy_route(b_url))
                    self.assertEqual(
                        hp_map.enabled and hp_map.proxy,
                        hp_ptn in hostnameport_pattern_proxy_cache)
                else:
                    self.assertFalse(uses_proxy_route(b_url))

                # Verify sync_https_adapters()
                # Note: Syncing for adapters tested in testSslContextSession
                #       Here we test for syncing of enabled, etc.
                try:
                    hp_adptr = https_client.get_adapter(
                        requests_base_url(b_url))
                except InvalidSchema:
                    hp_adptr = None

                if hp_map is not None:
                    # Note: enabling a hp mapping will NOT create an adapter;
                    #       this can only be done manually via
                    #       https_client.mount_sslcontext_adapter(), or by
                    #       creating a connection to an endpoint that has an
                    #       enabled mapping that matches
                    if hp_adptr is not None:
                        self.assertTrue(hp_map.enabled)
                else:
                    self.assertTrue(hp_adptr is None)

                # Verify sync_layer_legend_urls()
                link_url = base_models.Link.objects.get(pk=b + 1).url
                print('link_url: {0}'.format(link_url))
                if hp_map is not None:
                    # Note: legend graphics URL should always be proxied, if
                    #       mapping is enabled, as JS viewers manage the link
                    #       themselves
                    self.assertEqual(hp_map.enabled,
                                     has_proxy_prefix(link_url))
                else:
                    self.assertFalse(has_proxy_prefix(link_url))

                # Verify sync_map_layers()
                map_lyr = maps_models.MapLayer.objects.get(pk=b + 1)
                self.assertFalse(has_proxy_prefix(map_lyr.ows_url))  # never
                src_params = json.loads(map_lyr.source_params)

                if hp_map is not None:
                    self.assertEqual(hp_map.enabled and hp_map.proxy,
                                     src_params['use_proxy'])
                else:
                    self.assertFalse(src_params['use_proxy'])

        base_specs = [
            {'match': True, 'proxy': True},    # services.arcgisonline.com
            {'match': True, 'proxy': True},    # mapproxy.bdless.test
            {'match': False, 'proxy': False},  # data-test.bdlessgeo.io
            {'match': False, 'proxy': False},  # //data-test.bdlessgeo.io
        ]
        # Test defaults of loaded data
        test_base_urls(base_urls, base_specs)

        # Edit mappings: en/disable and/or proxy, and move up/down, then retest
        #
        # self.hp_maps (hnp -> sslconfig patterns, in order)
        #     u'*.arcgisonline.com*'
        #     u'*.boundless.test*'
        #     u'*.*'

        # Flip just proxy
        arc_hp_map = self.hp_maps[0]
        arc_hp_map.proxy = False
        arc_hp_map.save()
        base_specs[0]['proxy'] = False
        test_base_urls(base_urls, base_specs)

        # Flip just enabled
        arc_hp_map.enabled = False
        arc_hp_map.save()
        base_specs[0]['match'] = False
        test_base_urls(base_urls, base_specs)

        # (proxy should be considered False, even if True, when map disabled)
        arc_hp_map.proxy = True
        arc_hp_map.save()
        base_specs[0]['proxy'] = True
        test_base_urls(base_urls, base_specs)

        # Enable wildcard (arc and data now match; all match some mapping)
        wild_hp_map.enabled = True
        wild_hp_map.proxy = True
        wild_hp_map.save()
        for i in range(0, len(base_specs)):
            for k in base_specs[i]:
                base_specs[i][k] = True
        test_base_urls(base_urls, base_specs)

        # Move wildcard up from bottom and disable mapproxy (matches all)
        wild_hp_map.move_up()  # auto-saves
        mp_hp_map = self.hp_maps[1]
        mp_hp_map.enabled = False
        mp_hp_map.save()
        for i in range(0, len(base_specs)):
            for k in base_specs[i]:
                base_specs[i][k] = True
        test_base_urls(base_urls, base_specs)

        # Move arc down from top and disable it (matches all)
        arc_hp_map.move_down()  # auto-saves
        arc_hp_map.enabled = False
        arc_hp_map.save()
        for i in range(0, len(base_specs)):
            for k in base_specs[i]:
                base_specs[i][k] = True
        test_base_urls(base_urls, base_specs)

        # Disable wildcard proxy (matches all)
        wild_hp_map.proxy = False
        wild_hp_map.save()
        for i in range(0, len(base_specs)):
            base_specs[i]['proxy'] = False
        test_base_urls(base_urls, base_specs)

        # Re-enable wildcard proxy (matches all)
        wild_hp_map.proxy = True
        wild_hp_map.save()
        for i in range(0, len(base_specs)):
            base_specs[i]['proxy'] = True
        test_base_urls(base_urls, base_specs)

        # Enable arc; disable wildcard (only arc should match)
        arc_hp_map.enabled = True
        arc_hp_map.save()
        wild_hp_map.enabled = False
        wild_hp_map.save()
        base_specs[0]['match'] = True
        base_specs[0]['proxy'] = True
        for i in range(1, len(base_specs)):
            for k in base_specs[i]:
                base_specs[i][k] = False
        test_base_urls(base_urls, base_specs)

        # Re-enable wildcard
        wild_hp_map.enabled = True
        wild_hp_map.save()
        for i in range(0, len(base_specs)):
            for k in base_specs[i]:
                base_specs[i][k] = True
        test_base_urls(base_urls, base_specs)

        # Delete wildcard (only arc should match, other mappings disabled)
        wild_hp_map.delete()
        for i in range(1, len(base_specs)):
            for k in base_specs[i]:
                base_specs[i][k] = False
        test_base_urls(base_urls, base_specs)


@pytest.mark.skip(reason="Because it can't auth to running exchange")
@pytest.mark.skipif(
    not has_mapproxy(),
    reason='Test requires mapproxy docker-compose container running')
class TestPkiServiceRegistration(PkiTestCase):

    def setUp(self):
        self.login()

    # Service.objects.all().delete()

    def testMapProxyRegistration(self):
        logger.debug("Service.objects:\n{0}"
                     .format(repr(Service.objects.all())))
        mp_service = self.mp_root + 'service'

        resp = self.client.post(
            reverse("register_service"),
            {'url': mp_service, 'type': enumerations.WMS}
        )
        self.assertIsNotNone(resp)
        self.assertEqual(resp.status_code, 200)

        logger.debug("Service.objects:\n{0}"
                     .format(repr(Service.objects.all())))
        wms_srv = Service.objects.get(base_url=mp_service)
        self.assertEqual(wms_srv.base_url, mp_service)
        self.assertEqual(wms_srv.online_resource, mp_service)
        self.assertEqual(wms_srv.type, enumerations.WMS)
        self.assertEqual(wms_srv.method, enumerations.INDEXED)
        self.assertEqual(wms_srv.name, 'mapproxymapproxy-wms-proxy')


@pytest.mark.skipif(
    not has_mapproxy(),
    reason='Test requires mapproxy docker-compose container running')
class TestPkiRequest(PkiTestCase):

    def setUp(self):
        self.login()
        HostnamePortSslConfig.objects.all().delete()

    def tearDown(self):
        HostnamePortSslConfig.objects.all().delete()

    def test_crypto(self):
        c = Crypto()
        data = 'abcd'
        self.assertEqual(c.decrypt(c.encrypt(data)), data)
        udata = u'abcd'
        self.assertEqual(c.decrypt(c.encrypt(udata)), data)
        udata = u'abcd'
        self.assertEqual(c.decrypt(c.encrypt(udata)), data)
        accdata = 'çéàè↓'
        self.assertEqual(c.decrypt(c.encrypt(accdata)), accdata)
        uaccdata = u'çéàè↓'
        self.assertEqual(c.decrypt(c.encrypt(uaccdata)), accdata)

    def test_default_config(self):
        config_1 = SslConfig.objects.get(pk=1)
        self.assertEqual(config_1, SslConfig.default_ssl_config())
        del config_1

        # Simulate admin removing it
        SslConfig.objects.get(pk=1).delete()
        with self.assertRaises(SslConfig.DoesNotExist):
            SslConfig.objects.get(pk=1)

        # Re-add default
        SslConfig.objects.create_default()
        config_1 = SslConfig.objects.get_create_default()
        self.assertEqual(config_1, SslConfig.default_ssl_config())

        config_1.https_retries = False
        config_1.save()
        host_port_map = HostnamePortSslConfig(
            hostname_port=self.mp_host_port,
            ssl_config=config_1)
        host_port_map.save()
        with self.assertRaises(SSLError):
            # Default should not work for mapproxy PKI
            https_client.get(self.mp_root)

        host_port_map = HostnamePortSslConfig(
            hostname_port='example.com',
            ssl_config=config_1)
        host_port_map.save()
        res = https_client.get('https://example.com')
        self.assertEqual(res.status_code, 200)

    def test_no_client(self):
        self.create_hostname_port_mapping(2)
        res = https_client.get(self.mp_root)
        # Nginx non-standard status code 400 is for no client cert supplied
        self.assertEqual(res.status_code, 400)

    def test_client_no_password(self):
        self.create_hostname_port_mapping(3)
        res = https_client.get(self.mp_root)
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.mp_txt, res.content.decode("utf-8"))

    def test_client_and_password(self):
        self.create_hostname_port_mapping(4)
        res = https_client.get(self.mp_root)
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.mp_txt, res.content.decode("utf-8"))

    def test_client_and_password_alt_root(self):
        self.create_hostname_port_mapping(5)
        res = https_client.get(self.mp_root)
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.mp_txt, res.content.decode("utf-8"))

    def test_client_and_password_tls12_only(self):
        self.create_hostname_port_mapping(6)
        res = https_client.get(self.mp_root)
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.mp_txt, res.content.decode("utf-8"))

    def test_no_client_no_validation(self):
        self.create_hostname_port_mapping(7)
        res = https_client.get(self.mp_root)
        self.assertEqual(res.status_code, 200)

    def test_client_no_password_tls12_only_ssl_opts(self):
        self.create_hostname_port_mapping(8)
        res = https_client.get(self.mp_root)
        self.assertEqual(res.status_code, 200)

    @pytest.mark.skip(reason="Because it's fixture loading needs fixed")
    def test_pki_request_correct_url(self):
        # client and password to access mapproxy
        self.create_hostname_port_mapping(4)
        response = self.client.get(pki_route(self.mp_root))
        self.assertEqual(response.status_code, 200)
        default_mp_response = 'Welcome to MapProxy'
        self.assertIn(default_mp_response, response.content.decode("utf-8"))

    def test_pki_request_incorrect_url(self):
        incorrect_url = 'https://mapproxy.boundless.test:8044/service'
        with pytest.raises(Exception):
            self.client.get(pki_route(incorrect_url))

    def test_pki_request_missing_url(self):
        pki_root = '/pki/'
        response = self.client.get(pki_root)
        missing_url_response = 'Resource URL missing for PKI request'
        self.assertEqual(response.status_code, 400)
        self.assertIn(missing_url_response, response.content.decode("utf-8"))


@pytest.mark.skipif(
    not has_mapproxy(),
    reason='Test requires mapproxy docker-compose container running')
class TestGeoNodeProxy(PkiTestCase):
    def setUp(self):
        self.login()

    @pytest.mark.skip(reason="Because it's fixture loading needs fixed")
    def test_proxy_request_correct_url(self):
        proxy_root = '/proxy/?url='
        response = self.client.get(proxy_root + quote(self.mp_root))
        self.assertEqual(response.status_code, 200)
        default_mp_response = '<ServiceException>unknown WMS request type'
        self.assertIn(default_mp_response, response.content.decode("utf-8"))

    def test_proxy_request_incorrect_url(self):
        proxy_root = '/proxy/?url='
        incorrect_url = 'https://mapproxy.boundless.test:8044/service'
        with pytest.raises(Exception):
            self.client.get(proxy_root + quote(incorrect_url))

    # Patch pki_request so we can tell if proxy rerouted to it
    # noinspection PyUnusedLocal
    @staticmethod
    def mock_pki_request(**kwargs):
        return HttpResponse("Mock pki request response",
                            status=302,
                            content_type="text/plain")

    @pytest.mark.skip(reason="Because it's fixture loading needs fixed")
    @mock.patch("ssl_pki.views.pki_request", side_effect=mock_pki_request)
    def test_proxy_reroute(self, mock_pki_request):
        proxy_root = '/proxy/?url='
        response = self.client.get(proxy_root + quote(self.mp_root))
        # response should have gotten the mock_pki_request response
        self.assertEqual(response.status_code,
                         mock_pki_request.return_value.status_code)
        self.assertEqual(response.content,
                         mock_pki_request.return_value.content)

    @mock.patch("ssl_pki.views.pki_request", side_effect=mock_pki_request)
    def test_proxy_no_reroute(self, mock_pki_request):
        proxy_root = '/proxy/?url='
        response = self.client.get(proxy_root + quote(self.mp_root_http))
        self.assertNotEqual(response.status_code,
                            mock_pki_request.return_value.status_code)
        self.assertNotEqual(response.content,
                            mock_pki_request.return_value.content)


# TODO: Is this the correct place to test service handler?
class TestPkiServiceHandler(PkiTestCase):
    def setUp(self):
        self.login()
        HostnamePortSslConfig.objects.all().delete()
        self.create_hostname_port_mapping(6)
        self.service_name = 'data-test'

    def tearDown(self):
        HostnamePortSslConfig.objects.all().delete()

    # TODO: This may not be due to the missing fixtures, need to verify
    @pytest.mark.skip(reason="Fails due to XMLError with WMS Service Handler")
    def test_handler_contains_header(self):
        from geonode.services.serviceprocessors.handler \
            import get_service_handler
        test_key = 'test_key'
        test_header = {test_key: 'test_value'}
        import pdb
        pdb.set_trace()
        service = get_service_handler(
            self.mp_root,
            enumerations.WMS,
            test_header
        )
        self.assertIn('PKI_SERVICE_TYPE', service.parsed_service.headers)
        self.assertIn('Authorization', service.parsed_service.headers)
        self.assertIn(test_key, service.parsed_service.headers)
        # TODO: Can arcrest serivce headers be tested as well?

    @pytest.mark.skip(reason="Fails due to XMLError with WMS Service Handler")
    @mock.patch("geonode.services.models.Service", autospec=True)
    def test_non_pki_handler_contains_bearer_token(self, mock_service):
        from geonode.services.views import _get_service_handler
        request = RequestFactory().get('/layers/geonode:testlayer/')
        request.session = []
        # need a mock service
        mock_service.base_url = self.mp_root
        mock_service.type = 'WMS'
        mock_service.name = self.service_name
        service = _get_service_handler(request, mock_service)
        self.assertIn('Authorization', service.parsed_service.headers)

    @pytest.mark.skip(reason="Fails due to XMLError with WMS Service Handler")
    def test_handler_contains_pki_url(self):
        from geonode.services.serviceprocessors.handler \
            import get_service_handler
        wms_service = get_service_handler(self.mp_root, enumerations.WMS)
        self.assertIsNotNone(wms_service.pki_url)
        self.assertIsNotNone(wms_service.pki_proxy_url)
        arcrest_service = get_service_handler(self.mp_root, enumerations.REST)
        self.assertIsNotNone(arcrest_service.pki_url)
        self.assertIsNotNone(arcrest_service.pki_proxy_url)


class TestPkiUtils(PkiTestCase):

    def setUp(self):
        mproot = self.mp_root.rstrip('/').lower()
        mphostpport = self.mp_host_port
        ex_local_url = settings.EXCHANGE_LOCAL_URL.rstrip('/')
        site_url = settings.SITEURL.rstrip('/')

        self.base_url = \
            '{0}/service?version=1.1.1&service=WMS'.format(mproot)
        self.protocol_relative_url = \
            '//{0}/service?version=1.1.1&service=WMS'\
            .format(mphostpport)
        self.pki_url = \
            '{0}/pki/{1}/service%3Fversion%3D1.1.1%26service%3DWMS'\
            .format(ex_local_url, quote(mphostpport))
        self.pki_site_url = \
            '{0}/pki/{1}/service%3Fversion%3D1.1.1%26service%3DWMS'\
            .format(site_url, quote(mphostpport))
        self.proxy_url = \
            '{0}/proxy/?url={1}%2Fservice%3Fversion%3D1.1.1%26service%3DWMS'\
            .format(site_url, quote_plus(mproot))

        logging.debug("base_url: {0}".format(self.base_url))
        logging.debug("pki_url: {0}".format(self.pki_url))
        logging.debug("pki_site_url: {0}".format(self.pki_site_url))
        logging.debug("proxy_url: {0}".format(self.proxy_url))

    def test_routes(self):
        # has
        self.assertTrue(has_pki_prefix(pki_prefix()))
        self.assertTrue(has_pki_prefix(pki_site_prefix()))
        self.assertTrue(has_pki_prefix(self.pki_url))
        self.assertTrue(has_pki_prefix(self.pki_site_url))
        self.assertTrue(has_proxy_prefix(self.proxy_url))

        # to
        self.assertEqual(self.pki_url,
                         pki_route(self.base_url))
        self.assertEqual(self.pki_site_url,
                         pki_route(self.base_url, site=True))
        self.assertEqual(self.proxy_url,
                         proxy_route(self.base_url))

        # from
        self.assertEqual(self.base_url,
                         pki_route_reverse(self.pki_url))
        self.assertEqual(self.base_url,
                         pki_route_reverse(self.pki_site_url))
        self.assertEqual(self.base_url,
                         proxy_route_reverse(self.proxy_url))

        # convert
        self.assertEqual(self.proxy_url,
                         pki_to_proxy_route(self.pki_url))
        self.assertEqual(self.proxy_url,
                         pki_to_proxy_route(self.pki_site_url))

        # noop
        self.assertEqual(self.base_url,
                         pki_route_reverse(self.base_url))
        self.assertEqual(self.base_url,
                         proxy_route_reverse(self.base_url))

        # chained
        self.assertEqual(
            self.base_url,
            pki_route_reverse(pki_route(self.base_url)))
        self.assertEqual(
            self.base_url,
            pki_route_reverse(pki_route(self.base_url, site=True)))
        self.assertEqual(
            self.base_url,
            proxy_route_reverse(proxy_route(self.base_url)))
        self.assertEqual(
            self.base_url,
            proxy_route_reverse(pki_to_proxy_route(pki_route(self.base_url))))

    def test_urls(self):
        self.assertTrue(protocol_relative_url(self.protocol_relative_url))
        self.assertEqual(
            self.base_url,
            protocol_relative_to_scheme(self.protocol_relative_url))
        self.assertEqual(
            self.base_url,
            protocol_relative_to_scheme(self.base_url))
        self.assertNotEqual(
            self.base_url,
            protocol_relative_to_scheme(self.protocol_relative_url,
                                        scheme='http'))
        self.assertEqual(
            self.base_url,
            relative_to_absolute_url(self.protocol_relative_url))
        self.assertNotEqual(
            self.base_url,
            relative_to_absolute_url(self.protocol_relative_url,
                                     scheme='http'))
        self.assertEqual(
            self.base_url,
            relative_to_absolute_url(self.base_url))


class TestPkiValidation(TestCase):

    def test_pki_functions(self):
        # pki_dir_path
        for k in (
                'alice-cert.pem',
                'bad_alice-cert_unsupported.der',
        ):
            pki_f = pki_dir_path(k)
            self.assertTrue(pki_f.startswith(get_pki_dir()))

            pki_f2 = pki_file(k)
            self.assertEqual(pki_f, pki_f2)
            pki_f3 = pki_dir_path(pki_f2)
            self.assertEqual(pki_f2, pki_f3)

        # pki_file_exists_readable
        for k in (
            'alice-cert.pem',
            'bad_alice-cert_unsupported.der',
        ):
            self.assertTrue(pki_file_exists_readable(k))

        self.assertFalse(pki_file_exists_readable('blah.pem'))

        # pki_file_contents
        alice_key = b"""-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDUCocRWKuiSAent74zw+HQVUA1cWIgp9odE/oawgE8kyx3dCX3
o/CR1mqfG9vCcFW0vCBBiJmVJv5W3EBIjKpW5yiPoOJqqzQihkNdwoFi+vRO7370
liEjoHwFN+V0S0/UqCT4TKnZLk5HslEp+ekbh9PdBHkS//7rDM47F+PtAQIDAQAB
AoGBAKNknWIjhtadVLDL6RgwmGCWYM0N2wS481022KIn3xYTfs9pxBwIy0dGB5El
wXkaYSDNWrnFDjwd+R1ryWleY579+4qSYAkRl0m0HG0aaj0kws1Rg1obJLYFVlVj
UEEaaD4ynGpf4PBdZVRD1bo5rgTZKQOM7tNKKOmKoIk76mwVAkEA9zqT6SUtcsrT
DjhxszXzG9umEZoOolNLu8bgB1RXVrDmPeeYsjfD541toeAsH1/19vCeRQeptJVz
NHhm3aovjwJBANuQXMNW7NMbRgh5TZEVvG6DvG/4VeSknA0Y5LipYeId0Mf59UkM
PIfWoss4rXBTENZKdzv4ouavklv+B/OK0m8CQQCCG8ffuPsUIH22TCo6QDgy/wOE
2+i7sM54gg9AjDhynSJujcWkdQiagamiuVE/KcdOMA97EK9VJBm/EWZBXeEtAkAb
9gR6M+Ww9LY0eg4wvc3jXQ9wSvXVSkk9OcBW6+s1OorODLz58n765ZCRxMQBm/J2
98C7eGx2aEGBSZaFo1YtAkBNAc/tTQGvUblf3ZuaF3mg5oMhzwAk9oj+8YzXrlY9
MPrd0MBerM5NERa+58Jn87K7a3h0TgSIQ5N8ypXHTi3H
-----END RSA PRIVATE KEY-----
"""
        alice_key_contents = pki_file_contents('alice-key.pem')
        self.assertEqual(alice_key, alice_key_contents)

        blah_contents = pki_file_contents('blah.pem')
        self.assertEqual(b'', blah_contents)

        # acceptable_format
        for k in (
            'root-root2-chains.pem',
            'alice-key.pem',
            'alice-cert.pem',
            'bad_marinus-key_pkcs8.pem',
        ):
            self.assertTrue(pki_acceptable_format(pki_file_contents(k)))

        for k in (
            'bad_alice-cert_unsupported.der',
            'blah.pem',
        ):
            self.assertFalse(pki_acceptable_format(pki_file_contents(k)))

        # cert_date_not_yet_valid
        for k in (
            'root-root2-chains.pem',
            'alice-cert.pem',
        ):
            self.assertFalse(cert_date_not_yet_valid(pki_file_contents(k)))

        for k in (
            'bad_jane-client_not-yet.pem',
            'blah.pem',
        ):
            self.assertTrue(cert_date_not_yet_valid(pki_file_contents(k)))

        # cert_date_expired
        for k in (
            'root-root2-chains.pem',
            'alice-cert.pem',
        ):
            self.assertFalse(cert_date_expired(pki_file_contents(k)))

        for k in (
            'bad_marinus-cert_expired.pem',
            'bad_Google-IA-G2_expired-CA.pem',
        ):
            self.assertTrue(cert_date_expired(pki_file_contents(k)))

        # is_ca_cert
        for k in (
            'root-root2-chains.pem',
            'bad_Google-IA-G2_expired-CA.pem',
        ):
            self.assertTrue(is_ca_cert(pki_file_contents(k)))

        for k in (
            'alice-cert.pem',
            'blah.pem',
        ):
            self.assertFalse(is_ca_cert(pki_file_contents(k)))

        # is_client_cert
        for k in (
            'alice-cert.pem',
            'bad_marinus-cert_expired.pem',
        ):
            self.assertTrue(is_client_cert(pki_file_contents(k)))

        for k in (
            'root-root2-chains.pem',
            'bad_Google-IA-G2_expired-CA.pem',
            'blah.pem',
        ):
            self.assertFalse(is_client_cert(pki_file_contents(k)))

    def test_pki_load_functions(self):
        # load_certs
        certs = load_certs(
            pki_file_contents('alice-cert.pem')
        )[0]
        self.assertEqual(len(certs), 1)
        certs = load_certs(
            pki_file_contents('alice-key.pem')
        )[0]
        self.assertEqual(len(certs), 0)
        certs = load_certs(
            pki_file_contents('root-root2-chains.pem')
        )[0]
        self.assertEqual(len(certs), 5)
        certs = load_certs(
            pki_file_contents('blah.pem')
        )[0]
        self.assertEqual(len(certs), 0)

        certs, msgs = load_certs(
            pki_file_contents('bad_certs_one-bad.pem')
        )
        self.assertEqual(len(certs), 1)
        self.assertTrue(len(msgs) == 1)
        # logging.debug('msgs: {0}'.format(msgs))

        # load_first_cert
        cert = load_first_cert(
            pki_file_contents('alice-cert.pem')
        )
        self.assertTrue(hasattr(cert, 'public_bytes'))
        cert = load_first_cert(
            pki_file_contents('bad_certs_one-bad.pem')
        )
        self.assertTrue(hasattr(cert, 'public_bytes'))

        cert = load_first_cert(
            pki_file_contents('alice-key.pem')
        )
        self.assertIsNone(cert)
        cert = load_first_cert(
            pki_file_contents('blah.pem')
        )
        self.assertIsNone(cert)

        # cert_subject_common_name
        cert = load_first_cert(
            pki_file_contents('alice-cert.pem')
        )
        self.assertEqual(cert_subject_common_name(cert), 'alice')

        # load_private_key
        priv_key = load_private_key(
            pki_file_contents('alice-key.pem')
        )
        self.assertTrue(hasattr(priv_key, 'private_bytes'))
        priv_key2 = load_private_key(
            pki_file_contents('alice-key_w-pass.pem'),
            password=b'password'
        )
        self.assertTrue(hasattr(priv_key2, 'private_bytes'))
        # password not in bytes should be converted
        priv_key3 = load_private_key(
            pki_file_contents('alice-key_w-pass.pem'),
            password=u'password'
        )
        self.assertTrue(hasattr(priv_key3, 'private_bytes'))
        # PKCS#8 format, instead of OpenSSL 'traditional'
        priv_key4 = load_private_key(
            pki_file_contents('bad_marinus-key_pkcs8.pem'),
            password=b'password'
        )
        self.assertTrue(hasattr(priv_key4, 'private_bytes'))

        with self.assertRaises(PkiValidationError):
            # not a private key
            load_private_key(
                pki_file_contents('alice-cert.pem')
            )
        with self.assertRaises(PkiValidationError):
            # password needed, but not supplied
            load_private_key(
                pki_file_contents('alice-key_w-pass.pem')
            )
        with self.assertRaises(PkiValidationError):
            # password defined, but key not encrypted
            load_private_key(
                pki_file_contents('alice-key.pem'),
                password=b'password'
            )
        with self.assertRaises(PkiValidationError):
            # just plain bad key (line removed)
            load_private_key(
                pki_dir_path('bad_jane-key.pem')
            )

    def test_pki_validations(self):
        # validate_cert_matches_private_key
        validate_cert_matches_private_key(
            pki_file_contents('alice-cert.pem'),
            pki_file_contents('alice-key_w-pass.pem'),
            password=b'password'
        )
        with self.assertRaises(PkiValidationError):
            validate_cert_matches_private_key(
                pki_file_contents('jane-cert.pem'),
                pki_file_contents('alice-key_w-pass.pem'),
                password=b'password'
            )
        with self.assertRaises(PkiValidationError):
            validate_cert_matches_private_key(
                pki_file_contents('alice-cert.pem'),
                pki_file_contents('alice-key_w-pass.pem'),
                password=b''
            )
        # first cert or bad_certs_one-bad.pem is alice-cert.pem
        msgs = validate_cert_matches_private_key(
            pki_file_contents('bad_certs_one-bad.pem'),
            pki_file_contents('alice-key_w-pass.pem'),
            password=b'password'
        )
        self.assertTrue(len(msgs) == 1)
        # logging.debug('msgs: {0}'.format(msgs))

        # validate_cert_file_matches_key_file
        validate_cert_file_matches_key_file(
            'alice-cert.pem',
            'alice-key_w-pass.pem',
            password=b'password'
        )

        # validate_ca_certs
        msgs = validate_ca_certs(
            pki_dir_path('root-root2-chains.pem'),
            allow_expired=False
        )
        self.assertTrue(len(msgs) == 0)

        with self.assertRaises(PkiValidationError) as e:
            validate_ca_certs(
                pki_dir_path('bad_Google-IA-G2_expired-CA.pem'),
                allow_expired=False
            )
        err = e.exception
        self.assertIn(u'are expired', err.message)

        msgs = validate_ca_certs(
            pki_dir_path('bad_Google-IA-G2_expired-CA.pem'),
            allow_expired=True
        )
        self.assertTrue(len(msgs) == 1)
        self.assertIn(u'are expired', msgs[0])

        with self.assertRaises(PkiValidationError) as e:
            validate_ca_certs(
                pki_dir_path('blah.pem'),
                allow_expired=True
            )
        err = e.exception
        self.assertIn('can not be located', err.message)

        # validate_client_cert
        msgs = validate_client_cert(
            pki_dir_path('alice-cert.pem')
        )
        self.assertTrue(len(msgs) == 0)

        with self.assertRaises(PkiValidationError) as e:
            validate_client_cert(
                pki_dir_path('blah.pem')
            )
        err = e.exception
        self.assertIn('can not be located', err.message)

        with self.assertRaises(PkiValidationError) as e:
            validate_client_cert(
                pki_dir_path('bad_alice-cert_unsupported.der')
            )
        err = e.exception
        self.assertIn('not in acceptable format', err.message)

        with self.assertRaises(PkiValidationError) as e:
            validate_client_cert(
                pki_dir_path('root-root2-chains.pem')
            )
        err = e.exception
        self.assertIn('no readable client certs', err.message)

        msgs = validate_client_cert(
            pki_dir_path('bad_multiple-client-certs.pem')
        )
        self.assertTrue(len(msgs) == 1)
        self.assertIn('multiple client certs', msgs[0])

        with self.assertRaises(PkiValidationError) as e:
            validate_client_cert(
                pki_dir_path('bad_marinus-cert_expired.pem'),
            )
        err = e.exception
        self.assertIn('is expired', err.message)

        # validate_client_key
        msgs = validate_client_key(
            pki_dir_path('alice-key.pem')
        )
        self.assertTrue(len(msgs) == 0)

        msgs = validate_client_key(
            pki_dir_path('alice-key_w-pass.pem'),
            password=b'password'
        )
        self.assertTrue(len(msgs) == 0)

        # password not in bytes should be converted
        msgs = validate_client_key(
            pki_dir_path('alice-key_w-pass.pem'),
            password=u'password'
        )
        self.assertTrue(len(msgs) == 0)

        # PKCS#8 format, instead of OpenSSL 'traditional'
        msgs = validate_client_key(
            pki_dir_path('bad_marinus-key_pkcs8.pem'),
            password=b'password'
        )
        self.assertTrue(len(msgs) == 0)

        with self.assertRaises(PkiValidationError):
            # not a private key
            validate_client_key(
                pki_dir_path('alice-cert.pem')
            )
        with self.assertRaises(PkiValidationError):
            # password needed, but not supplied
            validate_client_key(
                pki_dir_path('alice-key_w-pass.pem')
            )
        with self.assertRaises(PkiValidationError):
            # password defined, but key not encrypted
            validate_client_key(
                pki_dir_path('alice-key.pem'),
                password=b'password'
            )
        with self.assertRaises(PkiValidationError):
            # just plain bad key (line removed)
            validate_client_key(
                pki_dir_path('bad_jane-key.pem')
            )
