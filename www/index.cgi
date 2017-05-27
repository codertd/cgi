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

            ($content_type,$content_body) = getIndexPage();

        } else { # default landing page.
            ($content_type,$content_body) = getIndexPage();

        }

    } catch {
        # Log errors, but render home page by default.
        print STDERR Dumper("An Error has occurred. $_");
        ($content_type,$content_body) = getIndexPage();
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

    my $content_type = 'text/html';
    my $content_body = qq~
<html>
<head>
    <title>CGI Test</title>
    <link href="/assets/css/bootstrap/bootstrap.min.css" rel="stylesheet" type="text/css" />
    <link href="/assets/css/bootstrap/bootstrap-theme.min.css" rel="stylesheet" type="text/css" />    
    <link href="/assets/css/app/cgi.css" rel="stylesheet" type="text/css" />    
</head>
<body>

It works!

<!-- Placed at the end of the document so the pages load faster -->
<script src="/assets/js/jquery/jquery.min.js"></script>
<script src="/assets/js/jquery-validate/jquery.validate.min.js"></script>
<script src="/assets/js/bootstrap/bootstrap.min.js"></script>
<script src="/assets/js/app/cgi.js"></script>
</body>
</html>
~;

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