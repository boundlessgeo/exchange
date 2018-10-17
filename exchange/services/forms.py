from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from geonode.base.enumerations import UPDATE_FREQUENCIES
from geonode.base.models import TopicCategory, License
from geonode.services import forms as services_forms

from .models import Service


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
               ('Structured Observations (SOM)', 'Structured Observations (SOM)'),  # flake8
               ('Unknown', 'Unknown')]

    provenance_choices = [(x, str(x)) for x in getattr(settings, 'REGISTRY_PROVENANCE_CHOICES', [])]

    return provenance_choices + default


class ServiceForm(services_forms.ServiceForm):
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

    class Meta(services_forms.ServiceForm.Meta):
        model = Service
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
