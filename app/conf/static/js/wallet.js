// WALLET

$(function() {
	//CHECK EXISTS LIST-DEBIT
	if($('#list-debit').length){
		list_dict = [];
		list_dict.push({"timePicker": false});
		list_dict.push(get_locale({"format": "DD/MM/YYYY"}));
		$('input[name="date"]').daterangepicker(get_config_datapicker(list_dict));
		/*if($('input[name="date"]').val()){
			context = {"singleDatePicker": true, "startDate": $('input[name="date"]').val(),
			    		"endDate": "12/12/2017", "locale": {"format": 'DD/MM/YYYY'},}
		}else{
			context = {"singleDatePicker": true, "defaultDate": '', "locale": {"format": 'DD/MM/YYYY'},}

		}
		$('input[name="date"]').daterangepicker(context);*/
	}

	//CHECK EXISTS LIST-DEPOSIT
	if($('#list-deposit').length){
		list_dict = [];
		list_dict.push({"timePicker": false});
		list_dict.push(get_locale({"format": "DD/MM/YYYY"}));
		$('input[name="date"]').daterangepicker(get_config_datapicker(list_dict));
	}

	//CHECK EXIST LIST-NOTE
	if($('#list_note').length){
		list_dict = [];
		list_dict.push({"timePicker": false});
		list_dict.push(get_locale({"format": "DD/MM/YYYY"}));
		$('input[name="date"]').daterangepicker(get_config_datapicker(list_dict));

		//ACTION CLICK CHECKBOX
	    $('#note-list-input input[type^="checkbox"]').click(function (e){
			if($(this).prop('checked')){$(this).parents('li').addClass('completed');}
            else{$(this).parents('li').removeClass('completed');}
	     	url = '/wallet/update_status_note/'+$(this).attr("id");
	     	note_get_function(url);
            setTimeout(function(){
                get_list_alerts();
            }, 100);
	    });

	    //CALL AJAX GET URL
		function note_get_function(url){
		  $.ajax({type: 'get', url: url,});
		  return false;
		}
	}

	//CHECK EXIST NOTE
	if($('#note')){
		list_dict = [];
		list_dict.push({"singleDatePicker": true,"timePicker": true});
		list_dict.push(get_locale({"format": "DD/MM/YYYY h:mm"}));
		$('input[name="date_note"]').daterangepicker(get_config_datapicker(list_dict));
	}

	//CECK EXISTS ELEMENT ADD-DEPOSIT
	if($('#add-deposit')){
		list_dict = [];
		list_dict.push({"singleDatePicker": true,"timePicker": true});
		list_dict.push(get_locale({"format": "DD/MM/YYYY h:mm"}));
		$('input[name="date_releases"]').daterangepicker(get_config_datapicker(list_dict));
	}

	//CHECK EXISTS ELEMENT ADD-DEBIT
	if($('#add-debit')){
		list_dict = [];
		list_dict.push({"singleDatePicker": true,"timePicker": true});
		list_dict.push(get_locale({"format": "DD/MM/YYYY h:mm"}));
		$('input[name="date_releases"]').daterangepicker(get_config_datapicker(list_dict));
	}

	//GET CONFIG DATAPICKER
	function get_config_datapicker(list_dict){
		context = {
		 "ranges": {
			'Today': [moment(), moment()],
			'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
			'Last 7 Days': [moment().subtract(6, 'days'), moment()],
			'Last 30 Days': [moment().subtract(29, 'days'), moment()],
			'This Month': [moment().startOf('month'), moment().endOf('month')],
			'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
		},
		 "linkedCalendars": false,
		 "opens": "left",
		}

		$.each(list_dict, function(key, value) {
			$.extend(context, value);
		});
		return context;
	}

	//GET LOCALE
	function get_locale(format_date){
		locale = {
			"locale": {
		    "separator": " - ",
		    "applyLabel": "Apply",
		    "cancelLabel": "Cancel",
		    "fromLabel": "From",
		    "toLabel": "To",
		    "customRangeLabel": "Custom",
		    "weekLabel": "W",
		    "daysOfWeek": ["Su","Mo","Tu","We","Th","Fr","Sa"],
		    "monthNames": ["January","February","March","April","May","June","July",
		    			   "August","September","October","November","December"],
		    "firstDay": 1
			},
		}
		if(format_date){
			$.extend(locale["locale"], format_date);
		}
		return locale;
	}

});//END GLOBAL FUNCTION