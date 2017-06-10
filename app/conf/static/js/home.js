
/*** HOME ***/

/* FUNCTION RESIZE GRAPHICS */
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

$(function() {
    /**
    * Adjust size for hidden charts
    * @param chart highcharts
    */
    $(window).resize(function () {
        if (this.resizeTO) clearTimeout(this.resizeTO);
            this.resizeTO = setTimeout(function () {
            // resizeEnd call function with pass context body
                adjustGraph.call($('body'));}, 500);
    });

    /* GRAPHIC HOME */
    $('#chart-line').highcharts({
        colors: ['#90ed7d','#f45b5b'],
        plotOptions: {
            series: {lineWidth:3,}
        },
        title: {text: ''},
        subtitle: {text: ''},
        yAxis: {
            title: {text: ''}
        },
        credits: {enabled: false},
        tooltip: {
            formatter:function(){
                return '<b>' + this.point.series.name + '</b><br>Valor: <b>R$ ' + Highcharts.numberFormat(this.point.y,0,',','.') + '</b><br>Data: ' + Highcharts.dateFormat('%d/%m/%Y',new Date(this.x));
            }
        },
        exporting: {enabled: false},
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: { // don't display the dummy year
                month: '%e. %b',
                year: '%b'
            },
            title: {text: ''}
        },
        series: [{name: 'Depósitos',
                data: [[Date.UTC(2017, 01, 01), 500],[Date.UTC(2017, 01, 02), 43934],
                       [Date.UTC(2017, 01, 03), 52503], [Date.UTC(2017, 01, 04), 57177],
                       [Date.UTC(2017, 01, 05), 69658], [Date.UTC(2017, 01, 06), 97031]]},
                {name: 'Débitos',
                data: [[Date.UTC(2017, 01, 01), 24916],[Date.UTC(2017, 01, 02), 24064],
                       [Date.UTC(2017, 01, 03), 80000], [Date.UTC(2017, 01, 04), 29851],
                       [Date.UTC(2017, 01, 05), 32490], [Date.UTC(2017, 01, 06), 30282],
                       [Date.UTC(2017, 01, 07), 38121], [Date.UTC(2017, 01, 08), 40434],
                       [Date.UTC(2017, 01, 09), 1000]]},]
    });

    /* RESIZE GRAPHIC CLICK OPEN MENU LEFT */
    $("#open-menu").click(function(event) {
        event.preventDefault();
        setTimeout(function(){
            adjustGraph.call($('body'));
        }, 400);
    });

}); //end function