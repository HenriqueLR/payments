
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

    /* RESIZE GRAPHIC CLICK OPEN MENU LEFT */
    $("#open-menu").click(function(event) {
        event.preventDefault();
        setTimeout(function(){
            adjustGraph.call($('body'));
        }, 400);
    });

}); //end function