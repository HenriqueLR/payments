/* wallet js functions */

$(function() {
	//single input calendar
	if($('#list-debit').length){
		$('input[name="date"]').daterangepicker({"locale": {"format": 'DD/MM/YYYY'}});
		/*if($('input[name="date"]').val()){
			context = {"singleDatePicker": true, "startDate": $('input[name="date"]').val(),
			    		"endDate": "12/12/2017", "locale": {"format": 'DD/MM/YYYY'},}
		}else{
			context = {"singleDatePicker": true, "defaultDate": '', "locale": {"format": 'DD/MM/YYYY'},}

		}
		$('input[name="date"]').daterangepicker(context);*/
	}

	if($('#list-deposit').length){
		$('input[name="date"]').daterangepicker({"locale": {"format": 'DD/MM/YYYY'}});
	}

	if($('#list-note').length){
		$('input[name="date"]').daterangepicker({"locale": {"format": 'DD/MM/YYYY'}});

	    $('#note-list-input input[type^="checkbox"]').click(function (e) {
	     	url = '/wallet/list_note/?note='+$(this).attr("id");
	     	note_get_function(url)
	    });

		function note_get_function(url){
		  $.ajax({type: 'get', url: url,});
		  return false;
		}

	}

});