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

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from geonode.services import enumerations
from geonode.services.forms import CreateServiceForm, ServiceForm
from geonode.base.models import TopicCategory, License
from geonode.base.enumerations import UPDATE_FREQUENCIES

from exchange.remoteservices.serviceprocessors.handler \
    import get_service_handler

from exchange.remoteservices.models import ExchangeService

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


def get_classifications():
    classification_dict = getattr(settings, 'CLASSIFICATION_LEVELS', {})
    return [(x, str(x)) for x in list(classification_dict.keys())]


def get_caveats():
    classification_dict = getattr(settings, 'CLASSIFICATION_LEVELS', {})
    caveats = []

    for key in classification_dict.keys():
        caveats.extend([(x, str(x)) for x in classification_dict[key]])

    return set(caveats)


def get_provenances():
    default = [('Commodity', 'Commodity'),
               ('Crowd-sourced data', 'Crowd-sourced data'),
               ('Derived by trusted agents ', 'Derived by trusted agents '),
               ('Open Source', 'Open Source'),
               ('Structured Observations (SOM)',
                'Structured Observations (SOM)'),  # flake8
               ('Unknown', 'Unknown')]

    provenance_choices = [(x, str(x)) for x in getattr(
        settings, 'REGISTRY_PROVENANCE_CHOICES', [])]

    return provenance_choices + default


class ExchangeEditServiceForm(ServiceForm):
    classification = forms.ChoiceField(
        label=_("Classification"),  # choices=get_classifications(),
        widget=forms.Select(attrs={'cols': 60, 'class': 'inputText'}))
    caveat = forms.ChoiceField(
        label=_("Releasability"),  # choices=get_caveats(),
        widget=forms.Select(attrs={'cols': 60, 'class': 'inputText'}))
    provenance = forms.ChoiceField(
        label=_("Provenance"), choices=get_provenances(),
        widget=forms.Select(attrs={'cols': 60, 'class': 'inputText'}))
    category = forms.ModelChoiceField(
        label=_('Category'),
        queryset=TopicCategory.objects.filter(
            is_choice=True).extra(
            order_by=['description']))
    license = forms.ModelChoiceField(
        label=_('License'), queryset=License.objects.filter())

    maintenance_frequency = forms.ChoiceField(
        label=_("Maintenance Frequency"), choices=UPDATE_FREQUENCIES,
        widget=forms.Select(attrs={'cols': 60, 'class': 'inputText'}))
    fees = forms.CharField(label=_('Fees'), max_length=1000,
                           widget=forms.TextInput(
                               attrs={
                                   'size': '60',
                                   'class': 'inputText'
                               }))
    poc_name = forms.CharField(
        label=_('Point of Contact'),
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'size': '60',
                'class': 'inputText'
            }
        )
    )
    poc_position = forms.CharField(
        label=_('PoC Position'),
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'size': '60',
                'class': 'inputText'
            }
        )
    )
    poc_email = forms.CharField(
        label=_('PoC Email'),
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'size': '60',
                'class': 'inputText'
            }
        )
    )
    poc_phone = forms.CharField(
        label=_('PoC Phone'),
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'size': '60',
                'class': 'inputText'
            }
        )
    )
    poc_address = forms.CharField(
        label=_('PoC Location/Address'),
        max_length=255,
        widget=forms.Textarea(
            attrs={
                'cols': 60
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        if not getattr(settings, 'CLASSIFICATION_BANNER_ENABLED', False):
            self.fields.pop('classification')
            self.fields.pop('caveat')

    class Meta(ServiceForm.Meta):
        model = ExchangeService
        labels = {'description': _('Short Name')}
        fields = (
            'classification',
            'caveat',
            'title',
            'category',
            'description',
            'abstract',
            'keywords',
            'license',
            'maintenance_frequency',
            'provenance',
            'fees',
            'poc_name',
            'poc_position',
            'poc_email',
            'poc_phone',
            'poc_address',
        )


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

            except Exception:
                raise ValidationError(
                    _("Could not connect to the service at %(url)s"),
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
