// handling ajax events
$(document).ready(function() {
    $("#download-spinner").css("visibility","hidden");
    $("#download-button").click(function(e) {
    e.preventDefault();  //stop the browser from following
    $("#download-spinner").css("visibility","visible");
    l1 = $('input[name=radioInline1]:checked').val();
    l2 = $('input[name=radioInline2]:checked').val();
    lyrics = $('#lyrics').is(':checked');
    $(".info-download").removeClass('alert-success').addClass('alert-info');
    $(".info-download").css("visibility", "visible");
    $("#info-download-msg").text("Procesando canciones. Por favor, sea paciente");
    $.ajax({
            method: 'POST',
            url: 'process_songs/',
            data: {'index1': l1, 'index2': l2, 'lyrics': lyrics},
        success: function(data, status, response) {
            $("#info-download-msg").text("Generando zip. Por favor, sea paciente");
            window.location.assign('process_songs/');
            $("#download-spinner").css("visibility","hidden");
            $(".info-download").css("visibility", "hidden");
            $(".info-download").toggleClass('alert-info alert-success');
            $(".info-download").css("visibility", "visible");
            $("#info-download-msg").text("¡Proceso finalizado!");
	    deleteFilesFromTemplate();
	    resetValues();
        },
        error: function(data) {
	    alert("Se ha producido un error en el servidor");
	    $("#download-spinner").css("visibility","hidden");
        },
    });
    }); // end click download button
});
