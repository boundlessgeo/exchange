from django.conf import settings
from django.contrib.auth.middleware import RemoteUserMiddleware
from oauthlib.common import generate_token
from oauth2_provider.models import AccessToken, get_application_model
import datetime
from django.utils.cache import patch_vary_headers


class GeoAxisMiddleware(RemoteUserMiddleware):
    """
    Middleware for utilizing GEOAXIS provided authentication. This is a
    subclass of the RemoteUserMiddleware. The header value is configurable
    by setting a django setting of GEOAXIS_HEADER.
    """
    header = getattr(settings, 'GEOAXIS_HEADER', 'OAM_REMOTE_USER')
    force_logout_if_no_header = False


class GeoServerTokenMiddleware(object):
    """
    Middleware for exposing the Geoserver Access Token as a cookie.
    """
    def _get_token(self, request):
        try:
            return request.COOKIES[settings.ACCESS_TOKEN_NAME]
        except KeyError:
            return None

    def _set_token(self, request, response):
        if request.user and request.user.is_authenticated():
            access_token = request.META.get('ACCESS_TOKEN', None)
            if access_token is None:
                Application = get_application_model()
                geoserver_app = Application.objects.get(name="GeoServer")
                token = generate_token()
                ttl = datetime.datetime.now() + datetime.timedelta(days=3)
                AccessToken.objects.get_or_create(user=request.user,
                                                  application=geoserver_app,
                                                  expires=ttl,
                                                  token=token)
                access_token = token
            response.set_cookie(
                settings.ACCESS_TOKEN_NAME,
                access_token,
                max_age=settings.SESSION_COOKIE_AGE,
                domain=settings.SESSION_COOKIE_DOMAIN,
                path=settings.SESSION_COOKIE_PATH,
                secure=settings.SESSION_COOKIE_SECURE or None,
                httponly=settings.SESSION_COOKIE_HTTPONLY or None,)
            patch_vary_headers(response, ('Cookie',))
        else:
            response.delete_cookie(settings.ACCESS_TOKEN_NAME,
                                   domain=settings.SESSION_COOKIE_DOMAIN)

    def process_request(self, request):
        if request.user and request.user.is_authenticated():
            access_token = self._get_token(request)
            if access_token is not None:
                request.META['ACCESS_TOKEN'] = access_token

    def process_response(self, request, response):
        try:
            self._set_token(request, response)
        except:
            pass
        return response
