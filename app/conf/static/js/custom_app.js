//GLOBAL FUNCTIONS
var global_function = {
    close_modal_dash:function(time){
        setTimeout(function(){$('#modal-home button[class="close"]').click();}, time);
    },
    display_error_modal_dash:function(){
        return '<div class="modal-header"><button aria-hidden="true" \
                data-dismiss="modal" class="close" type="button"> \
                <i style="font-size:15px;" class="lnr lnr-cross"></i> \
                </button><h4 class="modal-title">Error</h4></div> \
                <div class="modal-body"><div id="modal-home">Ocorreu um \
                erro, tente novamente.</div></div>';
    },
    get_config_datapicker:function(list_dict){
        context = {"ranges": {'Today': [moment(), moment()],
            'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Last 7 Days': [moment().subtract(6, 'days'), moment()],
            'Last 30 Days': [moment().subtract(29, 'days'), moment()],
            'This Month': [moment().startOf('month'), moment().endOf('month')],
            'Last Month': [moment().subtract(1, 'month').startOf('month'),
                           moment().subtract(1, 'month').endOf('month')]
        },"linkedCalendars": false,"opens": "left",}

        $.each(list_dict,function(key, value){
            $.extend(context, value);
        });

        return context;
    },
    get_locale:function(format_date){
        locale = {
            "locale":{
            "separator": " - ","applyLabel": "Apply",
            "cancelLabel": "Cancel","fromLabel": "From",
            "toLabel": "To","customRangeLabel": "Custom",
            "weekLabel": "W","daysOfWeek": ["Su","Mo","Tu","We","Th","Fr","Sa"],
            "monthNames": ["January","February","March","April",
                           "May","June","July","August","September",
                           "October","November","December"], "firstDay": 1},}
        if(format_date){
            $.extend(locale["locale"], format_date);
        }

        return locale;
    },
    get_single_datetime:function(){
        list_dict = [];
        list_dict.push({"singleDatePicker": true, "timePicker": true});
        list_dict.push(global_function.get_locale({"format": "DD/MM/YYYY h:mm"}));
        return global_function.get_config_datapicker(list_dict);
    },
    get_single_date:function(){
        list_dict = [];
        list_dict.push({"singleDatePicker": true, "timePicker": false});
        list_dict.push(global_function.get_locale({"format": "DD/MM/YYYY"}));
        return global_function.get_config_datapicker(list_dict);
    },
    get_range_date:function(){
        list_dict = [];
        list_dict.push({"singleDatePicker": false, "timePicker": false});
        list_dict.push(global_function.get_locale({"format": "DD/MM/YYYY"}));
        return global_function.get_config_datapicker(list_dict);
    },
    list_alerts_timeout:function(time){
        setTimeout(function(){global_function.list_alerts();},time);
    },
    list_alerts:function(){
		$.ajax({type: 'get',
		    url: '/main/alerts/',
		    success: function(data){$("#alerts-nav-bar").html(data);},
		    error: function (data){$("#alerts-nav-bar").html('Error');},
		});
    },
};//END GLOBAL FUNCTIONS

//OBJECT NOTE
var note = {
    list_note_timeout:function(time){
        setTimeout(function(){note.list_note();}, time);
    },
    list_note:function(){
        $.ajax({type:'get', url:'/wallet/list_note/',
            success:function(data){$("#context-notes").html(data);},
            error:function (data){$("#context-notes").html("<h3>Não existem notas cadastradas</h3>");},
        });
    },
    update_status_note:function(id){
        $.ajax({type:'get', url:'/wallet/update_status_note/'+id});
    },
    get_form_note:function(url){
        $.ajax({type:'get', url:url,
            success:function(data){$("#modal-home").html(data);},
            error:function(data){$("#modal-home").html(global_function.display_error_modal_dash());},
        }).done(function(){$('input[name="date_note"]').daterangepicker(global_function.get_single_datetime());});
    },
    send_form_note:function(form){
        $.ajax({type:form.attr('method'),
            url:form.attr('action'),
            data:form.serialize(),
            beforeSend:function(){form.find(":submit").prop('disabled', true);},
            success:function(data, textStatus, xhr){
                if(form.attr('name') == 'delete_note'){
                    $("#context-notes").html(data);
                    if(($(data).find("div.alert-success").length)){
                        global_function.list_alerts_timeout(100);
                    }
                }else{
                    $("#modal-home").html(data);
                    if(($(data).find("div.alert-success").length)){
                        global_function.list_alerts_timeout(100);
                        note.list_note_timeout(100);
                    }
                }
            },
            error:function(data){$("#modal-home").html(global_function.display_error_modal_dash());},
            complete:function(){form.find(":submit").prop('disabled', false);},
        }).done(function(){
            if(form.attr('name') != 'delete_note'){
                $('input[name="date_note"]').daterangepicker(global_function.get_single_datetime());
            }else{global_function.close_modal_dash(300);}
        });//END CALL AJAX
    },
	complet_list_item:function(item){
		if(item.prop('checked')){item.parents('li').addClass('completed');}
		else{item.parents('li').removeClass('completed');}
	},
};//END NOTE OBJECT

//READY FUNCTIONS
$(function(){
	//LIST ALERTS
	if($('#alerts-nav-bar').length){global_function.list_alerts_timeout(100);}

	//ACTIVE ITEM MENU LEFT
	$('#left-nav').on('click', 'li > a', function(){
	    $('#left-nav li > a').removeClass('active');
	    $(this).addClass('active');
	});
});//END READY FUNCTIONS