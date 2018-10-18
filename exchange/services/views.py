from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.utils.translation import ugettext as _

from exchange.services import forms
from exchange.services.models import Service


# To override geonode.services.views.edit_service
@login_required
def edit_service(request, service_id):
    """
    Edit an existing Service
    """
    service = get_object_or_404(Service, pk=service_id)

    classification_dict = getattr(settings, "CLASSIFICATION_LEVELS", {})
    if request.user != service.owner and not request.user.has_perm(
            'change_service', obj=service):
        return HttpResponse(
            loader.render_to_string(
                '401.html', context={
                    'error_message': _(
                        "You are not permitted to change this service."
                    )}, request=request), status=401)
    if request.method == "POST":
        service_form = forms.ServiceForm(
            request.POST, instance=service, prefix="service")
        if service_form.is_valid():
            service = service_form.save(commit=False)
            service.keywords.clear()
            service.keywords.add(*service_form.cleaned_data['keywords'])
            service.save()
            return HttpResponseRedirect(service.get_absolute_url())
    else:
        service_form = forms.ServiceForm(
            instance=service, prefix="service")
    return render(request,
                  "services/service_edit_extension.html",
                  context={"service": service,
                           "service_form": service_form,
                           "classification_levels": classification_dict})
