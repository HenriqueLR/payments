// WALLET

// WALLET ACTION CONTROLL
$(function() {
	// INPUT PLUGINS DATETIMEPICKER INIT
	$('input[name="date"]').daterangepicker(global_function.get_range_date());
	$('input[name="date_note"]').daterangepicker(global_function.get_single_datetime());
	$('input[name="date_releases"]').daterangepicker(global_function.get_single_datetime());

	//CHECK EXIST LIST-NOTE
	if($('#list_note').length){
        //ACTION CLICK CHECKBOX
	    $('#note-list-input input[type^="checkbox"]').click(function (e){
        	note.complet_list_item($(this));
            note.update_status_note($(this).attr("id"));
            //CALL UPDATE STATUS NOTE
            global_function.list_alerts_timeout(100);
	    });
	}

});// END WALLET ACTION CONTROLL