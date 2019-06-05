/*
 * Create a thumbnal based on the center of an OL3 
 * map canvas.
 */

var getThumbnailPathFromUrl = function() {
    // determine the object type and id from the URL 
    var path_info = window.location.pathname.split('/').slice(-2)

    // put it together in a URL
    return '/thumbnails/' + path_info[0] + '/' + path_info[1];
}

// TODO: Update this to use js-cookie library instead of this mess
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var getCsrfToken = function() {
    // return Cookies.get('csrftoken');
    return getCookie('csrftoken');
}

var csrfSafeMethod = function(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var refreshThumbnail = function() {
        var thumb = $('#thumbnail');
        var time_str = (new Date()).getTime();
        thumb.attr('src', thumb.attr('src').split('?')[0] + '?.ck=' + time_str);
}

// TODO: This is designed to work with React viewer
// Needs to be updated to work with MoW
var createMapThumbnail = function() {
    var canvas = document.getElementsByTagName('canvas')[0];

    // first, calculate the center 'thumbnail'
    //   of the image.
    var thumb_w = 240, thumb_h = 180;
    var w = canvas.width, h = canvas.height; 

    // create a temporary canvas for the 
    //  new thumbnail.
    var thumb_canvas = document.createElement('canvas');
    thumb_canvas.width = thumb_w;
    thumb_canvas.height = thumb_h;
    thumb_canvas.getContext('2d').drawImage(canvas, 0, 0, w, h, 0, 0, thumb_w, thumb_h);

    // get the PNG for saving...
    var png_data = thumb_canvas.toDataURL('image/png');

    // and remove the element from the DOM.
    thumb_canvas.remove();

    var url = getThumbnailPathFromUrl();

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCsrfToken());
            }
        }
    });
    $.ajax({
        type: "POST",
        url: url,
        data: png_data,
        success: function(data, status, jqXHR) {
            refreshThumbnail();
            return true;
        }
    });
    return true;
}

var createDocumentThumbnail = function() {
    var url = getThumbnailPathFromUrl();

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCsrfToken());
            }
        }
    });
    $.ajax({
        type: "POST",
        url: url,
        data: 'refresh',
        success: function(data, status, jqXHR) {
            refreshThumbnail();
            return true;
        }
    });
    return true;
}


var uploadThumbnail = function(inputId) {
    var url = getThumbnailPathFromUrl();

    var reader = new FileReader();

    var input = document.getElementById(inputId);

    // when the file reader gets the new file,
    //  send it up to the server.
    //reader.onload = function(e) {
    var upload = function() {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getCsrfToken());
                }
            }
        });
        $.ajax({
            type: "POST",
            url: url,
            data: input.files[0],
            processData: false,
            success: function(data, status, jqXHR) {
                refreshThumbnail();
            }
        });
    }


    // use jquery to normalize the event handling
    $('#'+inputId).on('change', function() {
        //reader.readAsBinaryString(input.files[0]);
        upload();
    });

    // use the click event to open the file upload dialog.
    $('#'+inputId).click();
    return true;
}
