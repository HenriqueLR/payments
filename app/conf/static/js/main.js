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
    get_form_delete_deposit:function(element){
        $.ajax({type:'get', url:'/wallet/delete_deposit/'+element.attr("id"),
            beforeSend:function(){
                element.find('.lnr').toggleClass('lnr lnr-trash fa fa-spinner fa-spin');
            },
            success:function(data){
                context = element.parents('.actions').find('.delete-context-table');
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
    get_form_delete_debit:function(element){
        $.ajax({type:'get', url:'/wallet/delete_debit/'+element.attr("id"),
            beforeSend:function(){
                element.find('.lnr').toggleClass('lnr lnr-trash fa fa-spinner fa-spin');
            },
            success:function(data){
                context = element.parents('.actions').find('.delete-context-table');
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
    get_form_payment:function(url){
        $.ajax({type:'get', url:url,
            success:function(data){$("#modal-home").html(data);},
            error:function(data){$("#modal-home").html(global_function.display_error_modal_dash());},
        }).done(function(){$('input[name="date_releases"]').daterangepicker(global_function.get_single_datetime());});
    },
    send_form_debit:function(form){
        $.ajax({type:form.attr('method'),
            url:form.attr('action'),
            data:form.serialize(),
            beforeSend:function(){
                submit = form.find(":submit").prop('disabled', true);
                if(form.attr('name') == 'delete_debit'){
                    submit.find('i.fa').toggleClass('fa fa-check fa fa-spinner fa-spin');
                }
            },
            success:function(data, textStatus, xhr){
                if(form.attr('name') == 'delete_debit'){
                    setTimeout(function(){
                        $("#context-debits").html(data);
                    }, 800);
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
                if(form.attr('name') != 'delete_debit'){
                    $("#modal-home").html(global_function.display_error_modal_dash());
                }else{
                    submit = form.find(":submit").prop('disabled', true);
                    setTimeout(function(){
                        submit.find('i.fa').toggleClass('fa fa-spinner fa-spin fa fa-warning');
                    }, 800);
                }
            },
            complete:function(){
                if(form.attr('name') != 'delete_debit'){
                    form.find(":submit").prop('disabled', false);
                }
            },
        }).done(function(){
            if(form.attr('name') != 'delete_debit'){
                $('input[name="date_releases"]').daterangepicker(global_function.get_single_datetime());
            }
        });
    },
    send_form_deposit:function(form){
        $.ajax({type:form.attr('method'),
            url:form.attr('action'),
            data:form.serialize(),
            beforeSend:function(){
                submit = form.find(":submit").prop('disabled', true);
                if(form.attr('name') == 'delete_deposit'){
                    submit.find('i.fa').toggleClass('fa fa-check fa fa-spinner fa-spin');
                }
            },
            success:function(data, textStatus, xhr){
                if(form.attr('name') == 'delete_deposit'){
                    setTimeout(function(){
                        $("#context-deposits").html(data);
                    }, 800);
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
                if(form.attr('name') != 'delete_deposit'){
                    $("#modal-home").html(global_function.display_error_modal_dash());
                }else{
                    submit = form.find(":submit").prop('disabled', true);
                    setTimeout(function(){
                        submit.find('i.fa').toggleClass('fa fa-spinner fa-spin fa fa-warning');
                    }, 800);
                }
            },
            complete:function(){
                if(form.attr('name') != 'delete_deposit'){
                    form.find(":submit").prop('disabled', false);
                }
            },
        }).done(function(){
            if(form.attr('name') != 'delete_deposit'){
                $('input[name="date_releases"]').daterangepicker(global_function.get_single_datetime());
            }
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
                    return '<b>' + this.point.series.name + '</b><br>Valor: R$ '+
                    Highcharts.numberFormat(this.point.y,2,',','.') + '<br>Data: '+
                    Highcharts.dateFormat('%d/%m/%Y', this.x*1000);
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
$(document).ready(function() {
    //CHECK EXISTS DIV NOTAS
    if($('#notes_home').length) {
        //GET LIST NOTES
        note.list_note();

        //CHECKBOX UPDATE STATUS NOTE
        $('#notes_home #context-notes').on('click','input[type^="checkbox"]',function(){
            console.log('input[type^="checkbox"]');
            note.complet_list_item($(this));
            note.update_status_note($(this).attr("id"));
            //CALL UPDATE STATUS NOTE
            global_function.list_alerts_timeout(100);
        });

        //GET DELETE FORM NOTE
        $('#notes_home #context-notes').on('click','.delete-note',function(e){
            console.log('delete-note');
            e.preventDefault();
            note.get_form_delete_note($(this));
            //note.get_form_note("/wallet/delete_note/"+$(this).attr("id"));
        });
        //CLOSE BOX BTN DELETE NOTE
        $('#notes_home #context-notes').on('click', '.delete-context .btn-close-custom',
            function(e){
                console.log('close box btn delete note');
                e.preventDefault();
                $(this).parents('.delete-context').fadeOut(600);
        });
        //SUBMIT DELETE FORM NOTE
        $('#notes_home #context-notes').on('submit','.delete-context .form-delete-note',function(e){
            console.log('form-delete-note');
            e.preventDefault();
            note.send_form_note($(this));
        });

        //GET EDIT FORM NOTE
        $('#notes_home #context-notes').on('click','.edit-note',function(e){
            console.log('edit-note');
            note.get_form_note("/wallet/update_note/"+$(this).attr("id"));
        });

        //GET ADD FORM NOTE
        $('#notes_home').on('click','.add-form',function(e){
            console.log('add-form');
            note.get_form_note('/wallet/add_note/');
        });

        //SUBMIT ADD/EDIT FORM NOTE
        $('#modal-home').on('submit','.form-modal-note',function(e){
            console.log('form-modal-note');
            e.preventDefault();
            note.send_form_note($(this));
        });
    }//END CHECK NOTES

    //CHECK EXISTS DIV PAYMENTS
    if($('#payments').length) {
        //GET LIST DEBIT AND DEPOSITS
        releases.list_debits();
        releases.list_deposits();

        //GET ADD FORM DEBIT
        $('#payments #debit-col').on('click','.add-form',function(e){
            console.log('add-form');
            releases.get_form_payment('/wallet/add_debit/');
        });

        $('#payments #deposit-col').on('click','.add-form',function(e){
            console.log('add-form');
            releases.get_form_payment('/wallet/add_deposit/');
        });

        //GET DETAIL BOX TR TABLE DEPOSITS
        $('#payments #deposit-col').on('click','#context-deposits .open-dialog',function(e){
            console.log('click tr');
            element_box = $(this).parents('tr').find('.open-dialog-box');
            element_td = element_box.parents('td');
            element_box.remove();
            element_td.addClass('open-dialog');

            parents_box = $(this).parents('tbody').find('.open-dialog-box');
            if(parents_box.length > 0){
                console.log('parents box dialog');
                //SET INPUTS STAGE SESSION
                for(var i = 0; i < parents_box.length; i += 1) {
                    element_box_parents = $(parents_box[i]).parents('tr').find('.open-dialog-box');
                    element_td_parents = element_box_parents.parents('td');
                    element_box_parents.remove();
                    element_td_parents.addClass('open-dialog');
                }
            }

            $(this).removeClass('open-dialog');
            $(this).append('<div class="open-dialog-box"> \
                    <div class="panel-heading"> \
                        <h3 class="panel-title">Detalhes do depósito</h3> \
                        <div class="right"> \
                            <button type="button" class="btn-remove"> \
                                <i class="lnr lnr-cross-circle"></i> \
                            </button> \
                        </div> \
                    </div> \
                    <div class="panel-body"> \
                    <div class="col-md-12 text-center"> \
                        <span class="fa fa-spinner fa-spin"></span> \
                    </div> \
                    </div> \
                    </div>');

            element = $(this);
            actions_parents = $(this).parents('tr').find('.actions');

            element.find('.open-dialog-box').show('fade', 'slow', function(){
                context = element.find('.open-dialog-box');

                url = '/wallet/detail_deposit/'+actions_parents.find('a:first-child').attr('id');
                //context.load(url);

                $.ajax({type:'get', url: url,
                    success:function(data){
                        context.html(data);
                    },
                });

            });
        });

        //CLOSE DETAIL BOX TR TABLE DEPOSITS
        $('#payments #deposit-col').on('click','#context-deposits .open-dialog-box .btn-remove', function(e){
            console.log('close detail box');
            $(this).parents('td').addClass('open-dialog');
            $(this).parents('.open-dialog-box').remove();
        });

        //GET FORM DELETE DEPOSIT
        $('#payments #context-deposits').on('click','.delete-deposit', function(e){
            console.log('delete-deposit');
            e.preventDefault();
            releases.get_form_delete_deposit($(this));
            //releases.get_form_payment("/wallet/delete_deposit/"+$(this).attr("id"));
        });
        //SUBMIT DELETE FORM DEPOSIT
        $('#payments #context-deposits').on('submit','.delete-context-table .form-delete-deposit',
            function(e){
                console.log('form-delete-deposit');
                e.preventDefault();
                releases.send_form_deposit($(this));
        });

        //CLOSE BOX BTN DELETE DEPOSIT / DEBIT
        $('#payments').on('click', '.delete-context-table .btn-close-custom',
            function(e){
                console.log('close box btn delete deposit debit');
                e.preventDefault();
                $(this).parents('.delete-context-table').fadeOut(600);
        });

        //GET FORM DELETE DEBIT
        $('#payments #context-debits').on('click','.delete-debit', function(e){
            console.log('delete-debit');
            e.preventDefault();
            releases.get_form_delete_debit($(this));
        });
        //SUBMIT DELETE FORM DEBIT
        $('#payments #context-debits').on('submit','.delete-context-table .form-delete-debit',
            function(e){
                console.log('form-delete-debit');
                e.preventDefault();
                releases.send_form_debit($(this));
        });

        //GET DETAIL BOX TR TABLE DEBITS
        $('#payments #debit-col').on('click','#context-debits .open-dialog',function(e){
            console.log('click tr debit');
            element_box = $(this).parents('tr').find('.open-dialog-box');
            element_td = element_box.parents('td');
            element_box.remove();
            element_td.addClass('open-dialog');

            parents_box = $(this).parents('tbody').find('.open-dialog-box');
            if(parents_box.length > 0){
                console.log('parents box dialog');
                //SET INPUTS STAGE SESSION
                for(var i = 0; i < parents_box.length; i += 1) {
                    element_box_parents = $(parents_box[i]).parents('tr').find('.open-dialog-box');
                    element_td_parents = element_box_parents.parents('td');
                    element_box_parents.remove();
                    element_td_parents.addClass('open-dialog');
                }
            }

            $(this).removeClass('open-dialog');
            $(this).append('<div class="open-dialog-box"> \
                    <div class="panel-heading"> \
                        <h3 class="panel-title">Detalhes do débito</h3> \
                        <div class="right"> \
                            <button type="button" class="btn-remove"> \
                                <i class="lnr lnr-cross-circle"></i> \
                            </button> \
                        </div> \
                    </div> \
                    <div class="panel-body"> \
                    <div class="col-md-12 text-center"> \
                        <span class="fa fa-spinner fa-spin"></span> \
                    </div> \
                    </div> \
                    </div>');

            element = $(this);
            actions_parents = $(this).parents('tr').find('.actions');

            element.find('.open-dialog-box').show('fade', 'slow', function(){
                context = element.find('.open-dialog-box');

                url = '/wallet/detail_debit/'+actions_parents.find('a:first-child').attr('id');
                //context.load(url);

                $.ajax({type:'get', url: url,
                    success:function(data){
                        context.html(data);
                    },
                });

            });
        });

        //CLOSE DETAIL BOX TR TABLE DEPOSITS
        $('#payments #debit-col').on('click','#context-debits .open-dialog-box .btn-remove', function(e){
            console.log('close detail box');
            $(this).parents('td').addClass('open-dialog');
            $(this).parents('.open-dialog-box').remove();
        });

        //SUBMIT ADD FORM DEBIT
        $('#modal-home').on('submit','.form-modal-debit',function(e){
            console.log('form-modal-debit');
            e.preventDefault();
            releases.send_form_debit($(this));
        });

        $('#modal-home').on('submit','.form-modal-deposit',function(e){
            console.log('form-modal-deposit');
            e.preventDefault();
            releases.send_form_deposit($(this));
        });

        //EDIT NOTE
        $('#payments #context-debits').on('click','.edit-debit',function(e){
            console.log('edit-debit');
            releases.get_form_payment("/wallet/update_debit/"+$(this).attr("id"));
        });

        $('#payments #context-deposits').on('click','.edit-deposit',function(e){
            console.log('edit-deposit');
            releases.get_form_payment("/wallet/update_deposit/"+$(this).attr("id"));
        });
    }//END CHECK PAYMENTS

    //CHECK EXISTS DIV OVERLOAD
    if($("#overview").length) {
        //GET OVERVIEW
        graphics.get_overview_timeout(100);

        //RESIZE GRAPH IN COLLAPSE EVENT BTN OVERVIEW
        $('#overview').on('click', '.btn-toggle-collapse', function(event){
            console.log('btn-toggle-collapse');
            event.preventDefault();
            setTimeout(function(){
                graphics.adjust_graphic.call($('body'));
            }, 400);
        });
    }//END CHECK OVERLOAD

    //CONFIG CHARTS HOME
    if(($("#overview").length) &&
        ($('#payments').length) &&
        ($('#notes_home').length)) {

        //SET INPUTS STAGE SESSION
        for(var i = 0; i < sessionStorage.length; i += 1) {
            input_element = $('.config-home').find('input[name^="'+sessionStorage.key(i)+'"]');
            if(Boolean(parseInt(sessionStorage.getItem(sessionStorage.key(i))))){
                input_element.prop('checked', !Boolean(parseInt(sessionStorage.getItem(sessionStorage.key(i)))));
                id_element = '#'+input_element.attr('name');
                $(id_element).hide();
            }
        }

        //CLICK CONTROLL FADE
        $('.config-home').on('click', '.dropdown-btn', function(e) {
            console.log('dropdown-btn');
            e.preventDefault();
            dropdown_element = $('.config-home').find('.dropdown-menu-config');
            button_element = $('.config-home').find('i').addClass('fa-spin');
            if(dropdown_element.css('display') == 'none') {
                dropdown_element.show('fade', 'slow',
                    function(){button_element.removeClass('fa-spin');});
            }else{
                dropdown_element.hide('fade', 'slow',
                    function(){button_element.removeClass('fa-spin');});
            }
        });

        //CHECKBOX CONTROLL
        $('.config-home').on('click', 'input[type^="checkbox"]', function(e) {
            console.log('input[type^="checkbox"]');
            var id_element = '#'+$(this).attr('name');
            setTimeout(function(){
                graphics.adjust_graphic.call($('body'));
            }, 400);

            if($(this).prop('checked')){
                sessionStorage.setItem($(this).attr('name'), "0");
                $(id_element).fadeIn(600);
            }
            else{
                sessionStorage.setItem($(this).attr('name'), "1");
                $(id_element).fadeOut(600);
            }
        });
    }//END CHARTS HOME

});//END HOME ACTION CONTROLL