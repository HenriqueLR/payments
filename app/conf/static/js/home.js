// HOME

//FUNCTION CREATE GRAPHIC
function create_graphic(data){
    $('#chart-line').highcharts({
        colors: ['#90ed7d','#f45b5b'],
        plotOptions: {
            series: {lineWidth:3,}
        },
        title: {text: ''},
        subtitle: {text: ''},
        yAxis: {title: {text: ''}},
        credits: {enabled: false},
        tooltip: {
            formatter:function(){
                return '<b>' + this.point.series.name + '</b><br>Valor: <b>R$ ' + Highcharts.numberFormat(this.point.y,0,',','.') + '</b><br>Data: ' + Highcharts.dateFormat('%d/%m/%Y', this.x*1000);
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
}

//FUNCTION EDIT STATUS NOTE
function note_get_function(url){
    $.ajax({type: 'get', url: url,});
    return false;
}

//FUNCTION GET DATA GRAPHIC
function get_graphics(){
    $.ajax({
        type: 'get',
        url: '/main/graphics/',
        dataType: "json",
        success: function(data){
            if ((data[0].data.length > 0) || (data[1].dataaa.length > 0)){
                create_graphic(data);
            }else{
                $('#chart-line').html('<h3 class="text-center">Nao existem atividades \
                                      cadastradas para gerar o grafico</h3>')
            }
        },
    });
}

//FUNCTION RESIZE GRAPHICS
function adjustGraph(chart) {
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
}

//INIT FUNCTIONS
$(function() {

    //INIT GRAPHIC
    get_graphics();

    //ADJUST SIZE FOR HIDDEN CHARTS
    $(window).resize(function () {
        if (this.resizeTO) clearTimeout(this.resizeTO);
            this.resizeTO = setTimeout(function () {
            // resizeEnd call function with pass context body
                adjustGraph.call($('body'));}, 500);
    });

    //RESIZE GRAPHIC CLICK OPEN MENU LEFT
    $("#open-menu").click(function(event) {
        event.preventDefault();
        setTimeout(function(){
            adjustGraph.call($('body'));
        }, 400);
    });

    //CHECK EXISTS DIV
    if($('#notas').length){

        //CONTROL EVENT CHECKBOX LIST NOTE
        $('#notas input[type^="checkbox"]').click(function (e) {
            url = '/wallet/list_note/?note='+$(this).attr("id");
            note_get_function(url);
            setTimeout(function(){
                get_list_alerts();
            }, 100);
        });

    }//ENDIF

}); //END FUNCTION