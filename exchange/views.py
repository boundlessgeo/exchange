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
from geonode.maps.views import _resolve_map
from geonode.layers.views import _resolve_layer, _PERMISSION_MSG_METADATA
from geonode.base.models import TopicCategory
from guardian.shortcuts import assign_perm
from pip._vendor import pkg_resources
from exchange.tasks import create_record, delete_record
from django.core.urlresolvers import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from social_django.utils import psa


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
