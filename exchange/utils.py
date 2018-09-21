# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2018 Boundless Spatial
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

from geonode.utils import get_bearer_token


def append_access_token(url, **kwargs):
    """
    :param url: URL
    :type url: str
    :param kwargs: Args for get_bearer_token
    :type kwargs: dict
    :return: Updated URL
    """
    access_token = get_bearer_token(**kwargs)
    # no query params yet
    if url.find('?') is -1:
        url = url + '?access_token=' + access_token
    else:
        # TODO: if it already has an access_token, do we want to overwrite it?
        if url.find('access_token') is -1:
            url = url + '&access_token=' + access_token
    return url
