$(document).ready(function() {


	$("*").addClass("noselect");

	$(".list-item").click(function() {

		id = $(this).attr('id');

		$("body").find("." + id).show();
	});

	$(".closebar").click(function() { 
		$(this).parent().hide();
	});


});