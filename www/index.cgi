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
    my $self = shift;


    my $q = CGI->new;
    my $cgi_module = new cgi_module();


    my ($content_type, $content_body);

    try {

        # Route "dispatch"
        if ($q->param('ajaxquery')) { # if its an ajax call, render json.
            ($content_type,$content_body) = getAjaxData( $q->param('ajaxquery') );

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

    print $cgi_module->render( $self, $data );

    return 1;
}



sub getIndexPage {
    my $self = shift;

    my $content_type = 'text/html';
    my $content_body = qq~
<html>
<head>
    <title>CGI Test</title>
</head>
<body>
It works!
</body>
</html>
~;

    return ($content_type,$content_body);
}


sub getAjaxData {
    my $self = shift;
    my $query_param = shift;

    my $cgi_module = new cgi_module();

    my $content_type = 'application/json';
    my $content_body = {
        'query' => $query_param,
        'test'  => 1
    };

    my $dbh = $self->getDBH();


    # encode as json
    $content_body = $cgi_module->getJSON->encode($content_body);

    return ($content_type,$content_body);
}