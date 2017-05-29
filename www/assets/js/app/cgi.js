$(document).ready(function() {

    $('.datepicker').datepicker({
        format: 'mm/dd/yyyy',
        startDate: '+1d'
    });

    $.validator.addMethod(
        "time_regex",
        function(value, element, regexp) {
            var check = false;
            return this.optional(element) || regexp.test(value);
        },
        "Please check the format of your time (HH:MMam)."
    );

    $("#appointment_form").validate({
        rules: {
            datepicker: "required",
            appointment_time: {
                required: true,
                time_regex: /^\d\d\:\d\d[ap]m$/,
                minlength: 7,
                maxlength: 7,
            },
            appointment_description: {
                required: true,
                minlength: 10
            },
        },
        messages: {
            datepicker: "Please select a date on or after today.",
            appointment_time: {
                required: "Please enter an Appointment Time in the form HH:MMam or HH::MMpm",
                minlength: "Your appointment time must be in the format HH:MMam or HH::MMpm."
            },
            appointment_description: {
                required: "Please provide an Appointment Description.",
                minlength: "Your description must be at least 10 characters long."
            }
        }
    });

    getAppointments();

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

    // disable enter so form doesnt submit accidentally,
    // but dynamically change the results based on content
    // of search box.
    // TODO: we cant search for the displayed date/time, which is confusing.
    $('form input').on('keypress', function(e) {
        return e.which !== 13;
    });
    $('#search_input').on('keypress', function(e) {
        var querystring = $("#search_input").val();
        getAppointments(querystring);
        return e.which !== 13;
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

    $("#appointment_form").submit();

    return false;
}

function submitSearch() {
    // Prevent submit, we just want to toggle vis.
    event.preventDefault();

    var querystring = $("#search_input").val();
    getAppointments(querystring);

    return false;
}

function getAppointments(querystring) {

    var response;

    var datafields = {
        ajax_query: 1,
    };
    if (typeof querystring != 'undefined') {
        datafields.ajax_search = querystring;
    };

    var ajaxpost = {
        // The URL for the request
        url: '/index.cgi',

        // The data to send (will be converted to a query string)
        data: datafields,
        // Whether this is a POST or GET request
        type: "POST",
        // The type of data we expect back
        dataType: "json",
    };

    // Using the core $.ajax() method
    $.ajax(ajaxpost)
        // Code to run if the request succeeds (is done);
        // The response is passed to the function
        .done(function(json) {

            $('#existing_appointments tbody tr').remove();
            $.each(json, function(i, item) {
                //var date_time = item.appointment_time.split(" ");
                //var markup = "<tr><td>" + date_time[0] + "</td><td>" + date_time[1] + "</td><td>" + item.appointment_description + "</td></tr>";
                var markup = "<tr><td>" + item.translated_date + "</td><td>" + item.translated_time + "</td><td>" + item.appointment_description + "</td></tr>";
                $("#existing_appointments tbody").append(markup);
            });
        })
        // Code to run if the request fails; the raw request and
        // status codes are passed to the function
        .fail(function(xhr, status, errorThrown) {
            console.log("Sorry, there was a problem!");
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