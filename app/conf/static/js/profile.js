/* Profile */

$(function() {
	//single input calendar
	if($('input[name="birthday"]').val()){
		context = {"singleDatePicker": true, "startDate": $('input[name="birthday"]').val(),
		    		"endDate": "12/12/2017", "locale": {"format": 'DD/MM/YYYY'},}
	}else{
		context = {"singleDatePicker": true, "defaultDate": '', "locale": {"format": 'DD/MM/YYYY'},}

	}
	$('input[name="birthday"]').daterangepicker(context);
});