$(document).ready(function() {
    console.log("Appointment cgi ready!");
    getAppointments();
});


function getAppointments() {
    console.log("in get appointments, sending ajax");
    var response;
    var url = '/index.cgi';
    var data = {
        //ajax_query: $('#search_params').val(),
        ajax_query: '123',
    };
    console.log(data);
    return false;
};