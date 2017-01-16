$(document).ready(function() {
	document.getElementById("login-button").disabled = true;
    $('#id_password1').keyup(function() {
	$('#result').html(checkStrength($('#id_password1').val()))
    })
    function checkStrength(password) {
	var strength = 0
	if (password.length < 8) {
	    $('#result').removeClass()
	    $('#result').addClass('short')
	    $('#login-button').removeClass()
	    $('#login-button').addClass('btn btn-lg btn-primary btn-block disabled')
	    return 'Corta'
	}
	if (password.length > 8) strength += 1
	// If password contains both lower and uppercase characters, increase strength value.
	if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) strength += 1
	// If it has numbers and characters, increase strength value.
	if (password.match(/([a-zA-Z])/) && password.match(/([0-9])/)) strength += 1
	// If it has one special character, increase strength value.
	if (password.match(/([!,%,&,@,#,$,^,*,?,_,~])/)) strength += 1
	// If it has two special characters, increase strength value.
	if (password.match(/(.*[!,%,&,@,#,$,^,*,?,_,~].*[!,%,&,@,#,$,^,*,?,_,~])/)) strength += 1
	// Calculated strength value, we can return messages
	// If value is less than 2
	$('#login-button').removeClass()
	$('#login-button').addClass('btn btn-lg btn-primary btn-block')
	document.getElementById("login-button").disabled = false;
	if (strength < 2) {
	    $('#result').removeClass()
	    $('#result').addClass('weak')
	    var res = 'Débil'; var esp = '\xa0'
	    for (var i = 0; i < 10; i++) {
	    	esp = esp.concat('\xa0');
	    };
	    return res.concat(esp)
	} else if (strength == 2) {
	    $('#result').removeClass()
	    $('#result').addClass('good')
	    var res = 'Buena'; var esp = '\xa0'
	    for (var i = 0; i < 25; i++) {
	    	esp = esp.concat('\xa0');
	    };
	    return res.concat(esp)
	} else {
	    $('#result').removeClass()
	    $('#result').addClass('strong')
		var res = 'Fuerte'; var esp = '\xa0'
	    for (var i = 0; i < 40; i++) {
	    	esp = esp.concat('\xa0');
	    };
	    return res.concat(esp)
	    }
    }
});
