// Typekit
try{Typekit.load({ async: true });}catch(e){}


// Append arrow to button text
$(document).ready(function() {
	//var template_url="<?php echo bloginfo('template_url'); ?>";

	$('.cta').append('<img src="/static/Plants/icon-white-arw.png" />');

})