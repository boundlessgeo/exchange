#########################################################################
#
# Copyright (C) 2017 OSGeo, (C) 2018 Boundless Spatial
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

"""Utilities for enabling ESRI REST Mapserver remote services in geonode."""

from geonode.services.serviceprocessors.mapserver \
    import MapserverServiceHandler
from geonode.services.serviceprocessors.mapserver import _get_valid_name
import logging
from arcrest.ags import MapService as ArcMapService
from geonode.services.enumerations import CASCADED, INDEXED
from geonode.layers.utils import create_thumbnail
from geonode.base.models import Link
from django.conf import settings

try:
    if 'ssl_pki' not in settings.INSTALLED_APPS:
        raise ImportError
    from ssl_pki.utils import (
        has_pki_prefix,
        pki_to_proxy_route,
        pki_route_reverse,
        proxy_route
    )
except ImportError:
    has_pki_prefix = None
    pki_to_proxy_route = None
    pki_route_reverse = None
    proxy_route = None

logger = logging.getLogger(__name__)


class ExchangeMapserverServiceHandler(MapserverServiceHandler):
    """Remote service handler for OGC WMS services"""

    def __init__(self, url, **kwargs):
        headers = kwargs.pop('headers', None)
        logger.debug('passed headers = {0}'.format(headers))

        self.parsed_service = ArcMapService(url, add_headers=headers)
        self.indexing_method = (
            INDEXED if self._offers_geonode_projection() else CASCADED)
        self.url = self.parsed_service.url
        self.pki_proxy_url = None
        self.pki_url = None
        if callable(has_pki_prefix) and has_pki_prefix(self.url):
            self.pki_url = self.url
            self.pki_proxy_url = pki_to_proxy_route(self.url)
            self.url = pki_route_reverse(self.url)
        self.title = self.parsed_service.itemInfo['title']
        self.name = _get_valid_name(self.parsed_service.itemInfo['name'])

    def _create_layer_thumbnail(self, geonode_layer):
        """Grab the image from the service."""

        thumbnail_remote_url = "{}/info/thumbnail".format(self.url)
        logger.debug("thumbnail_remote_url: {}".format(thumbnail_remote_url))
        thumbnail_create_url = "{}/info/thumbnail".format(
            self.pki_url or self.url)
        logger.debug("thumbnail_remote_url: {}".format(thumbnail_create_url))
        create_thumbnail(
            instance=geonode_layer,
            thumbnail_remote_url=thumbnail_remote_url,
            thumbnail_create_url=thumbnail_create_url,
            check_bbox=False,
            overwrite=True,
        )

    def _create_layer_legend_link(self, geonode_layer):
        """Get the layer's legend and save it locally

        Regardless of the service being INDEXED or CASCADED we're always
        creating the legend by making a request directly to the original
        service.

        """

        legend_url = "{}/legend?f=pjson".format(self.url)
        if self.pki_url is not None:
            legend_url = proxy_route(legend_url)

        logger.debug("legend_url: {}".format(legend_url))
        Link.objects.get_or_create(
            resource=geonode_layer.resourcebase_ptr,
            url=legend_url,
            defaults={
                "extension": 'json',
                "name": 'Legend',
                "url": legend_url,
                "mime": 'application/json',
                "link_type": 'data',
            }
        )
