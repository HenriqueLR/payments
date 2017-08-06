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
        context = {'ranges':{'Hoje':[moment(), moment()],
                   'Ontem':[moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                   'Últimos 7 dias':[moment().subtract(6, 'days'), moment()],
                   'Últimos 30 dias':[moment().subtract(29, 'days'), moment()],
                   'Este Mês':[moment().startOf('month'), moment().endOf('month')],
                   'Último Mês':[moment().subtract(1, 'month').startOf('month'),
                                 moment().subtract(1, 'month').endOf('month')]},
                   'linkedCalendars':false, 'buttonClasses':'btn btn-sm','opens':'left',
                   'applyClass':'btn-primary','cancelClass':'btn-danger',"autoApply":true
        }

        $.each(list_dict,function(key, value){
            $.extend(context, value);
        });

        return context;
    },
    get_locale:function(format_date){
        locale = {
            "locale":{
            "separator": " - ","applyLabel": "<i class='fa fa-check'></i>",
            "cancelLabel": "<i class='fa fa-times'></i>","fromLabel": "From",
            "toLabel": "To","customRangeLabel": "Calendário",
            "weekLabel": "W","daysOfWeek": ["Dom","Seg","Ter","Qua","Qui","Sex","Sab"],
            "monthNames": ["Janeiro","Fevereiro","Março","Abril",
                           "Maio","Junho","Julho","Agosto","Setembro",
                           "Outubro","Novembro","Dezembro"], "firstDay": 1},}
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
    get_custom_datetimepicker:function(date_format, dict){
        list_dict = [];
        list_dict.push(dict);
        list_dict.push(global_function.get_locale({"format": date_format}));
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
    set_session_left_menu:function(){
        if(Boolean(sessionStorage.getItem("layout-fullwidth"))){
            sessionStorage.setItem("layout-fullwidth", "");
        }else{sessionStorage.setItem("layout-fullwidth", "1");}
    },
    left_menu_set_status:function(){
        if(!Boolean(sessionStorage.getItem("layout-fullwidth"))){
            $('body').addClass('layout-fullwidth');
        }else{
            $('body').removeClass('layout-fullwidth');
        }
    },
    update_status_left_menu_session:function(){
        $.ajax({type: 'get', url: '/main/set_left_menu_session/'});
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
    get_form_delete_note:function(element){
        $.ajax({type:'get', url:'/wallet/delete_note/'+element.attr("id"),
            beforeSend:function(){
                element.find('.lnr').toggleClass('lnr lnr-trash fa fa-spinner fa-spin');
            },
            success:function(data){
                context = element.parents('li').find('.delete-context');
                context.html(data);
                context.fadeIn(600);
            },
            error:function(data){
                setTimeout(function(){
                    element.find('.fa').toggleClass('fa fa-spinner fa-spin lnr lnr-trash');
                }, 300);
            },
            complete:function(){
                setTimeout(function(){
                    element.find('.fa').toggleClass('fa fa-spinner fa-spin lnr lnr-trash');
                }, 300);
            },
        });
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
            beforeSend:function(){
                submit = form.find(":submit").prop('disabled', true);
                if(form.attr('name') == 'delete_note'){
                    submit.find('i.fa').toggleClass('fa fa-check fa fa-spinner fa-spin');
                }
            },
            success:function(data, textStatus, xhr){
                if(form.attr('name') == 'delete_note'){
                    setTimeout(function(){
                        $("#context-notes").html(data);
                    }, 800);
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
            error:function(data){
                if(form.attr('name') != 'delete_note'){
                    $("#modal-home").html(global_function.display_error_modal_dash());
                }else{
                    submit = form.find(":submit").prop('disabled', true);
                    setTimeout(function(){
                        submit.find('i.fa').toggleClass('fa fa-spinner fa-spin fa fa-warning');
                    }, 800);
                }
            },
            complete:function(){
                if(form.attr('name') != 'delete_note'){
                    form.find(":submit").prop('disabled', false);
                }
            },
        }).done(function(){
            if(form.attr('name') != 'delete_note'){
                $('input[name="date_note"]').daterangepicker(global_function.get_single_datetime());
            }
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
        console.log('left menu');
	    $('#left-nav li > a').removeClass('active');
	    $(this).addClass('active');
	});

    //CONTROLL ACTIONS OPEN MENU LEFT
    $("#open-menu").click(function(event) {
        console.log('open menu');
        event.preventDefault();

        //RESIZE GRAPHIC IF EXISTS
        if($("#overview").length){
            setTimeout(function(){
                graphics.adjust_graphic.call($('body'));
            }, 400);
        }

        //UPDATE STATUS LOCAL STORAGE LEFT MENU
        //global_function.set_session_left_menu();
        global_function.update_status_left_menu_session();
    });

    //INIT STATUS LEFT MENU LOCAL STORAGE
    //global_function.left_menu_set_status();


});//END READY FUNCTIONS