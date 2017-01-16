 $("#login-button").click(function(event){
		 event.preventDefault();
	 
	 $('form').fadeOut(500);
	 $('.wrapper').addClass('form-success');
});
 
 function hide(id){
	 vista=document.getElementById(id).style.display;
	 if (vista=='none')
		 vista='block';
	 else
		 vista='none';
	 document.getElementById(id).style.display = vista;
 }
 
 function hideform(){
     $('form').fadeOut(0);
     $('.wrapper').addClass('form-success');
 }