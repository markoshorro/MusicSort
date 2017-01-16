// handling logic in checkboxes
$('#options1').click(function() {
    if($('#default1').is(':checked')) {
	$('#default2').prop('checked',true);
	$("#options2").hide();
    } else {
	$("#options2").show();
    }
    $('#artist2').prop('disabled', false);
    $('#genre2').prop('disabled', false);
    $('#year2').prop('disabled', false);
    $('#album2').prop('disabled', false);
    if($('#artist1').is(':checked')) {
	$('#default2').prop("checked",true);
	$('#artist2').prop('disabled', true);
    }
    if($('#genre1').is(':checked')) {
	$('#default2').prop('checked',true);
	$('#genre2').prop('disabled', true);
    }
    if($('#year1').is(':checked')) {
	$('#default2').prop('checked',true);
	$('#year2').prop('disabled', true);
    }
    if($('#album1').is(':checked')) {
	$('#default2').prop('checked',true);
	$('#album2').prop('disabled', true);
    }
});
