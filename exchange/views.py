import requests
import logging
from django.conf import settings
from django.contrib.auth.models import Group
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from exchange.version import get_version
from geonode import get_version as get_version_geonode
from geonode.maps.views import _resolve_map, clean_config
from geonode.layers.views import _resolve_layer, _PERMISSION_MSG_METADATA
from geonode.base.models import TopicCategory
from guardian.shortcuts import assign_perm
from pip._vendor import pkg_resources
from exchange.tasks import create_record, delete_record
from django.core.urlresolvers import reverse, resolve
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from social_django.utils import psa
from geonode.utils import llbbox_to_mercator, bbox_to_projection
from geonode.utils import forward_mercator, build_social_links
from geonode.utils import default_map_config, GXPLayer, GXPMap
from geonode.utils import DEFAULT_TITLE, DEFAULT_ABSTRACT
from geonode.layers.models import Layer
from collections import OrderedDict
from guardian.shortcuts import get_perms
from geonode.security.views import _perms_info_json
from geonode.documents.models import get_related_documents
import uuid
import math
from urlparse import urlsplit, parse_qsl, urlunsplit
from django.http.request import validate_host
from urllib import quote
from django.utils.http import is_safe_url
from geonode.maps.models import Map, MapLayer, MapSnapshot
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from geonode.contrib.createlayer.utils import create_layer
from geonode.contrib.createlayer.forms import NewLayerForm
from django.utils.translation import ugettext as _
from geonode.people.models import Profile
from exchange.remoteservices.serviceprocessors.handler \
    import get_service_handler

if 'geonode.geoserver' in settings.INSTALLED_APPS:
    from geonode.geoserver.helpers import ogc_server_settings
    from geonode.geoserver.helpers import gs_catalog
else:
    ogc_server_settings = None
    gs_catalog = None
try:
    import json
except ImportError:
    from django.utils import simplejson as json

try:
    if 'ssl_pki' not in settings.INSTALLED_APPS:
        raise ImportError
    from ssl_pki.models import uses_proxy_route
    from ssl_pki.models import has_ssl_config
    from ssl_pki.views import pki_request
    from ssl_pki.utils import (
        protocol_relative_url,
        protocol_relative_to_scheme,
    )
except ImportError:
    uses_proxy_route = None
    has_ssl_config = None
    pki_request = None
    protocol_relative_url = None
    protocol_relative_to_scheme = None


logger = logging.getLogger(__name__)


#
#   url(r'^register-by-token/(?P<backend>[^/]+)/$',
#       'register_by_access_token')

@psa('social:complete')
def register_by_access_token(request, backend):
    provider = request.backend
    user = None
    error_message = {'error': 'Invalid Token'}
    try:
        if 'geonode_anywhere' in settings.INSTALLED_APPS:
            from geonode_anywhere.views import process_request
            token = process_request(request)
            user = provider.do_auth(token)

        if user:
            login(request, user)
            return JsonResponse({'access_token':
                                 request.session['access_token']})
        else:
            return JsonResponse(error_message)

    except Exception as e:
        logger.error(e)
        return JsonResponse(error_message)


def home_screen(request):
    categories = TopicCategory.objects.filter(is_choice=True).order_by('pk')
    return render(request, 'index.html', {'categories': categories})


def documentation_page(request):
    return HttpResponseRedirect('/static/docs/html/index.html')


def get_pip_version(project):
    version = [
        p.version for p in pkg_resources.working_set
        if p.project_name == project
    ]
    if version != []:
        pkg_version = version[0][:-8] if version[0][:-8] else version[0][-7:]
        commit_hash = version[0][-7:] if version[0][:-8] else version[0][:-8]
        return {'version': pkg_version, 'commit': commit_hash}
    else:
        return {'version': '', 'commit': ''}


def get_geoserver_version():
    try:
        ogc_server = settings.OGC_SERVER['default']
        geoserver_url = '{}/rest/about/version.json'.format(
            ogc_server['LOCATION'].strip('/'))
        resp = requests.get(
            geoserver_url, auth=(ogc_server['USER'], ogc_server['PASSWORD']))
        version = resp.json()['about']['resource'][0]
        return {'version': version['Version'],
                'commit': version['Git-Revision'][:7]}
    except:  # noqa
        return {'version': '', 'commit': ''}


def get_exchange_version():
    exchange_version = get_pip_version('geonode-exchange')
    if not exchange_version['version'].strip():
        version = get_version()
        pkg_version = version[:-8] if version[:-8] else version[-7:]
        commit_hash = version[-7:] if version[:-8] else version[:-8]
        return {'version': pkg_version, 'commit': commit_hash}
    else:
        return exchange_version


def get_geonode_version():
    geonode_version = get_pip_version('GeoNode')
    if not geonode_version['version'].strip():
        version = get_version_geonode().split('.')
        pkg_version = '{0}.{1}.{2}'.format(version[0], version[1], version[2])
        commit_hash = version[3]
        return {'version': pkg_version, 'commit': commit_hash}
    else:
        return geonode_version


def about_page(request, template='about.html'):
    exchange_version = get_exchange_version()
    geoserver_version = get_geoserver_version()
    geonode_version = get_geonode_version()
    maploom_version = get_pip_version('django-exchange-maploom')
    importer_version = get_pip_version('django-osgeo-importer')
    react_version = get_pip_version('django-geonode-client')

    projects = [{
        'name': 'Boundless Exchange',
        'website': 'https://boundlessgeo.com/boundless-exchange/',
        'repo': 'https://github.com/boundlessgeo/exchange',
        'version': exchange_version['version'],
        'commit': exchange_version['commit']
    }, {
        'name': 'GeoNode',
        'website': 'http://geonode.org/',
        'repo': 'https://github.com/GeoNode/geonode',
        'boundless_repo': 'https://github.com/boundlessgeo/geonode',
        'version': geonode_version['version'],
        'commit': geonode_version['commit']
    }, {
        'name': 'GeoServer',
        'website': 'http://geoserver.org/',
        'repo': 'https://github.com/geoserver/geoserver',
        'boundless_repo': 'https://github.com/boundlessgeo/geoserver',
        'version': geoserver_version['version'],
        'commit': geoserver_version['commit']
    }, {
        'name': 'MapLoom',
        'website': 'http://prominentedge.com/projects/maploom.html',
        'repo': 'https://github.com/ROGUE-JCTD/MapLoom',
        'boundless_repo': ('https://github.com/boundlessgeo/'
                           'django-exchange-maploom'),
        'version': maploom_version['version'],
        'commit': maploom_version['commit']
    }, {
        'name': 'OSGeo Importer',
        'repo': 'https://github.com/GeoNode/django-osgeo-importer',
        'version': importer_version['version'],
        'commit': importer_version['commit']
    }, {
        'name': 'React Viewer',
        'website': 'http://client.geonode.org',
        'repo': 'https://github.com/GeoNode/geonode-client',
        'version': react_version['version'],
        'commit': react_version['commit']
    }]

    return render_to_response(template, RequestContext(request, {
        'projects': projects,
        'exchange_version': exchange_version['version']
    }))


def logout(request):
    redirect_to = reverse('account_logout')
    if hasattr(settings, 'ENABLE_AUTH0_LOGIN') and settings.ENABLE_AUTH0_LOGIN:
        from exchange.auth.backends.auth0 import AuthZeroOAuth2
        redirect_to = AuthZeroOAuth2.LOGOUT_URL
    return HttpResponseRedirect(redirect_to)


def capabilities(request):
    """
    The capabilities view is like the about page, but for consumption
    by code instead of humans. It serves to provide information about
    the Exchange instance.
    """
    capabilities = {}

    capabilities["versions"] = {
        'exchange': get_exchange_version(),
        'geonode': get_geonode_version(),
        'geoserver': get_geoserver_version(),
    }

    if 'geonode_anywhere' in settings.INSTALLED_APPS:
        from geonode_anywhere.views import get_capabilities
        capabilities.update(get_capabilities())

    current_site = get_current_site(request)
    capabilities["site_name"] = current_site.name

    return JsonResponse({'capabilities': capabilities})


def layer_detail(request, layername, template='layers/layer_detail.html'):
    layer = _resolve_layer(
        request,
        layername,
        'base.view_resourcebase',
        _("You are not permitted to view this layer"))

    # assert False, str(layer_bbox)
    config = layer.attribute_config()

    # Add required parameters for GXP lazy-loading
    layer_bbox = layer.bbox
    bbox = [float(coord) for coord in list(layer_bbox[0:4])]
    config["srs"] = getattr(settings, 'DEFAULT_MAP_CRS', 'EPSG:900913')
    config["bbox"] = bbox if config["srs"] != 'EPSG:900913' \
        else llbbox_to_mercator([float(coord) for coord in bbox])
    config["title"] = layer.title
    config["queryable"] = True
    if layer.default_style:
        config["styles"] = layer.default_style.name

    if layer.storeType == "remoteStore":
        source_srid = None
        # Only grab the service proj/bbox if it is valid
        if None not in layer.service.bbox[0:4]:
            bbox = [float(coord) for coord in list(layer.service.bbox[0:4])]
            source_srid = layer.service.srid
        # Otherwise try the service directly
        # This is needed since previous services registered
        # did not store the bbox/srid in the model
        else:
            try:
                service_handler = get_service_handler(
                    base_url=layer.service.base_url,
                    service_type=layer.service.type)
                if getattr(service_handler.parsed_service, 'initialExtent',
                           None):
                    bbox[0] = service_handler.parsed_service.initialExtent[
                        'xmin']
                    bbox[1] = service_handler.parsed_service.initialExtent[
                        'ymin']
                    bbox[2] = service_handler.parsed_service.initialExtent[
                        'xmax']
                    bbox[3] = service_handler.parsed_service.initialExtent[
                        'ymax']
                else:
                    logger.info('Could not retrieve extent from service: {0}'
                                .format(layer.service))
                if getattr(service_handler.parsed_service, 'spatialReference',
                           None):
                    source_srid = \
                        service_handler.parsed_service.spatialReference[
                            'latestWkid']
                else:
                    logger.info('Could not retrieve srid from service: {0}'
                                .format(layer.service))
            except Exception as e:
                logger.info('Failed to access service endpoint: {0}'
                            .format(layer.service.base_url))
                logger.info('Caught error: {0}'.format(e))
        if source_srid is None:
            source_srid = layer.srid
        target_srid = 3857 if config["srs"] == 'EPSG:900913' else config["srs"]
        reprojected_bbox = bbox_to_projection(bbox, source_srid=source_srid,
                                              target_srid=target_srid)
        bbox = reprojected_bbox[:4]
        config['bbox'] = [float(coord) for coord in bbox]
        service = layer.service
        source_url = service.base_url
        use_proxy = (callable(uses_proxy_route) and
                     uses_proxy_route(service.base_url))
        components = urlsplit(service.base_url)
        query_params = None
        if components.query:
            query_params = OrderedDict(
                parse_qsl(components.query, keep_blank_values=True))
            removed_query = [components.scheme, components.netloc,
                             components.path,
                             None, components.fragment]
            source_url = urlunsplit(removed_query)
        source_params = {
            "ptype": service.ptype,
            "remote": True,
            "url": source_url,
            "name": service.name,
            "use_proxy": use_proxy}
        if query_params is not None:
            source_params["params"] = query_params
        if layer.alternate is not None:
            config["layerid"] = layer.alternate
        maplayer = GXPLayer(
            name=layer.typename,
            ows_url=layer.ows_url,
            layer_params=json.dumps(config),
            source_params=json.dumps(source_params))
    else:
        maplayer = GXPLayer(
            name=layer.typename,
            ows_url=layer.ows_url,
            layer_params=json.dumps(config))

    # Update count for popularity ranking,
    # but do not includes admins or resource owners
    if request.user != layer.owner and not request.user.is_superuser:
        Layer.objects.filter(
            id=layer.id).update(popular_count=F('popular_count') + 1)

    # center/zoom don't matter; the viewer will center on the layer bounds
    map_obj = GXPMap(
        projection=getattr(settings, 'DEFAULT_MAP_CRS', 'EPSG:900913'))

    metadata = layer.link_set.metadata().filter(
        name__in=settings.DOWNLOAD_FORMATS_METADATA)

    granules = None
    all_granules = None
    filter = None
    if layer.is_mosaic:
        try:
            cat = gs_catalog
            cat._cache.clear()
            store = cat.get_store(layer.name)
            coverages = cat.mosaic_coverages(store)

            filter = None
            try:
                if request.GET["filter"]:
                    filter = request.GET["filter"]
            except:
                pass

            offset = 10 * (request.page - 1)
            granules = cat.mosaic_granules(
                coverages['coverages']['coverage'][0]['name'], store, limit=10,
                offset=offset, filter=filter)
            all_granules = cat.mosaic_granules(
                coverages['coverages']['coverage'][0]['name'], store,
                filter=filter)
        except:
            granules = {"features": []}
            all_granules = {"features": []}

    context_dict = {
        "resource": layer,
        'perms_list': get_perms(request.user, layer.get_self_resource()),
        "permissions_json": _perms_info_json(layer),
        "documents": get_related_documents(layer),
        "metadata": metadata,
        "is_layer": True,
        "wps_enabled": settings.OGC_SERVER['default']['WPS_ENABLED'],
        "granules": granules,
        "all_granules": all_granules,
        "filter": filter,
    }

    if 'access_token' in request.session:
        access_token = request.session['access_token']
    else:
        u = uuid.uuid1()
        access_token = u.hex

    if bbox is not None:
        minx, miny, maxx, maxy = [float(coord) for coord in bbox]
        x = (minx + maxx) / 2
        y = (miny + maxy) / 2

        if layer.is_remote or getattr(settings, 'DEFAULT_MAP_CRS',
                                      'EPSG:900913') == "EPSG:4326":
            center = list((x, y))
        else:
            center = list(forward_mercator((x, y)))

        if center[1] == float('-inf'):
            center[1] = 0

        BBOX_DIFFERENCE_THRESHOLD = 1e-5

        # Check if the bbox is invalid
        valid_x = (maxx - minx) ** 2 > BBOX_DIFFERENCE_THRESHOLD
        valid_y = (maxy - miny) ** 2 > BBOX_DIFFERENCE_THRESHOLD

        if valid_x:
            width_zoom = math.log(360 / abs(maxx - minx), 2)
        else:
            width_zoom = 15

        if valid_y:
            height_zoom = math.log(360 / abs(maxy - miny), 2)
        else:
            height_zoom = 15

        map_obj.center_x = center[0]
        map_obj.center_y = center[1]
        map_obj.zoom = math.ceil(min(width_zoom, height_zoom))

    context_dict["viewer"] = json.dumps(
        map_obj.viewer_json(request.user, access_token,
                            *(default_map_config(request)[1] + [maplayer])))

    context_dict["preview"] = getattr(
        settings,
        'LAYER_PREVIEW_LIBRARY',
        'leaflet')
    context_dict["crs"] = getattr(
        settings,
        'DEFAULT_MAP_CRS',
        'EPSG:900913')

    if layer.storeType == 'dataStore':
        links = layer.link_set.download().filter(
            name__in=settings.DOWNLOAD_FORMATS_VECTOR)
    else:
        links = layer.link_set.download().filter(
            name__in=settings.DOWNLOAD_FORMATS_RASTER)
    links_view = [item for idx, item in enumerate(links) if
                  item.url and 'wms' in item.url or 'gwc' in item.url]
    links_download = [item for idx, item in enumerate(links) if
                      item.url and 'wms' not in item.url and
                      'gwc' not in item.url]
    for item in links_view:
        if item.url and access_token:
            item.url = "%s&access_token=%s&time=%s" % \
                       (item.url, access_token, "0/9999")
    for item in links_download:
        if item.url and access_token:
            item.url = "%s&access_token=%s" % (item.url, access_token)

    if request.user.has_perm('view_resourcebase', layer.get_self_resource()):
        context_dict["links"] = links_view
    if request.user.has_perm('download_resourcebase',
                             layer.get_self_resource()):
        if layer.storeType == 'dataStore':
            links = layer.link_set.download().filter(
                name__in=settings.DOWNLOAD_FORMATS_VECTOR)
        else:
            links = layer.link_set.download().filter(
                name__in=settings.DOWNLOAD_FORMATS_RASTER)
        context_dict["links_download"] = links_download

    if settings.SOCIAL_ORIGINS:
        context_dict["social_links"] = build_social_links(request, layer)

    return render_to_response(template, RequestContext(request, context_dict))


def layer_metadata_detail(request, layername,
                          template='layers/metadata_detail.html'):

    layer = _resolve_layer(request, layername, 'view_resourcebase',
                           _PERMISSION_MSG_METADATA)

    return render_to_response(template, RequestContext(request, {
        "layer": layer,
        'SITEURL': settings.SITEURL[:-1]
    }))


def layer_publish(request, layername):
    layer = _resolve_layer(request, layername, 'view_resourcebase',
                           _PERMISSION_MSG_METADATA)
    layer.is_published = True
    layer.save()

    return HttpResponseRedirect(reverse(
                                'layer_detail',
                                args=([layer.service_typename])
                                ))


def map_metadata_detail(request, mapid,
                        template='maps/metadata_detail.html'):

    map_obj = _resolve_map(request, mapid, 'view_resourcebase')
    return render_to_response(template, RequestContext(request, {
        "layer": map_obj,
        "mapid": mapid,
        'SITEURL': settings.SITEURL[:-1],
    }))


def new_map_config(request):
    '''
    View that creates a new map.

    If the query argument 'copy' is given, the initial map is
    a copy of the map with the id specified, otherwise the
    default map configuration is used.  If copy is specified
    and the map specified does not exist a 404 is returned.
    '''
    DEFAULT_MAP_CONFIG, DEFAULT_BASE_LAYERS = default_map_config(request)

    if 'access_token' in request.session:
        access_token = request.session['access_token']
    else:
        access_token = None

    if request.method == 'GET' and 'copy' in request.GET:
        mapid = request.GET['copy']
        map_obj = _resolve_map(request, mapid, 'base.view_resourcebase')

        map_obj.abstract = DEFAULT_ABSTRACT
        map_obj.title = DEFAULT_TITLE
        map_obj.refresh_interval = 60000
        if request.user.is_authenticated():
            map_obj.owner = request.user

        config = map_obj.viewer_json(request.user, access_token)
        del config['id']
    else:
        if request.method == 'GET':
            params = request.GET
        elif request.method == 'POST':
            params = request.POST
        else:
            return HttpResponse(status=405)

        if 'layer' in params:
            bbox = None
            map_obj = Map(projection=getattr(settings, 'DEFAULT_MAP_CRS',
                                             'EPSG:900913'))
            layers = []
            for layer_name in params.getlist('layer'):
                try:
                    layer = _resolve_layer(request, layer_name)
                except ObjectDoesNotExist:
                    # bad layer, skip
                    continue
                except Http404:
                    # can't find the layer, skip it.
                    continue

                if not request.user.has_perm(
                        'view_resourcebase',
                        obj=layer.get_self_resource()):
                    # invisible layer, skip inclusion
                    continue

                layer_bbox = layer.bbox
                # assert False, str(layer_bbox)
                if bbox is None:
                    bbox = list(layer_bbox[0:4])
                else:
                    bbox = list(bbox)
                    bbox[0] = min(bbox[0], layer_bbox[0])
                    bbox[1] = max(bbox[1], layer_bbox[1])
                    bbox[2] = min(bbox[2], layer_bbox[2])
                    bbox[3] = max(bbox[3], layer_bbox[3])

                config = layer.attribute_config()

                # Add required parameters for GXP lazy-loading
                config["title"] = layer.title
                config["queryable"] = True

                config["srs"] = getattr(settings, 'DEFAULT_MAP_CRS',
                                        'EPSG:900913')
                config["bbox"] = bbox if config["srs"] != 'EPSG:900913' \
                    else llbbox_to_mercator([float(coord) for coord in bbox])

                if layer.storeType == "remoteStore":
                    service = layer.service
                    # Probably not a good idea to send the access token
                    # to every remote service. This should never match,
                    # so no access token should be sent to remote services.
                    ogc_server_url = urlsplit(
                        ogc_server_settings.PUBLIC_LOCATION).netloc
                    service_url = urlsplit(service.base_url).netloc

                    if config["srs"] == 'EPSG:900913':
                        target_srid = 3857
                    else:
                        target_srid = config["srs"]
                    reprojected_bbox = bbox_to_projection(
                        bbox,
                        source_srid=layer.srid,
                        target_srid=target_srid
                    )
                    bbox = reprojected_bbox[:4]
                    config['bbox'] = [float(coord) for coord in bbox]

                    if access_token and ogc_server_url == service_url and \
                            'access_token' not in service.base_url:
                        url = service.base_url + '?access_token={}'.format(
                            access_token)
                    else:
                        url = service.base_url
                    use_proxy = (callable(uses_proxy_route) and
                                 uses_proxy_route(service.base_url))
                    if layer.alternate is not None:
                        config["layerid"] = layer.alternate
                    maplayer = MapLayer(
                        map=map_obj,
                        name=layer.typename,
                        ows_url=layer.ows_url,
                        layer_params=json.dumps(config, cls=DjangoJSONEncoder),
                        visibility=True,
                        source_params=json.dumps({
                            "ptype": service.ptype,
                            "remote": True,
                            "url": url,
                            "name": service.name,
                            "use_proxy": use_proxy})
                    )
                else:
                    ogc_server_url = urlsplit(
                        ogc_server_settings.PUBLIC_LOCATION).netloc
                    layer_url = urlsplit(layer.ows_url).netloc

                    if access_token and ogc_server_url == layer_url and \
                            'access_token' not in layer.ows_url:
                        url = layer.ows_url + '?access_token=' + access_token
                    else:
                        url = layer.ows_url
                    maplayer = MapLayer(
                        map=map_obj,
                        name=layer.typename,
                        ows_url=url,
                        # use DjangoJSONEncoder to handle Decimal values
                        layer_params=json.dumps(config, cls=DjangoJSONEncoder),
                        visibility=True
                    )

                layers.append(maplayer)

            if bbox is not None:
                minx, miny, maxx, maxy = [float(coord) for coord in bbox]
                x = (minx + maxx) / 2
                y = (miny + maxy) / 2

                if layer.is_remote or getattr(settings, 'DEFAULT_MAP_CRS',
                                              'EPSG:900913') == "EPSG:4326":
                    center = list((x, y))
                else:
                    center = list(forward_mercator((x, y)))

                if center[1] == float('-inf'):
                    center[1] = 0

                BBOX_DIFFERENCE_THRESHOLD = 1e-5

                # Check if the bbox is invalid
                valid_x = (maxx - minx) ** 2 > BBOX_DIFFERENCE_THRESHOLD
                valid_y = (maxy - miny) ** 2 > BBOX_DIFFERENCE_THRESHOLD

                if valid_x:
                    width_zoom = math.log(360 / abs(maxx - minx), 2)
                else:
                    width_zoom = 15

                if valid_y:
                    height_zoom = math.log(360 / abs(maxy - miny), 2)
                else:
                    height_zoom = 15

                map_obj.center_x = center[0]
                map_obj.center_y = center[1]
                map_obj.zoom = math.ceil(min(width_zoom, height_zoom))

            config = map_obj.viewer_json(
                request.user, access_token, *(DEFAULT_BASE_LAYERS + layers))
            config['fromLayer'] = True
        else:
            config = DEFAULT_MAP_CONFIG
    return json.dumps(config)


def new_map(request, template='maps/map_new.html'):
    config = new_map_config(request)
    context_dict = {
        'config': config,
    }
    context_dict["preview"] = getattr(
        settings,
        'LAYER_PREVIEW_LIBRARY',
        '')
    if isinstance(config, HttpResponse):
        return config
    else:
        return render_to_response(template, RequestContext(request,
                                                           context_dict))


def new_map_json(request):

    if request.method == 'GET':
        config = new_map_config(request)
        if isinstance(config, HttpResponse):
            return config
        else:
            return HttpResponse(config)

    elif request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponse(
                'You must be logged in to save new maps',
                content_type="text/plain",
                status=401
            )

        map_obj = Map(owner=request.user, zoom=0,
                      center_x=0, center_y=0)
        map_obj.save()
        map_obj.set_default_permissions()

        # If the body has been read already, use an empty string.
        # See https://github.com/django/django/commit/58d555caf527d6f1bdfeab14527484e4cca68648 # noqa
        # for a better exception to catch when we move to Django 1.7.
        try:
            body = request.body
        except Exception:
            body = ''

        try:
            map_obj.update_from_viewer(body)
            MapSnapshot.objects.create(
                config=clean_config(body),
                map=map_obj,
                user=request.user)
        except ValueError as e:
            return HttpResponse(str(e), status=400)
        else:
            return HttpResponse(
                json.dumps({'id': map_obj.id}),
                status=200,
                content_type='application/json'
            )
    else:
        return HttpResponse(status=405)


def proxy(request):
    PROXY_ALLOWED_HOSTS = getattr(settings, 'PROXY_ALLOWED_HOSTS', ())

    host = None

    if ogc_server_settings is not None:
        if ogc_server_settings:
            hostname = (ogc_server_settings.hostname,)
        else:
            hostname = ()
        PROXY_ALLOWED_HOSTS += hostname
        host = ogc_server_settings.netloc

    if 'url' not in request.GET:
        return HttpResponse("The proxy service requires a "
                            "URL-encoded URL as a parameter.",
                            status=400,
                            content_type="text/plain"
                            )

    raw_url = request.GET['url']
    url = urlsplit(raw_url)
    headers = {}

    # Fix up any possible non-absolute URLs that have no scheme, or even domain
    if ((callable(protocol_relative_url) and
         protocol_relative_url(raw_url)) or not url.scheme):
        if url.netloc and callable(protocol_relative_to_scheme):
            # Fix up any '//' protocol relative URLs coming from JS map viewers
            # Use request.scheme to reference origin scheme context
            # Note: Can't use request.build_absolute_uri(raw_url) for this
            raw_url = protocol_relative_to_scheme(url.geturl(),
                                                  scheme=request.scheme)
            # logger.debug("protocol_relative_to_scheme = ".format(raw_url))
        else:
            raw_url = request.build_absolute_uri(raw_url)
            # logger.debug("build_absolute_uri = ".format(raw_url))
        url = urlsplit(raw_url)

    if not settings.DEBUG:
        if not (validate_host(url.hostname, PROXY_ALLOWED_HOSTS) or
                (callable(has_ssl_config) and has_ssl_config(url.geturl()))):
            return HttpResponse(
                "DEBUG is set to False but the host of the path provided to "
                "the proxy service is not in the PROXY_ALLOWED_HOSTS setting "
                "or defined to use the proxy in SSL/PKI configurations.",
                status=403,
                content_type="text/plain"
            )

    if url.scheme.lower() == 'https' \
            and callable(has_ssl_config) and has_ssl_config(url.geturl()):
        # Adjust request to mock call to pki_request view
        # Merge queries
        pki_req_query = request.GET.copy()
        """django.http.QueryDict"""
        # Strip the url param from request query
        del pki_req_query['url']
        # Note: leave other query pairs passed to this view, e.g. access_token

        # Add any query from passed url param's URL
        url_query = url.query.strip()
        for k, v in parse_qsl(url_query, keep_blank_values=True):
            pki_req_query.appendlist(k, v)
        request.GET = pki_req_query
        request.META["QUERY_STRING"] = pki_req_query.urlencode()

        # pki_request view is restricted to local calls
        request.META["REMOTE_ADDR"] = '127.0.0.1'
        request.META["REMOTE_HOST"] = 'localhost'
        # TODO: Update HTTP_X_FORWARDED_FOR? See: api.views.get_client_ip()

        base_url = urlunsplit((None, url.netloc, url.path, None, None))\
            .replace('//', '', 1)
        # For pki_request view, resource_url has no URL scheme
        resource_url = quote(base_url)

        pki_path = reverse('pki_request',
                           kwargs={'resource_url': resource_url})
        # Reset view paths attributes
        request.path = request.path_info = pki_path
        request.META["PATH_INFO"] = pki_path
        request.resolver_match = resolve(pki_path)

        logger.debug("pki_req QueryDict: {0}".format(pki_req_query))
        # logger.debug("pki_req META: {0}".format(request.META))
        logger.debug("pki_req META['QUERY_STRING']: {0}"
                     .format(request.META["QUERY_STRING"]))
        logger.debug("Routing through pki proxy: {0}".format(resource_url))
        return pki_request(request, resource_url=resource_url)

    if settings.SESSION_COOKIE_NAME in request.COOKIES and \
            is_safe_url(url=raw_url, host=host):
        headers["Cookie"] = request.META["HTTP_COOKIE"]

    if request.method in ("POST", "PUT") and "CONTENT_TYPE" in request.META:
        headers["Content-Type"] = request.META["CONTENT_TYPE"]

    http_client = requests.session()
    http_client.verify = True
    req_method = getattr(http_client, request.method.lower())
    resp = req_method(raw_url, headers=headers, data=request.body)

    if 'Content-Type' in resp.headers:
        content_type = resp.headers['Content-Type']
    else:
        content_type = 'text/plain'

    # If we get a redirect, let's add a useful message.
    if resp.status_code in (301, 302, 303, 307):
        response = HttpResponse(
            ('This proxy does not support redirects. The server in "%s" '
             'asked for a redirect to "%s"' %
             (raw_url, resp.headers['Location'])),
            status=resp.status_code,
            content_type=content_type
        )

        response['Location'] = resp.headers['Location']
    else:
        response = HttpResponse(
            resp.content,
            status=resp.status_code,
            content_type=content_type
        )

    return response


def geoserver_reverse_proxy(request):
    url = settings.OGC_SERVER['default']['LOCATION'] + 'wfs/WfsDispatcher'
    data = request.body
    headers = {'Content-Type': 'application/xml',
               'Data-Type': 'xml'}

    req = requests.post(url, data=data, headers=headers,
                        cookies=request.COOKIES)
    return HttpResponse(req.content, content_type='application/xml')


# Function returns a generator searching recursively for a key in a dict
def gen_dict_extract(key, var):
    if hasattr(var, 'iteritems'):
        for k, v in var.iteritems():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result


# Checks if key is present in dictionary
def key_exists(key, var):
    return any(True for _ in gen_dict_extract(key, var))


def empty_page(request):
    return HttpResponse('')


def publish_service(request, pk):
    """
    Publish the service records to the csw catalog
    """
    create_record.delay(pk)
    return redirect('services')


def remove_record_from_csw(sender, instance, using, **kwargs):
    """
    Delete all csw records associated with the service. We only
    run on service pre_delete to clean up the csw prior to the django db.
    """
    if instance.type in ["WMS", "OWS"]:
        for record in instance.servicelayer_set.all():
            delete_record(record.uuid)
    else:
        delete_record(instance.uuid)


def service_post_save(sender, **kwargs):
    """
    Assign CSW Manager permissions for all newly created Service instances.
    We only run on service creation to avoid having to check for existence
    on each call to Service.save.
    """
    service, created = kwargs["instance"], kwargs["created"]
    if created:
        group = Group.objects.get(name='csw_manager')
        assign_perm("change_service", group, service)
        assign_perm("delete_service", group, service)
        service.is_published = False
        service.save()


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


class AuthErrorPage(TemplateView):
    template_name = 'account/auth-failed.html'


@login_required
def layer_create(request, template='createlayer/layer_create.html'):
    """
    Create an empty layer.
    """
    error = None
    profile = Profile.objects.get(username=request.user.username)
    if request.method == 'POST' and \
            (profile.has_perm('layers.add_layer') is True or
             profile.is_staff is True or profile.is_superuser is True):
        form = NewLayerForm(request.POST)
        if form.is_valid():
            try:
                name = form.cleaned_data['name']
                name = slugify(name.replace(".", "_"))
                title = form.cleaned_data['title']
                geometry_type = form.cleaned_data['geometry_type']
                attributes = form.cleaned_data['attributes']
                permissions = form.cleaned_data["permissions"]
                layer = create_layer(name, title, request.user.username,
                                     geometry_type, attributes)
                layer.set_permissions(json.loads(permissions))
                return HttpResponseRedirect(
                    '/maps/new?layer=%s' % layer.typename)
            except Exception as e:
                error = '%s (%s)' % (e.message, type(e))
    else:
        form = NewLayerForm()

    ctx = {
        'form': form,
        'is_layer': True,
        'error': error
    }

    return render_to_response(template, RequestContext(request, ctx))
