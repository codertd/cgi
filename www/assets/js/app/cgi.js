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

    $.ajax({
        async: true,
        url: url,
        data: data,
        type: 'POST',
        //contentType: "application/json; charset=utf-8",
        timeout: 4000,
        success: function(data) {
            console.log(data);

            //$.each(data, function(i, item) {
            //    var markup = "<tr><td>" + item.appointment_time + "</td><td>" + item.appointment_description + "</td></tr>";
            //    $("#existing_appointments tbody").append(markup);
            //});

        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            console.log(XMLHttpRequest);
            response = XMLHttpRequest.responseJSON.error.Message;
            console.log(response);
        }
    });


    return true;
};