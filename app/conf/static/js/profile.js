/* Profile */

$(function() {
	/* single calendar input */
	$('input[name="birthday"]').daterangepicker({
	    "singleDatePicker": true,
	    "startDate": $('input[name="birthday"]').val(),
	    "endDate": "12/12/2017",
			"locale": {"format": 'DD/MM/YYYY'},
	});
});