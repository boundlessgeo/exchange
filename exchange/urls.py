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
from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from geonode.urls import urlpatterns as geonode_urls
from exchange.maploom.urls import urlpatterns as maploom_urls
from fileservice.urls import urlpatterns as fileservice_urls
from thumbnails.urls import urlpatterns as thumbnail_urls
from elasticsearch_app.urls import urlpatterns as search_urls
from . import views

js_info_dict = {
    'packages': ('geonode.layers',),
}

urlpatterns = patterns(
    '',
    url(r'^/?$', views.home_screen, name='home'),
    url(r'^layers/(?P<layername>[^/]*)/metadata_detail$',
        views.layer_metadata_detail, name='layer_metadata_detail'),
    url(r'^layers/(?P<layername>[^/]*)/publish$',
        views.layer_publish, name='layer_publish'),
    url(r'^maps/(?P<mapid>[^/]*)/metadata_detail$', views.map_metadata_detail,
        name='map_metadata_detail'),
    url(r'^wfsproxy/', views.geoserver_reverse_proxy,
        name='geoserver_reverse_proxy'),
    # Redirect help and developer links to the documentation page
    url(r'^help/$', views.documentation_page, name='help'),
    url(r'^developer/$', views.documentation_page, name='developer'),

    url(r'^services/(?P<pk>\d+)/publish$',
        views.publish_service, name='publish_service'),

    url(r'^auth-failed/', views.AuthErrorPage.as_view(), name='auth_failed'),
    url(r'^about/', views.about_page, name='about'),
    url(r'^capabilities/', views.capabilities, name='capabilities'),
    url(r'^logout/', views.logout, name='exchange_logout'),

    url(r'^maps/new$', views.new_map, name="new_map"),
    url(r'^maps/new/data$', views.new_map_json, name='new_map_json'),

    url(r'^proxy/', views.proxy),

    (r'^services/', include('exchange.remoteservices.urls')),
)

if 'ssl_pki' in settings.INSTALLED_APPS:
    from ssl_pki.urls import urlpatterns as pki_urls
    urlpatterns += pki_urls

if settings.ENABLE_SOCIAL_LOGIN is True:
    urlpatterns += [
        url('', include('social_django.urls', namespace='social'))
    ]

if settings.ENABLE_SOCIAL_LOGIN is True and settings.ANYWHERE_ENABLED is True:
    urlpatterns += [
        url(r'^register-by-token/(?P<backend>[^/]+)/$',
            views.register_by_access_token)
    ]

# If django-osgeo-importer is enabled...
if 'osgeo_importer' in settings.INSTALLED_APPS:
    # Replace the default Exchange 'layers/upload'
    from osgeo_importer.views import FileAddView
    urlpatterns += [
        url(
            r'^layers/upload$',
            login_required(FileAddView.as_view()),
            name='layer_upload'
        )
    ]
    # Add django-osgeo-importer URLs
    from osgeo_importer.urls import urlpatterns as osgeo_importer_urls
    urlpatterns += osgeo_importer_urls

# Layer detail override needs to come after the layer upload override
urlpatterns += [
    url(r'^layers/(?P<layername>[^/]*)$',
        views.layer_detail, name="layer_detail"),
]

if 'nearsight' in settings.INSTALLED_APPS:
    from nearsight.urls import urlpatterns as nearsight_urls
    urlpatterns += nearsight_urls

# Use our Elasticsearch implementation for search
urlpatterns += [url('', include(search_urls)), ]

if 'geonode_anywhere' in settings.INSTALLED_APPS:
    urlpatterns += [url(r"^anywhere/", include("geonode_anywhere.urls")), ]

if 'worm' in settings.INSTALLED_APPS:
    urlpatterns += [url(r"^services/", include("worm.urls")), ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += geonode_urls
urlpatterns += fileservice_urls
urlpatterns += thumbnail_urls
urlpatterns += maploom_urls

handler500 = 'exchange.views.handler500'
