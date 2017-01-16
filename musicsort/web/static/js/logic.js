// Get the template HTML and remove it from the doument
window.onload = function() {
    document.querySelector("#total-progress").style.visibility = "hidden";
};
var previewNode = document.querySelector("#template");
previewNode.id = "";
var previewTemplate = previewNode.parentNode.innerHTML;
previewNode.parentNode.removeChild(previewNode);

//////////////////////////////////////////////////////////////////////////////////////
// THIS CODE HAS BEEN TAKEN FROM DJANGO DOCUMENTS
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
//////////////////////////////////////////////////////////////////////////////////////

ready = 0;
uploaded = 0;
ERROR_UPLOAD = 0;
var parts, activeBar = 1, total = 0, flag = 1;

$("#songs-ready").text(ready);
$("#songs-uploaded").text(uploaded);
$(".info-download").css("visibility", "hidden");

resetValues = function() {
    ready = 0;
    uploaded = 0;
    $("#songs-ready").text(ready);
    $("#songs-uploaded").text(uploaded);
}

// cleaning files
$.post("delete_user_file/");

Dropzone.autoDiscover = false;
var myDropzone = new Dropzone(document.body, { // Make the whole body a dropzone
    url: "dragdrop/", // Set the url
    thumbnailWidth: 80,
    thumbnailHeight: 80,
    parallelUploads: 1,
    previewTemplate: previewTemplate,
    maxFiles: 50,
    acceptedFiles:"audio/mpeg3,.mp3",
    autoQueue: false, // Make sure the files aren't queued until manually added
    previewsContainer: "#previews", // Define the container to display the previews
    dictFallbackMessage: "El navegador no soporta drag'n'drop.",
    dictInvalidFileType: "No puedes subir ficheros de este tipo: sólo se admite .mp3.",
    dictResponseError: "El servidor ha respondido con {{statusCode}} código.",
    dictMaxFilesExceeded: "No puedes subir más ficheros.",
    clickable: ".fileinput-button", // Define the element that should be used as click trigger to select files.
    headers: {
        'X-CSRFToken': csrftoken
    }
});

Dropzone.options.myDropzone = {
}

myDropzone.on("addedfile", function(file) {
    $("#songs-ready").text(++ready);
    // Hookup the start button
    file.previewElement.querySelector(".start").onclick =
    function() {
        console.log("startSongOnclick");
        myDropzone.enqueueFile(file);
    };
});

// Update the total progress bar
myDropzone.on("complete", function() {
    var i
    if (activeBar == 0){
        if (flag == 1) {
            parts = 100.0 / ready;
            flag = 0;
        }
        total += parts;
        document.querySelector("#total-progress .progress-bar").style.width = total + "%";
    }
});

myDropzone.on("sending", function(file) {
    console.log("sending");
    // Show the total progress bar when upload starts
    document.querySelector("#total-progress").style.opacity = "1";
    // And disable the start button
    file.previewElement.querySelector(".start").setAttribute("disabled", "disabled");
});

myDropzone.on("complete", function(file) {
    console.log("complete");
    $("#songs-uploaded").text(++uploaded);
    $("#songs-ready").text(--ready);
    // Show the total progress bar when upload starts
    file.previewElement.querySelector(".progress").style.display = "none";
    file.previewElement.querySelector(".cancel").style.visibility = "hidden";
    file.previewElement.querySelector(".start").style.visibility = "hidden";
    if (ERROR_UPLOAD==1) {
       ERROR_UPLOAD==0;
    } else {
       file.previewElement.querySelector(".msg-upload").style.visibility = "visible";
    }
});

// Hide the total progress bar when nothing's uploading anymore
myDropzone.on("queuecomplete", function(progress) {
    console.log("queueComplete");
    document.querySelector("#total-progress").style.opacity = "0";
});

// Setup the buttons for all transfers
// The "add files" button doesn't need to be setup because the config
// `clickable` has already been specified.
document.querySelector("#actions .start").onclick = function() {
    console.log("#actions .start onclick");
    activeBar = 0;
    myDropzone.enqueueFiles(myDropzone.getFilesWithStatus(Dropzone.ADDED));
    document.querySelector("#total-progress").style.visibility = "visible";
};

document.querySelector("#actions .delete").onclick = function() {
    console.log("#actions .delete onclick");
    myDropzone.removeAllFiles(true);
};

// When error, removing file
myDropzone.on("error", function(file) {
    $("#text-error").text("Error al preparar el archivo. Puede que el tipo no sea aceptado (sólo se acepta formato MP3)");
    $(".error-panel").css("display", "block");
    $(".error-panel").css("visibility", "visible");
    myDropzone.removeFile(file);
});

$(function(){
    $("[data-hide]").on("click", function(){
        $(this).closest("." + $(this).attr("data-hide")).hide();
    });
});

// CANCELED FILE
myDropzone.on("cancelledfile", function(file) {
    $("#songs-ready").text(--ready);  
});

// EXCEDED FILE NUMBER
myDropzone.on("excededfile", function(file) {
    $("#songs-uploaded").text(--uploaded);
});


// REMOVED FILE
myDropzone.on("removedfile", function(file) {
    $("#songs-uploaded").text(--uploaded);
    $.post("del_file/");
});

// MAX FILES
myDropzone.on("maxfilesexceeded", function(file) {
    $("#text-error").text("Número máximo de canciones alcanzado");
    $(".error-panel").css("visibility", "visible");
    myDropzone.removeFile(file);
});

deleteFilesFromTemplate = function() {
    _ref = myDropzone.files.slice();
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
	file = _ref[_i];
	if (file.status !== Dropzone.UPLOADING || cancelIfNecessary) {
	    var _reff;
	    if (file.previewElement) {
		if ((_reff = file.previewElement) != null) {
		    if ((_reff.parentNode)!=null)
			_reff.parentNode.removeChild(file.previewElement);
		}
	    }
	}
    }
    myDropzone.reset;
}
