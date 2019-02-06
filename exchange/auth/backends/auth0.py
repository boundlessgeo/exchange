"""
Auth0 OAuth2 backend:
"""
import logging
from urlparse import urlparse
from social_core.backends.oauth import BaseOAuth2

from django.conf import settings

logger = logging.getLogger(__name__)


class AuthZeroOAuth2(BaseOAuth2):
    name = 'auth0'
    HOST = getattr(settings, 'SOCIAL_AUTH_AUTH0_HOST', 'auth0.com')
    CLIENT_KEY = getattr(settings, 'SOCIAL_AUTH_AUTH0_KEY', '')
    CLIENT_SECRET = getattr(settings, 'SOCIAL_AUTH_AUTH0_SECRET', '')
    OIDC_CONFORMANT = getattr(
        settings,
        'SOCIAL_AUTH_AUTH0_OIDC_CONFORMANT',
        False
    )
    ENFORCE_ENV_AUTHZ = getattr(
        settings,
        'SOCIAL_AUTH_AUTH0_ENFORCE_ENVIRONMENT_AUTHORIZATION',
        False
    )
    ID_KEY = 'user_id'
    AUTHORIZATION_URL = 'https://{domain}/authorize'.format(domain=HOST)
    ACCESS_TOKEN_URL = 'https://{domain}/oauth/token'.format(domain=HOST)
    LOGOUT_URL = 'https://{domain}/v2/logout' \
        '?returnTo={returnTo}account/logout' \
        '&client_id={client}'.format(returnTo=settings.SITEURL,
                                     domain=HOST, client=CLIENT_KEY)
    USER_INFO_URL = 'https://{domain}/userinfo?access_token={access_token}'
    REDIRECT_STATE = False
    ROLES_NAMESPACE = 'https://bex.boundlessgeo.io/roles'
    ENV_NAMESPACE = 'https://environments.boundlessgeo.io/roles'
    ACCESS_TOKEN_METHOD = 'POST'
    admin_roles = getattr(settings, 'AUTH0_ADMIN_ROLES', [])
    allowed_roles = getattr(settings, 'AUTH0_ALLOWED_ROLES', [])

    EXTRA_DATA = [
        ('refresh_token', 'refresh_token', True),
        ('user_id', 'user_id'),
        ('sub', 'sub'),
        ('name', 'name'),
        ('given_name', 'given_name'),
        ('middle_name', 'middle_name'),
        ('family_name', 'family_name'),
        ('email', 'email'),
        ('nickname', 'nickname'),
        ('picture', 'picture'),
        ('expires_in', 'expires'),
        ('preferred_username', 'preferred_username'),
        ('email_verified', 'email_verified'),
    ]

    def get_user_id(self, details, response):
        """ user_id property is sent as sub """
        if self.OIDC_CONFORMANT:
            return response['sub']
        else:
            if 'user_id' in details:
                return details['user_id']
            if 'user_id' in response:
                return response['user_id']
            if 'sub' in response:
                return response['sub']

    def compliance_check(self, response):
        details = {}
        if self.OIDC_CONFORMANT:
            details['user_roles'] = response.get(self.ROLES_NAMESPACE) or []
        else:
            user_metadata = response.get('user_metadata')
            app_metadata = response.get('app_metadata')
            fullname, first_name, last_name = self.get_user_names(
                user_metadata.get('name'),
                user_metadata.get('firstName'),
                user_metadata.get('lastName'))
            details['organization'] = user_metadata.get('organization')
            details['fullname'] = fullname
            details['first_name'] = first_name
            details['last_name'] = last_name
            details['user_roles'] = app_metadata.get('SiteRole').split(',')

        details['username'] = response.get('nickname')
        details['email'] = response.get('email')

        return details

    def get_user_details(self, response):
        """Return user details from Auth0 account"""
        details = self.compliance_check(response)

        superuser = False
        staff = False
        active = False

        if any(role in self.admin_roles for role in details['user_roles']):
            superuser = True
            staff = True

        if self.allowed_roles:
            if any(role in self.allowed_roles
                   for role in details['user_roles']):
                active = True
        else:
            active = True

        user_info = {
            'is_superuser': superuser,
            'is_staff': staff,
            'is_active': active
        }

        user_info.update(details)

        logger.debug(user_info)
        return user_info

    def user_data(self, access_token, *args, **kwargs):
        """Grab user profile information from Auth0."""
        response = self.get_json(
            self.USER_INFO_URL.format(
                domain=self.HOST, access_token=access_token))
        return response

    def auth_allowed(self, response, details):
        """Return True if the user should be allowed to authenticate, by
        checking SITE_URL against the enviornment whitelist"""
        if self.ENFORCE_ENV_AUTHZ is False:
            return True

        allowed = False
        allowed_environments = response.get(self.ENV_NAMESPACE)

        for environment_url in allowed_environments:
            site_url = urlparse(settings.SITEURL)
            env_url = urlparse(environment_url)
            if env_url.scheme == site_url.scheme:
                if env_url.hostname == site_url.hostname:
                    allowed = True
                    break

        return allowed
