//ACTIVE ITEM MENU LEFT
$('#left-nav').on('click', 'li > a', function(){
    $('#left-nav li > a').removeClass('active');
    $(this).addClass('active');
});

//GET LIST ALERTS
function get_list_alerts(){
	$.ajax({
	    type: 'get',
	    url: '/main/alerts/',
	    success: function(data) {
	        $("#alerts-nav-bar").html(data);
	    },
	    error: function (data) {
	        $("#alerts-nav-bar").html('Error');
	    },
	});
}

//READY FUNCTIONS
$(function(){
	get_list_alerts();
});