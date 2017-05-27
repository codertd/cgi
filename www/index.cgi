#!/usr/bin/perl
use strict;
use warnings;

use CGI;
use JSON;

use DBI;

use Data::Dumper;
use Try::Tiny;



main();

exit;





sub main {
    my $self = shift;

    my $q = CGI->new;
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
    render( $self, $data );

    return 1;
}




sub render {
    my $self = shift;
    my $data = shift;

    die "Unable to render results." unless (
        defined $data->{'content_type'} && 
        defined $data->{'content_body'} &&
        ref $data->{'cgi'} eq 'CGI'
    );
    #print STDERR Dumper($data);

    print $data->{'cgi'}->header($data->{'content_type'});
    print $data->{'content_body'}."\n";

    return 1;
}



sub getDBH {
    my $self = shift;

    my $db_info = {
        'db_host' => 'localhost',
        'db_name' => 'cgi',
        'db_user' => 'cgiuser',
        'db_pass' => 'myp455123!!!',
    };
    
    my $data_source = "dbi:mysql:database=".$db_info->{db_name}.':host='.$db_info->{db_host};

    # make sure we reconnect if the conn dies
    my $dbh = DBI->connect( $data_source, $db_info->{db_user}, $db_info->{db_pass},
       { mysql_auto_reconnect => 1 },
       );

    return $dbh;
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

    my $json = JSON->new;

    my $content_type = 'application/json';
    my $content_body = {
        'query' => $query_param,
        'test'  => 1
    };

    # encode as json
    $content_body = $json->encode($content_body);

    return ($content_type,$content_body);
}