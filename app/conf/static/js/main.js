// HOME

//OBJECT DEBIT / DEPOSIT
var releases = {
    list_debits_timeout:function(time){
        setTimeout(function(){releases.list_debits();}, time);
    },
    list_debits:function(){
        $.ajax({type:'get', url:'/wallet/list_debit/',
            success:function(data){$("#context-debits").html(data);},
            error:function(data){$("#context-debits").html("<h3>Não existem débitos cadastrados</h3>");},
        });
    },
    list_deposits_timeout:function(time){
        setTimeout(function(){releases.list_deposits();}, time);
    },
    list_deposits:function(){
        $.ajax({type:'get', url:'/wallet/list_deposit/',
            success:function(data){$("#context-deposits").html(data);},
            error:function(data){$("#context-deposits").html("<h3>Não existem depósitos cadastrados</h3>");},
        });
    },
    get_form_payment:function(url){
        $.ajax({type:'get', url:url,
            success:function(data){$("#modal-home").html(data);},
            error:function(data){console.log(data);$("#modal-home").html(global_function.display_error_modal_dash());},
        }).done(function(){$('input[name="date_releases"]').daterangepicker(global_function.get_single_datetime());});
    },
    send_form_debit:function(form){
        $.ajax({type:form.attr('method'),
            url:form.attr('action'),
            data:form.serialize(),
            beforeSend:function(){form.find(":submit").prop('disabled', true);},
            success:function(data, textStatus, xhr){
                if(form.attr('name') == 'delete_debit'){
                    $("#context-debits").html(data);
                    if(($(data).find("div.alert-success").length)){
                        graphics.get_overview_timeout(100);
                    }
                }else{
                    $("#modal-home").html(data);
                    if(($(data).find("div.alert-success").length)){
                        releases.list_debits_timeout(100);
                        graphics.get_overview_timeout(100);
                    }
                }
            },
            error:function(data){
                $("#modal-home").html(global_function.display_error_modal_dash());
            },
            complete:function(){
                form.find(":submit").prop('disabled', false);
            },
        }).done(function(){
            if(form.attr('name') != 'delete_debit'){
                $('input[name="date_releases"]').daterangepicker(global_function.get_single_datetime());
            }else{global_function.close_modal_dash(300);}
        });
    },
    send_form_deposit:function(form){
        $.ajax({type:form.attr('method'),
            url:form.attr('action'),
            data:form.serialize(),
            beforeSend:function(){form.find(":submit").prop('disabled', true);},
            success:function(data, textStatus, xhr){
                if(form.attr('name') == 'delete_deposit'){
                    $("#context-deposits").html(data);
                    if(($(data).find("div.alert-success").length)){
                        graphics.get_overview_timeout(100);
                    }
                }else{
                    $("#modal-home").html(data);
                    if(($(data).find("div.alert-success").length)){
                        releases.list_deposits_timeout(100);
                        graphics.get_overview_timeout(100);
                    }
                }
            },
            error:function(data){
                $("#modal-home").html(global_function.display_error_modal_dash());
            },
            complete:function(){
                form.find(":submit").prop('disabled', false);
            },
        }).done(function(){
            if(form.attr('name') != 'delete_deposit'){
                $('input[name="date_releases"]').daterangepicker(global_function.get_single_datetime());
            }else{global_function.close_modal_dash(300);}
        });
    },
};//END DEBIT / DEPOSIT

//OBJECT GRAPHIC
var graphics = {
    get_data_graphics:function(){
        $.ajax({
            type: 'get',
            url: '/main/graphics/',
            dataType: "json",
            success: function(data){
                if ((data[0].data.length > 0) || (data[1].data.length > 0)){
                    graphics.create_graphic(data);
                }else{
                    $('#chart-line').html('<h3 class="text-center">Não existem atividades \
                                            cadastradas para gerar o gráfico</h3>')
                }
            },
        });
    },
    create_graphic:function(data){
        $('#chart-line').highcharts({
            colors: ['#90ed7d','#f45b5b'],
            plotOptions: {series: {lineWidth:3,}},
            title: {text: ''},
            subtitle: {text: ''},
            yAxis: {title: {text: ''}},
            credits: {enabled: false},
            tooltip: {
                formatter:function(){
                    return '<b>' + this.point.series.name + '</b><br>Valor: <b>R$ '+ Highcharts.numberFormat(this.point.y,0,',','.') + '</b><br>Data: ' + Highcharts.dateFormat('%d/%m/%Y', this.x*1000);
                }
            },
            exporting: {enabled: false},
            xAxis: {
                type: 'datetime',
                labels: {
                    formatter:function(){
                        return Highcharts.dateFormat('%d/%m/%Y',this.value * 1000);
                    }
                },
                title: {text: ''},
            },
            series: data,
        });
    },
    adjust_graphic:function(chart){
        try {
            if (typeof (chart === 'undefined' || chart === null) && this instanceof jQuery) { // if no obj chart and the context is set

                this.find('.chart-container:visible').each(function () { // for only visible charts container in the curent context
                    $container = $(this); // context container
                    $container.find('div[id^="chart-"]').each(function () { // for only chart
                        $chart = $(this).highcharts(); // cast from JQuery to highcharts obj
                        $chart.setSize($container.width(), $chart.chartHeight, doAnimation = true); // adjust chart size with animation transition
                    });
                });
            } else {
                chart.setSize($('.chart-container:visible').width(), chart.chartHeight, doAnimation = true); // if chart is set, adjust
            }
        } catch (err) {
            // do nothing
        }
    },
    balance_charts:function(){
        $.ajax({type:'get', url:'/main/balance/',
            success:function(data){$("#totalizadores").html(data);},
        });
    },
    get_overview_timeout:function(time){
        setTimeout(function(){
            graphics.get_data_graphics();
            graphics.balance_charts();
        }, time);
    },
};//END OBJECT GRAPHIC

//GRAPHICS CONTROLL RESIZE
$(function(){
    //ADJUST SIZE FOR HIDDEN CHARTS
    $(window).resize(function () {
        if (this.resizeTO) clearTimeout(this.resizeTO);
            this.resizeTO = setTimeout(function () {
            // resizeEnd call function with pass context body
            graphics.adjust_graphic.call($('body'));}, 500);
    });
});//END GRAPHICS CONTROLL

//HOME ACTION CONTROLL
$(document).ready(function(){
    //CHECK EXISTS DIV NOTAS
    if($('#notes_home').length){
        //GET LIST NOTES
        note.list_note();

        //CHECKBOX UPDATE STATUS NOTE
        $('#notes_home #context-notes').on('click','input[type^="checkbox"]',function(){
            note.complet_list_item($(this));
            note.update_status_note($(this).attr("id"));
            //CALL UPDATE STATUS NOTE
            global_function.list_alerts_timeout(100);
        });

        //DELETE NOTE
        $('#notes_home #context-notes').on('click','.delete-note',function(e){
            note.get_form_note("/wallet/delete_note/"+$(this).attr("id"));
        });

        //EDIT NOTE
        $('#notes_home #context-notes').on('click','.edit-note',function(e){
            note.get_form_note("/wallet/update_note/"+$(this).attr("id"));
        });

        //GET ADD FORM NOTE
        $('#notes_home').on('click','.add-form',function(e){
            note.get_form_note('/wallet/add_note/');
        });

        //SUBMIT ADD/EDIT/DELETE FORM NOTE
        $('#modal-home').on('submit','.form-modal-note',function(e){
            e.preventDefault();
            note.send_form_note($(this));
        });
    }//END CHECK NOTES

    //CHECK EXISTS DIV PAYMENTS
    if($('#payments').length){
        //GET LIST DEBIT AND DEPOSITS
        releases.list_debits();
        releases.list_deposits();

        //GET ADD FORM DEBIT
        $('#payments #debit-col').on('click','.add-form',function(e){
            releases.get_form_payment('/wallet/add_debit/');
        });

        $('#payments #deposit-col').on('click','.add-form',function(e){
            releases.get_form_payment('/wallet/add_deposit/');
        });

        //DELETE DEBIT AND DEPOSITS
        $('#payments #context-deposits').on('click','.delete-deposit',function(e){
            releases.get_form_payment("/wallet/delete_deposit/"+$(this).attr("id"));
        });

        $('#payments #context-debits').on('click','.delete-debit',function(e){
            releases.get_form_payment("/wallet/delete_debit/"+$(this).attr("id"));
        });

        //SUBMIT ADD FORM DEBIT
        $('#modal-home').on('submit','.form-modal-debit',function(e){
            e.preventDefault();
            releases.send_form_debit($(this));
        });

        $('#modal-home').on('submit','.form-modal-deposit',function(e){
            e.preventDefault();
            releases.send_form_deposit($(this));
        });

        //EDIT NOTE
        $('#payments #context-debits').on('click','.edit-debit',function(e){
            releases.get_form_payment("/wallet/update_debit/"+$(this).attr("id"));
        });

        $('#payments #context-deposits').on('click','.edit-deposit',function(e){
            releases.get_form_payment("/wallet/update_deposit/"+$(this).attr("id"));
        });
    }//END CHECK PAYMENTS

    //CHECK EXISTS DIV OVERLOAD
    if($("#overview").length){
        //GET OVERVIEW
        graphics.get_overview_timeout(100);
    }//END CHECK OVERLOAD
});//END HOME ACTION CONTROLL