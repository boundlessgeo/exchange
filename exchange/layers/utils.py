import requests

from geonode import GeoNodeException
from geonode.contrib.createlayer.utils import logger
from geonode.geoserver.helpers import ogc_server_settings
from geonode.layers.models import Layer

# TODO : move this code to geonode


def update_gs_layer_bounds(layername):
    layer = Layer.objects.get(typename=layername)
    gs_user = ogc_server_settings.credentials[0]
    gs_password = ogc_server_settings.credentials[1]

    xml = ("<featureType>"
           "<enabled>true</enabled>"
           "</featureType>")
    url = (('%s/workspaces/%s/datastores/%s/featuretypes/%s.xml' +
            '?recalculate=nativebbox,latlonbbox')
           % (ogc_server_settings.internal_rest,
              layer.workspace, layer.store, layer.name))
    headers = {'Content-Type': 'application/xml'}
    req = requests.put(url, data=xml, headers=headers,
                       auth=(gs_user, gs_password))
    if req.status_code != 200:
        logger.error('Request status code was: %s' % req.status_code)
        logger.error('Response was: %s' % req.text)
        raise GeoNodeException("Layer could not be updated in GeoServer")
