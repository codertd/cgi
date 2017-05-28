$(document).ready(function() {

    $('.datepicker').datepicker({
        format: 'mm/dd/yyyy',
        startDate: '+1d'
    });

    console.log("Appointment cgi ready!");
    getAppointments('');

    $("#new_show").click(function(event) {
        toggleHiddenFields('open');
    });

    $("#new_cancel").click(function(event) {
        toggleHiddenFields('closed');
    });

    $("#new_add").click(function(event) {
        submitNewAppointment();
    });

    $("#search_button").click(function(event) {
        submitSearch();
    });

});

function toggleHiddenFields(state) {
    // Prevent submit, we just want to toggle vis.
    event.preventDefault();

    if (state === 'open') {
        $(".cancel_hide_fields").show();
        $(".add_hide_fields").hide();
    } else {
        $(".cancel_hide_fields").hide();
        $(".add_hide_fields").show();
    }

    return false;
}


function submitNewAppointment() {
    // Prevent submit, we just want to toggle vis.
    event.preventDefault();

    console.log("Validating!");


    console.log("submitting!");

    return false;
}

function submitSearch() {
    // Prevent submit, we just want to toggle vis.
    event.preventDefault();

    console.log("Validating!");


    console.log("submitting!");

    return false;
}

function getAppointments(querystring) {
    console.log("in get appointments, sending ajax");

    var response;
    var url = '/index.cgi';


    // Using the core $.ajax() method
    $.ajax({

            // The URL for the request
            url: url,

            // The data to send (will be converted to a query string)
            data: {
                ajax_query: querystring
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