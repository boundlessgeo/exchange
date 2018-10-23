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

from django.conf import settings
from exchange.version import get_version
import logging
from urlparse import urlparse

logger = logging.getLogger(__name__)

if settings.GEOQUERY_ENABLED:
    if settings.GEOQUERY_URL is None:
        logger.warn('No search endpoint defined.')
        logger.warn(
            'GEOQUERY_ENABLED was set to True, but GEOQUERY_URL '
            'was not defined.')
    elif urlparse(settings.GEOQUERY_URL).netloc is '':
        logger.warn(
            'GEOQUERY_URL improperly defined or is not a valid URL.')


def resource_variables(request):
    """Global exchange values to pass to templates"""
    defaults = dict(
        VERSION=get_version(),
        MAP_CRS=getattr(settings, 'DEFAULT_MAP_CRS', None),
        ENABLE_SOCIAL_LOGIN=getattr(settings, 'ENABLE_SOCIAL_LOGIN', False),
        ENABLE_GOOGLE_LOGIN=getattr(settings, 'ENABLE_GOOGLE_LOGIN', False),
        ENABLE_FACEBOOK_LOGIN=getattr(
            settings, 'ENABLE_FACEBOOK_LOGIN', False),
        ENABLE_GEOAXIS_LOGIN=getattr(settings, 'ENABLE_GEOAXIS_LOGIN', False),
        ENABLE_AUTH0_LOGIN=getattr(settings, 'ENABLE_AUTH0_LOGIN', False),
        AUTH0_APP_NAME=getattr(
            settings, 'AUTH0_APP_NAME', 'Boundless Connect'),
        INSTALLED_APPS=set(settings.INSTALLED_APPS),
        GEOAXIS_ENABLED=getattr(settings, 'GEOAXIS_ENABLED', False),
        ENABLE_MICROSOFT_AZURE_LOGIN=getattr(settings,
                                             'ENABLE_MICROSOFT_AZURE_LOGIN',
                                             False),
        MAP_PREVIEW_LAYER=getattr(settings, 'MAP_PREVIEW_LAYER', "''"),
        LOCKDOWN_EXCHANGE=getattr(settings, 'LOCKDOWN_GEONODE', False),
        LOGIN_WARNING=getattr(settings, 'LOGIN_WARNING_ENABLED', False),
        LOGIN_WARNING_TEXT=getattr(settings, 'LOGIN_WARNING_TEXT', "''"),
        STORYSCAPES_ENABLED=getattr(settings, 'STORYSCAPES_ENABLED', False),
        NOMINATIM_ENABLED=getattr(settings, 'NOMINATIM_ENABLED', True),
        NOMINATIM_URL=getattr(
            settings, 'NOMINATIM_URL', '//nominatim.openstreetmap.org'),
        GEOQUERY_ENABLED=getattr(settings, 'GEOQUERY_ENABLED', False),
        GEOQUERY_URL=getattr(settings, 'GEOQUERY_URL', None),
        LOOM_STYLING_ENABLED=getattr(settings, 'LOOM_STYLING_ENABLED', False),
        EXTENT_FILTER_ENABLED=getattr(settings, 'EXTENT_FILTER_ENABLED', True),
        DISABLE_BOUNDLESS_LINK_IN_FOOTER=getattr(
            settings, 'DISABLE_BOUNDLESS_LINK_IN_FOOTER', False),
        MAP_CLIENT_USE_CROSS_ORIGIN_CREDENTIALS=getattr(
            settings, 'MAP_CLIENT_USE_CROSS_ORIGIN_CREDENTIALS', False
        ),
        ES_SEARCH=getattr(settings, 'ES_SEARCH', False),
        PROXY_BASEMAP=getattr(settings, 'PROXY_BASEMAP', False),
        GOOGLE_ANALYTICS_ID=getattr(settings, 'GOOGLE_ANALYTICS_ID', False),
    )

    return defaults
