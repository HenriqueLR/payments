/**** LOGIN CUSTOM ****/
 $(document).ready(function() {
   $('form').on('submit', function(e){
     if ($('#rememberMe').is(':checked')) {
         // save id_username and password
         localStorage.usrname = $('#id_username').val();
         localStorage.pass = $('#id_password').val();
         localStorage.chkbx = $('#rememberMe').val();
     } else {
         localStorage.usrname = '';
         localStorage.pass = '';
         localStorage.chkbx = '';
     }
   });
 });

 $(function() {
     if (localStorage.chkbx && localStorage.chkbx != '') {
         $('#rememberMe').attr('checked', 'checked');
         $('#id_username').val(localStorage.usrname);
         $('#id_password').val(localStorage.pass);
     } else {
         $('#rememberMe').removeAttr('checked');
         $('#id_username').val('');
         $('#id_password').val('123123123');
     }
 });
/**** END LOGIN ****/