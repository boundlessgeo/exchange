from django.db import models
from .widgets import ColorPickerWidget


class ColorField(models.CharField):
    """
    A text field made to accept hexadecimal color value (#FFFFFF)
    with a color picker widget.
    """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 7
        super(ColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorPickerWidget
        return super(ColorField, self).formfield(**kwargs)
