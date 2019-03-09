# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2017 OSGeo, (C) 2018 Boundless Spatial
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

from geonode.services.forms import CreateServiceForm, ServiceForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.conf import settings
from django import forms
from geonode.services import enumerations
from geonode.base.models import License
from exchange.remoteservices.models import ExchangeService
from exchange.remoteservices.serviceprocessors.handler \
    import get_service_handler
from urllib2 import HTTPError as urllibHTTPError
from requests.exceptions import HTTPError, ConnectionError
try:
    if 'ssl_pki' not in settings.INSTALLED_APPS:
        raise ImportError
    from ssl_pki.models import (
        has_ssl_config,
        ssl_config_for_url
    )
except ImportError:
    has_ssl_config = None
    ssl_config_for_url = None


class ExchangeCreateServiceForm(CreateServiceForm):
    @staticmethod
    def validate_pki_url(url):
        """Validates the pki protected url and its associated certificates"""
        ssl_config = ssl_config_for_url(url)
        try:
            if ssl_config is None:
                # Should have an SslConfig, but this could happen
                raise ValidationError
            ssl_config.clean()
        except ValidationError:
            raise ValidationError(
                _("Error with SSL or PKI configuration for url: %(url)s. "
                  "Please contact your Exchange Administrator."),
                params={
                    "url": url,
                }
            )

    def clean(self):
        """Validates form fields that depend on each other"""
        url = self.cleaned_data.get("url")
        service_type = self.cleaned_data.get("type")
        if url is not None and service_type is not None:
            # Check pki validation
            if callable(has_ssl_config) and has_ssl_config(url):
                self.validate_pki_url(url)

        if url is not None and service_type is not None:
            try:
                service_handler = get_service_handler(
                    base_url=url, service_type=service_type)
            # WMS raises requests.exceptions.HTTPError
            except HTTPError as e:
                status_code = e.response.status_code
                if status_code == 500 or status_code == 403:
                    raise ValidationError(
                        _("HTTP {0} error. This could be due to authorization "
                          "failure. Please contact your Exchange Administrator"
                          " to confirm SSL or PKI configuration is correct."
                          .format(status_code)))
                elif status_code == 404:
                    raise ValidationError(
                        _("HTTP {0} error. The host of this service may be "
                          "down or inaccessible.".format(status_code)))
                else:
                    raise ValidationError(
                        _("Unknown error connecting to {0}: HTTP {1} error."
                          .format(url, status_code)))
            # ArcREST raises urllib2.HTTPError
            except urllibHTTPError as e:
                if e.code == 500 or e.code == 403:
                    raise ValidationError(
                        _("HTTP {0} error. This could be due to authorization "
                          "failure. Please contact your Exchange Administrator"
                          " to confirm SSL or PKI configuration is correct."
                          .format(e.code)))
                elif e.code == 404:
                    raise ValidationError(
                        _("HTTP {0} error. The host of this service may be "
                          "down or inaccessible.".format(e.code)))
                else:
                    raise ValidationError(
                        _("Unknown error connecting to {0}: HTTP {1} error."
                          .format(url, e.code)))
            except ConnectionError:
                raise ValidationError(
                    _("Connection timed out attempting to access {0} - "
                      "host may be down or inaccessible".format(url)))
            except KeyError:
                raise ValidationError(
                    _("Could not find a matching service at {0} - "
                      "host exists, but service name does not. Please ensure "
                      "the service name is typed correctly and present on "
                      "this host.".format(url)))
            except Exception:
                raise ValidationError(
                    _("Could not connect to the service at %(url)s "
                      "for an unknown reason"),
                    params={"url": url}
                )
            if not service_handler.has_resources():
                raise ValidationError(
                    _("Could not find importable resources for the service "
                      "at %(url)s"),
                    params={"url": url}
                )
            elif service_type not in (enumerations.AUTO, enumerations.OWS):
                if service_handler.service_type != service_type:
                    raise ValidationError(
                        _("Found service of type %(found_type)s instead "
                          "of %(service_type)s"),
                        params={
                            "found_type": service_handler.service_type,
                            "service_type": service_type
                        }
                    )
            self.cleaned_data["service_handler"] = service_handler
            self.cleaned_data["type"] = service_handler.service_type


# TODO: What is a better name for this?
# Needs to be differentiated from form which applies to ExchangeService model
class ServiceFormOverride(ServiceForm):
    license = forms.ModelChoiceField(
        label=_('License'),
        queryset=License.objects.filter(),
        required=False)
    abstract = forms.CharField(
        label=_("Abstract"),
        widget=forms.Textarea(
            attrs={
                'cols': 60
            }
        ),
        required=False
    )
    fees = forms.CharField(label=_('Fees'), max_length=1000,
                           widget=forms.TextInput(
                               attrs={
                                   'size': '60',
                                   'class': 'inputText'
                               }), required=False)


class ExchangeServiceForm(forms.ModelForm):
    poc_name = forms.CharField(
        label=_('Point of Contact'),
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'size': '60',
                'class': 'inputText'
            }
        ),
        required=False
    )
    poc_position = forms.CharField(
        label=_('PoC Position'),
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'size': '60',
                'class': 'inputText'
            }
        ),
        required=False
    )
    poc_email = forms.CharField(
        label=_('PoC Email'),
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'size': '60',
                'class': 'inputText'
            }
        ),
        required=False
    )
    poc_phone = forms.CharField(
        label=_('PoC Phone'),
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'size': '60',
                'class': 'inputText'
            }
        ),
        required=False
    )
    poc_address = forms.CharField(
        label=_('PoC Location/Address'),
        max_length=255,
        widget=forms.Textarea(
            attrs={
                'cols': 60
            }
        ),
        required=False
    )

    class Meta:
        model = ExchangeService
        labels = {'description': _('Short Name')}
        fields = (
            'poc_name',
            'poc_position',
            'poc_email',
            'poc_phone',
            'poc_address',
        )
