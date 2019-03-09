# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2016 OSGeo, (C) 2018 Boundless Spatial
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

from django.core.management.base import BaseCommand
from optparse import make_option
from geonode.services.models import Service
from exchange.remoteservices.forms import ExchangeCreateServiceForm
from exchange.remoteservices.serviceprocessors.handler \
    import get_service_handler

from geonode.people.utils import get_valid_user
import sys


class Command(BaseCommand):

    help = 'Import a remote map service into GeoNode'
    option_list = BaseCommand.option_list + (

        make_option('-o', '--owner', dest="owner", default=None,
                    help="Name of the user account which "
                         "should own the imported layers"),
        make_option('-r', '--registerlayers', dest="registerlayers",
                    default=False,
                    help="Register all layers found in the service"),
        make_option('-u', '--username', dest="username", default=None,
                    help="Username required to login to this service if any"),
        make_option('-p', '--password', dest="password", default=None,
                    help="Username required to login to this service if any"),
        make_option('-s', '--security', dest="security", default=None,
                    help="Security permissions JSON - who can view/edit"),
        make_option('-l', '--limit', dest="limit", default=3,
                    help="Number of items to Harvest"),
    )

    args = 'url name type method'

    def handle(self, url, name, type, method, console=sys.stdout, **options):
        user = options.get('user')
        owner = get_valid_user(user)
        limit = options.get('limit')

        register_service = True
        # First Check if this service already exists based on the URL
        base_url = url
        try:
            service = Service.objects.get(base_url=base_url)
        except Service.DoesNotExist:
            service = None
        if service is not None:
            print("This is an existing Service")
            register_service = False
            # Then Check that the name is Unique
        try:
            service = Service.objects.get(name=name)
        except Service.DoesNotExist:
            service = None
        if service is not None:
            print("This is an existing service using this name.\n"
                  "Please specify a different name.")
        if register_service:
            if method == 'I':
                form = ExchangeCreateServiceForm(data={
                    'url': base_url, 'type': type
                })
                if form.is_valid():
                    service_handler = form.cleaned_data["service_handler"]
                    service = service_handler.create_geonode_service(
                        owner=owner
                    )
                    service.full_clean()
                    service.save()
                    service.keywords.add(*service_handler.get_keywords())
                    service.set_default_permissions()

                    service_handler = get_service_handler(
                        service.base_url, service.type
                    )
                    available_resources = service_handler.get_resources()
                    print("Service created with id of %d" % service.id)
                    print(" Harvesting...")
                    processed = 0
                    for resource in available_resources:
                        if processed < limit:
                            try:
                                service_handler.harvest_resource(
                                    resource.id, service
                                )
                                processed = processed + 1
                            except:
                                print(" - Failed Harvesting Resource Id: {}"
                                      .format(resource.id))
                        else:
                            break
                else:
                    print(form.errors)
            else:
                print("Indexing is only available.")

        print('Done')
