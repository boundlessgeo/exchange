# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2017 Boundless Spatial
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

import ldap
import os
from ast import literal_eval as le
from .settings import str2bool
from django_auth_ldap.config import (ActiveDirectoryGroupType, LDAPSearch,
                                     MemberDNGroupType)

if str2bool(os.environ.get('AUTH_LDAP_DEBUG')):
    import logging

    logger = logging.getLogger('django_auth_ldap')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

AUTH_LDAP_SERVER_URI = os.environ.get('AUTH_LDAP_SERVER_URI', None)
LDAP_SEARCH_DN = os.environ.get('LDAP_SEARCH_DN', None)
LDAP_EMAIL_MAP = os.environ.get('LDAP_EMAIL_MAP', 'mail')
if str2bool(os.environ.get('LDAP_IS_AD', 'False')):
    AUTH_LDAP_USER = '(SAMAccountName=%(user)s)'
    AUTH_LDAP_GROUP_TYPE = ActiveDirectoryGroupType()
else:
    AUTH_LDAP_USER = '(uid=%(user)s)'
    AUTH_LDAP_GROUP_TYPE = MemberDNGroupType('member')

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)
AUTH_LDAP_BIND_DN = os.environ.get('AUTH_LDAP_BIND_DN', '')
AUTH_LDAP_BIND_PASSWORD = os.environ.get('AUTH_LDAP_BIND_PASSWORD', '')
AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': LDAP_EMAIL_MAP,
}
AUTH_LDAP_USER_SEARCH = LDAPSearch(LDAP_SEARCH_DN, ldap.SCOPE_SUBTREE,
                                   AUTH_LDAP_USER)

# ldap django search mappings
GROUP_SEARCH = os.environ.get('LDAP_GROUP_SEARCH', None)
if GROUP_SEARCH and len(GROUP_SEARCH) > 0:
    try:
        GROUP_SEARCH = le(GROUP_SEARCH)
    except SyntaxError:
        GROUP_SEARCH = GROUP_SEARCH
if GROUP_SEARCH:
    AUTH_LDAP_USER_FLAGS_BY_GROUP = {}
    AUTH_LDAP_GROUP_SEARCH = LDAPSearch(GROUP_SEARCH, ldap.SCOPE_SUBTREE,
                                        "(objectClass=group)")

    ACTIVE_SEARCH = os.environ.get('LDAP_ACTIVE_SEARCH', None)
    STAFF_SEARCH = os.environ.get('LDAP_STAFF_SEARCH', None)
    SU_SEARCH = os.environ.get('LDAP_SUPERUSER_SEARCH', None)

    if ACTIVE_SEARCH and len(ACTIVE_SEARCH) > 0:
        try:
            AUTH_LDAP_USER_FLAGS_BY_GROUP['is_active'] = le(ACTIVE_SEARCH)
        except SyntaxError:
            AUTH_LDAP_USER_FLAGS_BY_GROUP['is_active'] = ACTIVE_SEARCH
        if STAFF_SEARCH and len(STAFF_SEARCH) > 0:
            try:
                AUTH_LDAP_USER_FLAGS_BY_GROUP['is_staff'] = le(STAFF_SEARCH)
            except SyntaxError:
                AUTH_LDAP_USER_FLAGS_BY_GROUP['is_staff'] = STAFF_SEARCH
        if SU_SEARCH and len(SU_SEARCH) > 0:
            try:
                AUTH_LDAP_USER_FLAGS_BY_GROUP['is_superuser'] = le(SU_SEARCH)
            except SyntaxError:
                AUTH_LDAP_USER_FLAGS_BY_GROUP['is_superuser'] = SU_SEARCH
