import logging
import time
from celery.task import task

from django.db.models.signals import post_save
from django.conf import settings
from exchange.utils import get_bearer_token
from geonode.layers.models import Layer
from geonode.maps.models import Map
from geonode.geoserver.helpers import ogc_server_settings
from geonode.utils import forward_mercator
from requests import session
from requests.adapters import HTTPAdapter, Retry
from .models import is_automatic
from .models import save_thumbnail
from PIL import Image
import io
from urlparse import urlparse

try:
    if 'ssl_pki' not in settings.INSTALLED_APPS:
        raise ImportError
    from ssl_pki.models import has_ssl_config
    from ssl_pki.ssl_session import https_client
except ImportError:
    has_ssl_config = None
    https_client = None

try:
    xrange
except NameError:
    xrange = range

THUMBNAIL_BACKGROUND_WMS = getattr(
    settings,
    'THUMBNAIL_BACKGROUND_WMS',
    'https://demo.boundlessgeo.com/geoserver/wms?'
)

THUMBNAIL_BACKGROUND_WMS_LAYER = getattr(
    settings,
    'THUMBNAIL_BACKGROUND_WMS_LAYER',
    'ne:NE1_HR_LC_SR_W_DR'
)

logger = logging.getLogger(__name__)

# setup requests client with max retries
http_client = session()
http_client.verify = True
retry = Retry(
    total=4,
    status=4,
    backoff_factor=0.9,
    status_forcelist=[502, 503, 504],
    method_whitelist=set([
        'HEAD',
        'TRACE',
        'GET',
        'PUT',
        'POST',
        'OPTIONS',
        'DELETE'
    ])
)
http_client.mount('http://', HTTPAdapter(max_retries=retry))
http_client.mount('https://', HTTPAdapter(max_retries=retry))


# combines image content
def combine_images(images):
    returnimage = None
    for i in images:
        if i:
            image = Image.open(io.BytesIO(i)).convert('RGBA')
            # make all white pixels transparent
            pixdata = image.load()
            width, height = image.size
            for y in xrange(height):
                for x in xrange(width):
                    if pixdata[x, y] == (255, 255, 255, 255):
                        pixdata[x, y] = (255, 255, 255, 0)
            if not returnimage:
                returnimage = image
            else:
                baseimage = returnimage
                imagetoadd = image
                returnimage = Image.alpha_composite(
                    baseimage,
                    imagetoadd
                )
    if returnimage:
        with io.BytesIO() as output:
            returnimage.save(output, 'PNG')
            return output.getvalue()
    return None


def make_thumb_request(remote, baseurl, params=None):
    # Avoid using urllib.urlencode here because it breaks the url.
    # commas and slashes in values get encoded and then cause trouble
    # with the WMS parser.
    try:
        if params:
            p = "&".join("%s=%s" % item for item in params.items())
        else:
            p = ''

        thumbnail_create_url = baseurl + p
        p = urlparse(thumbnail_create_url)

        logger.info(
            'Thumbnail: Requesting thumbnail for %s. ',
            thumbnail_create_url
        )

        if remote:
            # Check for SSL configs; use https_client
            if thumbnail_create_url.lower().startswith('https') \
                    and has_ssl_config is not None and \
                    has_ssl_config(thumbnail_create_url, via_query=True):
                # has_ssl_config needs to query db, as call may be from task
                # worker, whose hostnameport_pattern_cache may be out of sync
                logger.info('Fetching %s with https_client'
                            % thumbnail_create_url)
                resp = https_client.get(thumbnail_create_url)
            else:
                logger.info('Fetching %s with no auth' % thumbnail_create_url)
                resp = http_client.get(thumbnail_create_url)
        else:
            # Log in to geoserver with token
            token = get_bearer_token()
            thumbnail_create_url = '%s&access_token=%s' % (
                thumbnail_create_url,
                token)
            logger.debug('fetching %s with token' % thumbnail_create_url)
            resp = http_client.get(thumbnail_create_url)

        if 200 <= resp.status_code <= 299:
            if 'ServiceException' not in resp.content:
                return resp.content

        logger.info(
            'Thumbnail: Encountered service exception or unexpected '
            'status code (%d).  Aborting.',
            resp.status_code)
        logger.debug('content: %s', resp.content)
    except Exception as e:
        logger.exception('Error occured making thumbnail')
    return None


# Get a thumbnail image
#
# This is based on the function in GeoNode but gets
# the image bytes instead.
#
# @return PNG bytes.
#
def get_bbox(instance, crs='EPSG:3857'):
    if crs is None:
        crs = 'EPSG:3857'
    minlon = min(float(instance.bbox_x0), float(instance.bbox_x1))
    minlat = min(float(instance.bbox_y0), float(instance.bbox_y1))
    maxlon = max(float(instance.bbox_x0), float(instance.bbox_x1))
    maxlat = max(float(instance.bbox_y0), float(instance.bbox_y1))

    lon_range = maxlon - minlon
    lat_range = maxlat - minlat
    ratio = lon_range / lat_range

    # create a buffer
    minlon = max(-180, minlon - lon_range * .1)
    minlat = max(-90, minlat - lat_range * .1)
    maxlon = min(180, maxlon + lon_range * .1)
    maxlat = min(90, maxlat + lat_range * .1)

    lon_range = maxlon - minlon
    lat_range = maxlat - minlat
    ratio = lon_range / lat_range

    if ratio < 200.0 / 150.0:
        lon_shift = abs(.5 * ((200.0 / 150.0 * lat_range) - lon_range))
        minlon = max(-180, minlon - lon_shift)
        maxlon = min(180, maxlon + lon_shift)
    else:
        adjusted_range = 150.0 / 200.0 * lon_range
        range_delta = adjusted_range - lat_range
        lat_shift = abs(.5 * range_delta)
        minlat = max(-90, minlat - lat_shift)
        maxlat = min(90, maxlat + lat_shift)

    lon_range = maxlon - minlon
    lat_range = maxlat - minlat
    ratio = lon_range / lat_range

    height = int(200 / ratio)
    logger.debug('height: %s', height)

    if crs == 'EPSG:3857':
        # create bbox in 3857
        minx, miny = forward_mercator([minlon, max(-85.0, minlat)])
        maxx, maxy = forward_mercator([maxlon, min(85.0, maxlat)])
        bbox = '%s,%s,%s,%s' % (
            minx,
            miny,
            maxx,
            maxy
        )
        return bbox, height
    elif crs == 'EPSG:4326':
        # deal with weird bbox order for geographic coords in wms 1.3.0
        bbox = '%s,%s,%s,%s' % (
            minlat,
            minlon,
            maxlat,
            maxlon
        )
        return bbox, height
    elif crs == 'CRS:84':
        # crs84 bbox
        bbox = '%s,%s,%s,%s' % (
            minlon,
            minlat,
            maxlon,
            maxlat
        )
        return bbox, height
    logger.debug('***************Could not determine BBOX***********')


def get_wms_thumbnail(instance=None, layers=None, bbox=None,
                      crs=None, format='image/png', height=None):
    if instance is None:
        if bbox is None or height is None:
            return None
        remote = True
        layers = THUMBNAIL_BACKGROUND_WMS_LAYER
        baseurl = THUMBNAIL_BACKGROUND_WMS

    elif (hasattr(instance, 'storeType') and
            instance.storeType == 'remoteStore'):
        remote = True
        baseurl = instance.ows_url + '?'
    else:
        remote = False
        baseurl = ogc_server_settings.LOCATION + \
            "wms/reflect?"

    if layers is None:
        layers = instance.typename.encode('utf-8')

    if bbox is None and instance is not None:
        bbox, height = get_bbox(instance)
    elif instance is not None:
        bbox, height = get_bbox(instance, crs=crs)

    # base parameters for WMS requests
    params = {
        'layers': layers,
        'format': format,
        'width': 200,
        'height': height,
        'transparent': 'true',
        'crs': 'EPSG:3857',
        # 'srs': 'EPSG:3857', # Boundless GWC uses SRS
        'request': 'GetMap',
        'service': 'wms',
        'version': '1.3.0',
        'styles': '',
        'bbox': bbox
    }

    # Get temporal extent if available
    if (hasattr(instance, 'temporal_extent_start') and
            hasattr(instance, 'temporal_extent_end') and
            instance.temporal_extent_start and instance.temporal_extent_end):

        time = '%s/%s' % (
            instance.temporal_extent_start,
            instance.temporal_extent_end
        )
        time = str.replace(time, ' ', 'T')
        time = str.replace(time, '+00:00', 'Z')
        params['TIME'] = time

    logger.debug('Making request for %s, %s', baseurl, params)
    content = make_thumb_request(remote, baseurl, params)

    if content:
        return content

    return None


def get_thumbnails(instance):
    # list of images to stack
    return_images = []
    map = False
    rest = False
    wms = False
    internal = False
    # Get type
    if instance.class_name == 'Map':
        map = True
    elif (hasattr(instance, 'storeType') and
            instance.storeType == 'remoteStore'):
        if instance.service.type == 'REST':
            rest = True
        elif instance.service.type == 'WMS':
            wms = True
    else:
        internal = True

    # Get bbox for instance regardless of type
    bbox, height = get_bbox(instance)

    # Get basemap for background

    bg = get_wms_thumbnail(None, bbox=bbox, height=height)
    if bg:
        return_images.append(bg)

    # ArcGIS Rest contains a convenient thumbnail endpoint
    # return this endpoint otherwise return bg with correct
    # extent
    if rest:
        thumbnail_create_url = "%s/info/thumbnail" % (instance.ows_url)
        content = make_thumb_request(True, thumbnail_create_url)
        if content:
            return content
        else:
            return bg

    # get list of local layers for maps or layer name for local/wms
    if map:
        local_layers = []
        wms_layers = []
        for layer in instance.layers:
            if layer.local:
                local_layers.append(layer.name)
                continue
            # Get actual layer rather than maplayer
            try:
                layer = Layer.objects.get(typename=layer.name)
                if (hasattr(layer, 'storeType') and
                        layer.storeType == 'remoteStore' and
                        layer.service.type == 'WMS'):
                    wms_layers.append(layer)
            except:
                logger.debug('could not find layer %s', layer.name)
        logger.debug('LAYERS: %s      |||    WMS LAYERS: %s',
                     local_layers, wms_layers)

        if(len(local_layers)) > 0:
            # get map full of local layers
            layers = ",".join(local_layers).encode('utf-8')
            content = get_wms_thumbnail(instance, layers=layers, bbox=bbox)
            if content:
                return_images.append(content)
        if(len(wms_layers)) > 0:
            for wms_layer in wms_layers:
                layers = wms_layer.typename.encode('utf-8')
                logger.debug('CYCLING THROUGH WMS LAYERS: %s', layers)
                content = get_wms_thumbnail(wms_layer,
                                            layers=layers, bbox=bbox)
                if content:
                    return_images.append(content)
                else:  # try as jpeg
                    content = get_wms_thumbnail(wms_layer, layers=layers,
                                                bbox=bbox, format='image/jpeg')
                if content:
                    return_images.append(content)
        return combine_images(return_images)

    # Get image for all local layers
    if internal:
        layers = instance.typename.encode('utf-8')
        content = get_wms_thumbnail(instance, bbox=bbox)
        if content:
            return_images.append(content)
        # internal we know should support 3857 image/png
        return combine_images(return_images)

    if wms:
        layers = instance.typename.encode('utf-8')
        logger.debug('Getting WMS thumbnail for %s', layers)
        content = get_wms_thumbnail(instance, layers=layers, bbox=bbox)
        if content:
            return_images.append(content)
            return combine_images(return_images)

        logger.debug('Getting WMS thumbnail for %s as png8', layers)
        content = get_wms_thumbnail(instance, layers=layers,
                                    bbox=bbox, format='image/png8')
        if content:
            return_images.append(content)
            return combine_images(return_images)

        logger.debug('Getting WMS thumbnail for %s as jpeg', layers)
        content = get_wms_thumbnail(instance, layers=layers,
                                    bbox=bbox, format='image/jpeg')
        if content:
            return_images.append(content)
            return combine_images(return_images)

        content = get_wms_thumbnail(
            instance,
            layers=layers,
            bbox=get_bbox(instance, 'EPSG:4326'),
            crs='EPSG:4326'
        )
        if content:
            return_images.append(content)
            return combine_images(return_images)

        content = get_wms_thumbnail(
            instance,
            layers=layers,
            bbox=get_bbox(instance, 'CRS:84'),
            crs='CRS:84'
        )
        if content:
            return_images.append(content)
            return combine_images(return_images)

    return None


@task(
    max_retries=1,
)
def generate_thumbnail_task(instance_id, class_name):
    logger.debug('generating thumbnail for %s %s', instance_id, class_name)
    obj_type = None
    instance = None
    if class_name == 'Layer':
        layerexists = False
        attempts = 0
        while not layerexists and attempts < 5:
            attempts = attempts + 1
            wait = attempts * 5
            try:
                instance = Layer.objects.get(typename=instance_id)
                obj_type = 'layers'
                layerexists = True
            except Layer.DoesNotExist:
                # Instance not saved yet, nothing more we can do
                logger.debug(
                    'Thumbnail: Layer \'%s\' does not yet exist, cannot '
                    'generate thumbnail. Trying again in %s seconds.',
                    instance_id, wait)
                time.sleep(wait)
    elif class_name == 'Map':
        mapexists = False
        attempts = 0
        while not mapexists and attempts < 12:
            attempts = attempts + 1
            wait = attempts * 5
            try:
                instance = Map.objects.get(id=instance_id)
                obj_type = 'maps'
                mapexists = True
            except Map.DoesNotExist:
                # Instance not saved yet, nothing more we can do
                logger.debug(
                    'Thumbnail: Map \'%s\' does not yet exist, cannot '
                    'generate thumbnail. Trying again in %s seconds.',
                    instance_id, wait)
                time.sleep(wait)

    else:
        logger.debug(
            'Thumbnail: Unsupported class: %s. Aborting.', class_name)
        return

    if not instance:
        logger.debug('Could not find instance')
        return

    logger.info(
        'Thumbnail: Generating thumbnail for \'%s\' of type %s.',
        instance_id, class_name)
    if(instance_id is not None and is_automatic(obj_type, instance_id)):
        # have geoserver generate a preview png and return it.
        thumb_png = get_thumbnails(instance)

        if(thumb_png is not None):
            logger.info(
                'Thumbnail: Thumbnail successfully generated for \'%s\'.',
                instance_id)
            if (hasattr(instance, 'storeType') and
                    instance.storeType == 'remoteStore'):
                save_thumbnail(obj_type, instance.service_typename,
                               'image/png', thumb_png, True)
            else:
                save_thumbnail(obj_type, instance_id,
                               'image/png', thumb_png, True)
        else:
            logger.debug(
                'Thumbnail: Unable to get thumbnail image from '
                'GeoServer for \'%s\'.',
                instance_id)


# This is used as a post-save signal that will
# automatically geneirate a new thumbnail if none existed
# before it.
def generate_thumbnail(instance, sender, **kwargs):
    instance_id = None
    if instance.class_name == 'Layer':
        instance_id = instance.typename
    elif instance.class_name == 'Map':
        instance_id = instance.id

    if instance_id is not None:
        if instance.is_published:
            logger.debug(
                'Thumbnail: Issuing generate thumbnail task for \'%s\'.',
                instance_id)
            generate_thumbnail_task.delay(
                instance_id=instance_id, class_name=instance.class_name)
        else:
            logger.debug(
                'Thumbnail: Instance \'%s\' is not published, skipping '
                'generation.',
                instance_id)
    else:
        logger.debug(
            'Thumbnail: Unsupported class: \'%s\'. Unable to generate '
            'thumbnail.',
            instance.class_name)


def register_post_save_functions():
    # Disconnect first in case this function is called twice
    logger.debug('Thumbnail: Registering post_save functions.')
    post_save.disconnect(generate_thumbnail, sender=Layer)
    post_save.connect(generate_thumbnail, sender=Layer, weak=False)
    post_save.disconnect(generate_thumbnail, sender=Map)
    post_save.connect(generate_thumbnail, sender=Map, weak=False)


register_post_save_functions()
