
/* ACTIVE ITEM MENU LEFT */
$('#left-nav').on('click', 'li > a', function(){
    $('#left-nav li > a').removeClass('active');
    $(this).addClass('active');
});