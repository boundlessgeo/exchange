from django.db import models
from geonode.services import models as services_models


class ExchangeService(services_models.Service):

    classification = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    provenance = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    caveat = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    poc_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    poc_position = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    poc_email = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    poc_phone = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    poc_address = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    def get_upload_session(self):
        raise NotImplementedError()


