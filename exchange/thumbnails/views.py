#
# There is only one view for the Thumbnail API.
#
# When the view is called with a GET request it returns
# either a missing thumbnail image *or* the image stored in the database.
#


from django.http import HttpResponse

from base64 import b64decode
import imghdr
import os

from .models import Thumbnail, save_thumbnail
from geonode.documents.models import Document
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

# cache the missing thumbnail for missing images.
TEST_DIR = os.path.dirname(__file__)
MISSING_THUMB = open(
    os.path.join(TEST_DIR, 'static/missing_thumb.png'), 'r').read()


def document_thumbnail(objectId):
    try:
        doc = Document.objects.get(id=objectId)
    except Document.DoesNotExist:
        return None
    if doc:
        img = doc._render_thumbnail()
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
            try:
                img = document_thumbnail(objectId)
            # This case should not occur but represents a failure to save
            except Exception as e:
                logger.debug('Thumbnail: Failed to save thumbnail for Document'
                             ' with id: {0}'.format(objectId))
                logger.debug('Thumbnail: {0}'.format(e))
            if img is None:
                error_msg = 'Thumbnail could not be found for document with ' \
                            'id {0}'.format(objectId)
                logger.debug('Thumbnail: ' + error_msg)
                messages.warning(request, error_msg)
                return HttpResponse(MISSING_THUMB, content_type='image/png')

            return HttpResponse(img, content_type='image/png')

        # else return the missing thumbnail.
        error_msg = 'Thumbnail could not be found for {0} with id {1}'.format(
            objectType, objectId)
        logger.debug('Thumbnail: ' + error_msg)
        messages.warning(request, error_msg)
        return HttpResponse(MISSING_THUMB, content_type='image/png')
    elif(request.method == 'POST'):
        # if body is 'refresh' then just create default document thumb
        if request.body == 'refresh':
            try:
                document_thumbnail(objectId)
            # This case should not occur but represents a failure to save
            except Exception as e:
                # TODO: Should we return a fail response here?
                logger.debug('Thumbnail: Failed to save thumbnail for Document'
                             ' with id: {0}'.format(objectId))
                logger.debug('Thumbnail: {0}'.format(e))
            return HttpResponse(status=201)

        body_len = len(request.body)

        # ensure the thumbnail is < 400kb.
        # This is an arbitrary check I've added, it could be
        # adjusted easily.
        max_bytes = 400000
        if(body_len > max_bytes):
            content = 'Thumbnail too large.'
            logger.debug('Thumbnail: Could not set because '
                         '{0}'.format(content))
            return HttpResponse(status=400, content=content)

        image_bytes = request.body
        # check to see if the image has been uploaded as a base64
        #  image.
        if(request.body[0:22] == 'data:image/png;base64,'):
            image_bytes = b64decode(request.body[22:])

        image_type = imghdr.what('', h=image_bytes)
        if(image_type is None):
            content = 'Bad thumbnail format.'
            logger.debug('Thumbnail: Could not set because '
                         '{0}'.format(content))
            return HttpResponse(status=400, content=content)

        # if the thumbnail does not exist, create a new one.
        try:
            save_thumbnail(
                objectType, objectId, 'image/' + image_type,
                image_bytes, False)
            # return a success message.
            return HttpResponse(status=201)
        except Exception as e:
            logger.error('Thumbnail: Failed to save thumbnail for {0} with '
                         'id {1}'.format(objectType, objectId))
            logger.error('Thumbnail: {0}'.format(e))
            return HttpResponse(status=400, content='Thumbnail failed to save')
