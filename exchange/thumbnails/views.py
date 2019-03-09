#
# There is only one view for the Thumbnail API.
#
# When the view is called with a GET request it returns
# either a missing thumbnail image *or* the image stored in the database.
#


import imghdr
from base64 import b64decode

import os
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from geonode.documents.models import Document

from .models import Thumbnail, save_thumbnail

# cache the missing thumbnail for missing images.
TEST_DIR = os.path.dirname(__file__)
MISSING_THUMB = open(
    os.path.join(TEST_DIR, 'static/missing_thumb.png'), 'r').read()

IMGTYPES = ['jpg', 'jpeg', 'tif', 'tiff', 'png', 'gif']


def render_document_thumbnail(doc):
    from cStringIO import StringIO

    size = 200, 150

    try:
        from PIL import Image, ImageOps
    except ImportError:
        # logger.error(
        #     '%s: Pillow not installed, cannot generate thumbnails.' %
        #     e)
        return None

    try:
        # if wand is installed, than use it for pdf thumbnailing
        from wand import image
    except:
        wand_available = False
    else:
        wand_available = True

    if wand_available and doc.extension and doc.extension.lower(
    ) == 'pdf' and doc.doc_file:
        # logger.debug(
        #     u'Generating a thumbnail for document: {0}'.format(
        #         self.title))
        try:
            with image.Image(filename=doc.doc_file.path) as img:
                img.sample(*size)
                return img.make_blob('png')
        except:
            pass
    # if we are still here, we use a default image thumb
    if doc.extension and doc.extension.lower() in IMGTYPES and doc.doc_file:
        img = Image.open(doc.doc_file.path)
        img = ImageOps.fit(img, size, Image.ANTIALIAS)
    else:
        filename = finders.find('documents/{0}-placeholder.png'.format(
            doc.extension.lower()), False) or \
            finders.find('documents/generic-placeholder.png', False)

        if not filename:
            return None

        img = Image.open(filename)

    imgfile = StringIO()
    img.save(imgfile, format='PNG')
    return imgfile.getvalue()


def document_thumbnail(objectId):
    try:
        doc = Document.objects.get(id=objectId)
    except Document.DoesNotExist:
        pass
    if doc:
        img = render_document_thumbnail(doc)
        # save so not needed to generate next time
        save_thumbnail(
            'documents', objectId, 'image/png', img, True)
        return img


def thumbnail_view(request, objectType, objectId):
    global MISSING_THUMB, ID_PATTERN

    thumb = None
    try:
        thumb = Thumbnail.objects.get(object_type=objectType,
                                      object_id=objectId)
    except Thumbnail.DoesNotExist:
        # move along, the code tests for None later.
        pass

    if(request.method == 'GET'):
        # if the thumb is not None, return it.
        if(thumb is not None):
            return HttpResponse(thumb.thumbnail_img,
                                content_type=thumb.thumbnail_mime)

        # if the thumbnail is for a document
        # create default thumbnail
        if(objectType == 'documents'):
            img = document_thumbnail(objectId)
            return HttpResponse(img, content_type='image/png')

        # else return the missing thumbnail.
        return HttpResponse(MISSING_THUMB, content_type='image/png')
    elif(request.method == 'POST'):
        # if body is 'refresh' then just create default document thumb
        if request.body == 'refresh':
            document_thumbnail(objectId),
            return HttpResponse(status=201)

        body_len = len(request.body)

        # ensure the thumbnail is < 400kb.
        # This is an arbitrary check I've added, it could be
        # adjusted easily.
        max_bytes = 400000
        if(body_len > max_bytes):
            return HttpResponse(status=400, content='Thumbnail too large.')

        image_bytes = request.body
        # check to see if the image has been uploaded as a base64
        #  image.
        if(request.body[0:22] == 'data:image/png;base64,'):
            image_bytes = b64decode(request.body[22:])

        image_type = imghdr.what('', h=image_bytes)
        if(image_type is None):
            return HttpResponse(status=400, content='Bad thumbnail format.')

        # if the thumbnail does not exist, create a new one.
        save_thumbnail(
            objectType, objectId, 'image/' + image_type, image_bytes, False)

        # return a success message.
        return HttpResponse(status=201)
