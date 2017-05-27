$(document).ready(function() {
    console.log("Appointment cgi ready!");
    getAppointments();
});


function getAppointments() {
    console.log("in get appointments, sending ajax");

    var response;
    var url = '/index.cgi';


    // Using the core $.ajax() method
    $.ajax({

            // The URL for the request
            url: url,

            // The data to send (will be converted to a query string)
            data: {
                ajax_query: 123
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType: "json",
        })
        // Code to run if the request succeeds (is done);
        // The response is passed to the function
        .done(function(json) {

            $('#existing_appointments tbody tr').remove();
            $.each(json, function(i, item) {
                console.log(item);
                var date_time = item.appointment_time.split(" ");
                var markup = "<tr><td>" + date_time[0] + "</td><td>" + date_time[1] + "</td><td>" + item.appointment_description + "</td></tr>";
                $("#existing_appointments tbody").append(markup);
            });
        })
        // Code to run if the request fails; the raw request and
        // status codes are passed to the function
        .fail(function(xhr, status, errorThrown) {
            alert("Sorry, there was a problem!");
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        })
        // Code to run regardless of success or failure;
        .always(function(xhr, status) {
            console.log("The request is complete!");
        });


    return true;
};