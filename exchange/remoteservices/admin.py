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

from django.contrib import admin

from geonode.base.admin import ResourceBaseAdminForm

from . import models


class ExchangeServiceAdminForm(ResourceBaseAdminForm):

    class Meta:
        model = models.ExchangeService
        fields = '__all__'


class ExchangeServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'geonode_service')
    list_display_links = ('id', 'geonode_service')
    form = ExchangeServiceAdminForm


admin.site.register(models.ExchangeService, ExchangeServiceAdmin)
