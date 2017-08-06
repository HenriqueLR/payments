// ACCOUNTS

//OBJECT REGISTER
var register = {
	open_window_payment:function(url, time){
		setTimeout(function(){
			window.open(url, '_blank');
		}, time);
	},
}

//OBJECT USER
var user = {
	get_form_edit_password:function(url){
	    $.ajax({type:'get', url:url,
	        success:function(data){$("#modal_edit_password").html(data);},
	        error:function(data){$("#modal_edit_password").html(global_function.display_error_modal_dash());},
	    });
	},
    send_form_password:function(form){
        $.ajax({type:form.attr('method'),
            url:form.attr('action'),
            data:form.serialize(),
            beforeSend:function(){form.find(":submit").prop('disabled', true);},
            success:function(data, textStatus, xhr){
				if (data == 'ok'){
					window.location.href = form.attr('success-url');
				}else{
					$("#modal_edit_password").html(data);}
            },
            error:function(data){$("#modal_edit_password").html(global_function.display_error_modal_dash());},
            complete:function(){form.find(":submit").prop('disabled', false);},
        });//END CALL AJAX
    },
}//END OBJECT USER

//ACCOUNTS ACTION CONTROLL
$(function() {
	//SET DATE PLUGIN IN ADD - EDIT USER / PROFILE
	if($('.accounts-user').length){
		date_format = "DD/MM/YYYY"
		dict = {"singleDatePicker": true, "timePicker": false, "showDropdowns": true}
		$('input[name="birthday"]').daterangepicker(global_function.get_custom_datetimepicker(date_format, dict));
	}

    //GET ADD FORM EDIT PASSWORD
    $('.include-password').on('click','.form-password',function(e){
    	console.log('accounts form-password');
        user.get_form_edit_password($(this).attr("url-form"));
    });

	//SUBMIT FORM EDIT PASSWORD
	$('#modal_edit_password').on('submit','.form-modal-edit-password',function(e){
		console.log('form-modal-edit-password');
	    e.preventDefault();
	    user.send_form_password($(this));
	});

	//REGISTER ACTION CONTROL
	if($("#create_account_register").length){
		//AUTOMATIC OPEN WINDOW PAYMENT
		if($('.alert-info').length){
			register.open_window_payment($("#id_form_account").attr("url-payment"), 3500);
		}

		//SUBMIT FORM CREATE ACCOUNT
		$('#id_form_account').on('submit',function(e){
			$('#id_create_account').attr("disabled", true);
		});
	}//END REGISTER ACTION CONTROL

});//END ACCOUNTS ACTION CONTROLL