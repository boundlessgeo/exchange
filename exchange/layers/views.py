import json

from django.http.response import HttpResponse
from geonode.layers.views import _resolve_layer, _PERMISSION_MSG_VIEW
from .utils import update_gs_layer_bounds


# TODO: move this view to geonode
def layer_update_bounds(request, layername):
    layer = _resolve_layer(
        request,
        layername,
        'base.view_resourcebase',
        _PERMISSION_MSG_VIEW)
    update_gs_layer_bounds(layername)
    layer.save()
    return HttpResponse(
        json.dumps({'data': '{} bbox has been updated.'.format(layername)}),
        content_type='application/json',
        status=200)
