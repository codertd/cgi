#!/usr/bin/perl
use strict;
use warnings;

#
# A simple perl cgi application the creates Appointments.
# Uses CGI to get information from HTTP post/get/ajax.
# Uses DBI to interface MySQL.
#


use CGI;

use Data::Dumper;
use Try::Tiny;

use lib '../lib';
use cgi_module;

# Start processing.
main();

exit;





sub main {
    #
    ## Main entry point for program.
    #
    # Contains the dispatch table, error catch mechanism, and render function.
    #

    my $q = CGI->new;
    my $cgi_module = new cgi_module();

    my ($content_type, $content_body);
    my $data_variables = {}; # for interpolation of data

    try {

        # Route "dispatch"
        if ($q->param('ajax_query')) { # if its an ajax call, render json.
            ($content_type,$content_body) = getAjaxData( $q );

        } elsif ($q->request_method eq 'POST') { # form post.

            # validate all input values
            my $validation_issues = $cgi_module->validateInputFormData($q);

            if (! scalar @$validation_issues ) {

                    $cgi_module->createAppointment($q);

            } else {

                foreach my $error (@$validation_issues) {
                    $data_variables->{errors_block}.=qq~<p class="errors_block">$error</p>~;
                }

            }

            # show everything.
            ($content_type,$content_body) = getIndexPage($data_variables);

        } else { # default landing page.
            ($content_type,$content_body) = getIndexPage($data_variables);

        }

    } catch {
        # Log errors, but render home page by default.
        print STDERR Dumper("An Error has occurred. $_");
        $data_variables->{errors_block}=qq~<p class="errors_block">I've encountered an issue: $_</p>~;
        ($content_type,$content_body) = getIndexPage($data_variables);
    };


    # Every render needs data.
    my $data = {
        'content_type' => $content_type,
        'content_body' => $content_body,
        'cgi'          => $q
    };

    print $cgi_module->render( $data );

    return 1;
}



sub getIndexPage {
    #
    ## The home page for the app.
    #

    # This is simple variable interpolation, so just strings not refs or complex objects.
    # I'd love to use TT here, but keeping it simple.
    my $data_variables = shift;

    $data_variables->{title} = 'CGI in Perl';

    my $content_type = 'text/html';
    my $content_body = qq~
<html>
<head>
    <title>[% title %]</title>
    <link href="/assets/css/bootstrap/bootstrap.min.css" rel="stylesheet" type="text/css" />
    <link href="/assets/css/bootstrap/bootstrap-theme.min.css" rel="stylesheet" type="text/css" />    
    <link href="/assets/css/bootstrap-datepicker/bootstrap-datepicker3.min.css" rel="stylesheet" type="text/css" />        
    <link href="/assets/css/app/cgi.css" rel="stylesheet" type="text/css" />    
</head>
<body>

<div class="jumbotron">
    <div class="container">
        <div class="row">
            <div class="col-md-8"><h2>Appointments</h2></div>
        </div>
    </div>
</div>

<!-- [% errors %] -->

<div class="container">
    <div class="row">
        <!-- content -->

        <!-- new appointment form -->
        <div class="col-md-8 align-middle">

            <form class="form-horizontal" id="appointment_form" name="appointment_form" method="POST">
            <fieldset>

                <div class="add_hide_fields">
                    <!-- New div toggle -->
                    <div class="form-group">
                        <div class="col-md-3">
                            <button id="new_show" name="new_show" class="btn btn-primary">NEW</button>
                        </div>
                    </div>
                </div>

                <div class="cancel_hide_fields" style="display:none;">

                <!-- New div toggle -->
                <div class="form-group">
                    <div class="col-md-3">
                        <button id="new_add" name="new_add" class="btn btn-primary">ADD</button>
                    </div>
                    <div class="col-md-5">
                        <button id="new_cancel" name="new_cancel" class="btn btn-danger">CANCEL</button>
                    </div>
                </div>

                <!-- datepicker -->
                <div class="form-group">
                    <label class="col-md-4 control-label" for="appointment_date">Date</label>  
                    <div class="input-group date col-md-4" data-provide="datepicker" data-date-format="yyyy-mm-dd" data-date-start-date="+1d">
                        <input required type="text" class="form-control input-md" name="appointment_date" id="appointment_date">
                        <div class="input-group-addon">
                            <span class="glyphicon glyphicon-th"></span>
                        </div>
                    </div>
                </div>

                <!-- Text input-->
                <div class="form-group">
                    <label class="col-md-4 control-label" for="appointment_time">Time</label>  
                    <div class="col-md-4">
                        <input required id="appointment_time" name="appointment_time" type="text" placeholder="Time" class="form-control input-md">
                    </div>
                </div>

                <!-- Text input-->
                <div class="form-group">
                    <label class="col-md-4 control-label" for="appointment_description">Description</label>  
                    <div class="col-md-4">
                        <input required id="appointment_description" name="appointment_description" type="text" placeholder="Description" class="form-control input-md">
                    </div>
                </div>
            </div>

            <div>
                <!-- Search Param and submit-->
                <div class="form-group">
                    <div class="col-md-4">
                        <input id="search_input" name="search_input" type="text" class="form-control input-md">
                    </div>
                    <div class="col-md-4">
                        <button id="search_button" name="search_button" class="btn btn-primary">SEARCH</button>
                    </div>
                </div>
            </div>

            </fieldset>
            </form>
        </div>

        <!-- existing appointments table -->
        <div class="col-md-8 align-middle">
        <table id="existing_appointments" class="appointment_table">
            <thead>
                <tr><th>Date</th><th>Time</th><th>Description</th></tr>
            </thead>
            <tbody>
            </tbody>
        </table>
        </div>

    </div>
</div>


<!-- Placed at the end of the document so the pages load faster -->
<script type="text/javascript" src="/assets/js/jquery/jquery.min.js"></script>
<script type="text/javascript" src="/assets/js/jquery-validate/jquery.validate.min.js"></script>
<script type="text/javascript" src="/assets/js/bootstrap/bootstrap.min.js"></script>
<script type="text/javascript" src="/assets/js/bootstrap-datepicker/bootstrap-datepicker.min.js"></script>
<script type="text/javascript" src="/assets/js/app/cgi.js"></script>
</body>
</html>
~;


    # Main interpolation.
    while( my( $key, $value ) = each %{$data_variables} ){
        $content_body =~ s/\[\% $key \%\]/$value/;
    }

    # special case variable name
    # css class found in cgi.css
    if (defined $data_variables->{errors_block}) {

        my $errors_content = qq~
<div class="container">
    <div class="row">
        ~.$data_variables->{errors_block}.qq~
    </div>
</div>
~;    
        $content_body =~ s/\<\!\-\- \[\% errors \%\] \-\-\>/$errors_content/;

    }

    return ($content_type,$content_body);
}


sub getAjaxData {
    #
    ## If the app does an ajax post and the ajax vars were found.
    #

    my $cgi = shift;

    my $cgi_module = new cgi_module();

    my $query_data = {};
    if ( $cgi->param('ajax_search') ) {
        $query_data->{'ajax_search'} = $cgi->param('ajax_search');
    };

    # Get matching/all appointments, and return encoded as json.
    my $content_type = 'application/json';    
    my $content_body = $cgi_module->getAppointmentsJSONFromDB($query_data);

    return ($content_type,$content_body);
}