/* wallet js functions */

$(function() {
	//single input calendar
	if($('#list-debit').length){
		if($('input[name="date"]').val()){
			context = {"singleDatePicker": true, "startDate": $('input[name="date"]').val(),
			    		"endDate": "12/12/2017", "locale": {"format": 'DD/MM/YYYY'},}
		}else{
			context = {"singleDatePicker": true, "defaultDate": '', "locale": {"format": 'DD/MM/YYYY'},}

		}
		$('input[name="date"]').daterangepicker(context);
	}

});