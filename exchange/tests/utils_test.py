from . import ExchangeTest
import mock
import json
from django.conf import settings


class DefaultMapConfigTest(ExchangeTest):

    def mock_proxy_route(*args):
        return True

    @mock.patch("geonode.utils.uses_proxy_route",
                side_effect=mock_proxy_route)
    @mock.patch("geonode.services.serviceprocessors.base.settings",
                autospec=True)
    def test_proxy_base_map(self, mock_service_settings, mock_proxy_route):
        mock_service_settings.PROXY_BASEMAP = True
        # TODO: Is there a way to mock this instead?
        settings.MAP_BASELAYERS = [{
            # We're mocking return value, but the url string needs to exist
            "source": {"ptype": "gxp_olsource", "url": "exists"},
            "type": "OpenLayers.Layer",
            "args": ["No background"],
            "name": "background",
            "visibility": False,
            "fixed": True,
            "group":"background",
        }]
        from geonode.utils import default_map_config
        map_config, base_layers = default_map_config(None)
        self.assertTrue(json.loads(base_layers[0].source_params)['use_proxy'])
