from django.db import models
from .fields import ColorField
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from resizeimage import resizeimage
from django.conf import settings


static_url = getattr(settings, 'STATIC_URL', '/static/theme/img/')
media_url = getattr(settings, 'MEDIA_URL', '/media/theme/img/')


def convert_image(image, width, height):
    """
    resize the image to the correct size needed by the template.
    """
    name = image.name
    pio = Image.open(image)
    if width is None:
        img = resizeimage.resize_height(pio, height, validate=False)
    else:
        img = resizeimage.resize_cover(pio, [width, height], validate=False)
    new_image_io = BytesIO()
    img.save(new_image_io, format=pio.format)
    image.delete(save=False)
    image.save(
        name,
        content=ContentFile(new_image_io.getvalue()),
        save=False
    )


class Theme(models.Model):
    name = models.CharField(
        max_length=28,
        null=False,
        blank=False
    )
    description = models.CharField(
        max_length=64,
        null=False,
        blank=True
    )

    default_theme = models.BooleanField(default=False, editable=False)
    active_theme = models.BooleanField(default=False)
    title = models.CharField(
        max_length=32,
        default=None,
        verbose_name="Landing Page Title",
        null=True,
        blank=True
    )
    tagline = models.CharField(
        max_length=64,
        default=None,
        verbose_name="Landing Page Tagline",
        null=True,
        blank=True
    )
    running_hex = ColorField(
        default="0F1A2C",
        verbose_name="Header Footer Color",
        null=True,
        blank=True
    )
    running_text_hex = ColorField(
        default="FFFFFF",
        verbose_name="Header Footer Text Color",
        null=True,
        blank=True
    )
    running_link_hex = ColorField(
        default="29748F",
        verbose_name="Header Footer Link Color",
        null=True,
        blank=True
    )
    pb_text = models.CharField(
        max_length=32,
        default="Boundless Spatial",
        verbose_name="Footer Link Text",
        help_text="Text for the Powered by section in the footer",
        null=True,
        blank=True
    )
    pb_link = models.URLField(
        default="http://boundlessgeo.com/",
        verbose_name="Footer Link URL",
        help_text="Link for the Powered by section in the footer",
        null=True,
        blank=True
    )
    docs_text = models.CharField(
        max_length=32,
        default="Documentation",
        verbose_name="Footer Documentation Text",
        help_text="Text for the documentation link",
        null=True,
        blank=True
    )
    docs_link = models.URLField(
        default=None,
        verbose_name="Documentation Link URL",
        help_text="Link for the Documentation",
        null=True,
        blank=True
    )
    background_logo = models.ImageField(
        upload_to='theme/img/',
        default=None,
        verbose_name="Background Image",
        help_text='Note: will resize to width 1440px and height 350px',
        null=True,
        blank=True
    )
    primary_logo = models.ImageField(
        upload_to='theme/img/',
        default=None,
        verbose_name="Primary Logo",
        help_text="Note: will resize to height 96px",
        null=True,
        blank=True
    )
    banner_logo = models.ImageField(
        upload_to='theme/img/',
        default=None,
        verbose_name="Header Logo",
        help_text="Note: will resize to height 35px",
        null=True,
        blank=True
    )
    custom_analytics = models.TextField(
        null=True,
        blank=True
    )

    def __unicode__(self):
        return self.name

    def _get_background_logo_url(self):
        """
        returns the background logo based on if it uses static or media images
        """
        if self.background_logo:
            if self.default_theme:
                return '%s%s' % (static_url, self.background_logo)
            else:
                return '%s%s' % (media_url, self.background_logo)
        else:
            return None
    background_logo_url = property(_get_background_logo_url)

    def _get_primary_logo_url(self):
        "returns the primary logo based on if it uses static or media images"
        if self.primary_logo:
            if self.default_theme:
                return '%s%s' % (static_url, self.primary_logo)
            else:
                return '%s%s' % (media_url, self.primary_logo)
        else:
            return None
    primary_logo_url = property(_get_primary_logo_url)

    def _get_banner_logo_url(self):
        "returns the banner logo based on if it uses static or media images"
        if self.banner_logo:
            if self.default_theme:
                return '%s%s' % (static_url, self.banner_logo)
            else:
                return '%s%s' % (media_url, self.banner_logo)
        else:
            return None
    banner_logo_url = property(_get_banner_logo_url)

    def __init__(self, *args, **kwargs):
        super(Theme, self).__init__(*args, **kwargs)
        self.__orig_background_logo = self.background_logo
        self.__orig_primary_logo = self.primary_logo
        self.__orig_banner_logo = self.banner_logo

    def save(self, *args, **kwargs):
        """
        Identifies if the image file is new and what file size it needs to be.
        Ensures that only one object has active_theme set to True.
        """
        if self.__orig_background_logo != self.background_logo:
            convert_image(self.background_logo, 1440, 350)
        if self.__orig_primary_logo != self.primary_logo:
            convert_image(self.primary_logo, None, 120)
        if self.__orig_banner_logo != self.banner_logo:
            convert_image(self.banner_logo, None, 35)

        if self.active_theme:
            try:
                temp = Theme.objects.get(active_theme=True)
                if self != temp:
                    temp.active_theme = False
                    temp.save()
            except Theme.DoesNotExist:
                pass

        super(Theme, self).save(*args, **kwargs)
