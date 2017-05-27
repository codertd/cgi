#!/usr/bin/perl
use strict;
use warnings;

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
    ##
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

            #print STDERR Dumper($q->request_method);
            #print STDERR Dumper($q->param('test'));

            #my @names = $q->param;
            #print STDERR Dumper(@names);

            # validate all input values
            #validate_appointment_input($q);

            # create the new appointment
            #create_appointment($q);


            ($content_type,$content_body) = getIndexPage($data_variables);

        } else { # default landing page.
            ($content_type,$content_body) = getIndexPage($data_variables);

        }

    } catch {
        # Log errors, but render home page by default.
        print STDERR Dumper("An Error has occurred. $_");
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
    ##
    #

    # This is simple variable interpolation, so just strings not refs.
    # I'd love to use TT here, but it needs to run with minimal includes.
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

<div class="container">
    <div class="row">
    <!-- errors -->
    </div>
</div>


<div class="container">
    <div class="row">
        <!-- content -->

        <!-- new appointment form -->
        <div class="col-md-8 align-middle">


            <form class="form-horizontal">
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
                    <div class="input-group date col-md-4" data-provide="datepicker">
                        <input type="text" class="form-control input-md">
                        <div class="input-group-addon">
                            <span class="glyphicon glyphicon-th"></span>
                        </div>
                    </div>
                </div>

                <!-- Text input-->
                <div class="form-group">
                    <label class="col-md-4 control-label" for="Time">Time</label>  
                    <div class="col-md-4">
                        <input id="Time" name="Time" type="text" placeholder="Time" class="form-control input-md">
                    </div>
                </div>

                <!-- Text input-->
                <div class="form-group">
                    <label class="col-md-4 control-label" for="apppointment_description">Description</label>  
                    <div class="col-md-4">
                        <input id="apppointment_description" name="apppointment_description" type="text" placeholder="Description" class="form-control input-md">
                    <span class="help-block">help</span>  
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
        <table id="existing_appointments">
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


    while( my( $key, $value ) = each %{$data_variables} ){
        $content_body =~ s/\[\% $key \%\]/$value/;
    }


    return ($content_type,$content_body);
}


sub getAjaxData {
    #
    ##
    #

    my $cgi = shift;

    print STDERR Dumper($cgi);

    my $cgi_module = new cgi_module();

    my $content_type = 'application/json';
    my $content_body = {
        'query' => $cgi->param('ajax_query'),
        'test'  => 1
    };

    # Get all appointments, and return encoded as json.
    $content_body = $cgi_module->getAppointmentsJSONFromDB();
    print STDERR $content_body;

    return ($content_type,$content_body);
}