// LOGIN

//OBJECT LOGIN
var login = {
    remember_local_store:function(){
         if(localStorage.chkbx && localStorage.chkbx != ''){
             $('#rememberMe').attr('checked', 'checked');
             $('#id_username').val(localStorage.usrname);
             $('#id_password').val(localStorage.pass);
         }else{
             $('#rememberMe').removeAttr('checked');
             $('#id_username').val('');
             $('#id_password').val('');
         }
    },
    remember_submit_form:function(){
        if($('#rememberMe').is(':checked')){
            // save id_username and password
            localStorage.usrname = $('#id_username').val();
            localStorage.pass = $('#id_password').val();
            localStorage.chkbx = $('#rememberMe').val();
        }else{
            localStorage.usrname = '';
            localStorage.pass = '';
            localStorage.chkbx = '';
        }
    },
    get_form_reset_password:function(url){
        $.ajax({type:'get', url:url,
            success:function(data){$("#modal_recovery_password").html(data);},
            error:function (data){$("#modal_recovery_password").html(global_function.display_error_modal_dash());},
        });
    },
    send_form_reset_password:function(form){
        $.ajax({type:form.attr('method'),
            url:form.attr('action'),
            data:form.serialize(),
            beforeSend:function(){form.find(":submit").prop('disabled', true);},
            success:function(data, textStatus, xhr){
				if (data == 'ok'){window.location.href = form.attr('success-url');}
				else{$("#modal_recovery_password").html(data);}
            },
            error:function(data){$("#modal_recovery_password").html(global_function.display_error_modal_dash());},
            complete:function(){form.find(":submit").prop('disabled', false);},
        });//END CALL AJAX
    },
}//END OBJECT LOGIN

//LOGIN ACTION CONTROLL
$(document).ready(function() {
    //SUBMIT FORM LOGIN CHECK SAVE LOCALSTORE
    $('#login-form').on('submit', function(e){
        login.remember_submit_form();
    });

    //SET VAL LOGIN INPUT LOCALSTORE
    login.remember_local_store();

    //GET FORM RESET PASSWORD
    $("#login-form").on('click', '.recovery_password', function(){
    	login.get_form_reset_password($(this).attr("url-form"));
    });

    //SUBMIT RESET PASSWORD LOGIN
    $('#modal_recovery_password').on('submit','#reset_password',function(e){
        e.preventDefault();
        login.send_form_reset_password($(this));
    });
});//END LOGIN ACTION CONTROLL