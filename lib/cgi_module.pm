package cgi_module;

use strict;
use warnings;

# ABSTRACT: XXXX: cgi_module library 
# PODNAME: cgi_module.pm

use JSON;
use DBI;

use Try::Tiny;
use Data::Dumper qw(Dumper);


# This is "OOP", so bless some references.
sub new {
    my $class = shift;
    my $self = {};

    bless $self, $class;

    return $self;
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

    my $output=$data->{'cgi'}->header($data->{'content_type'});
    $output.=$data->{'content_body'}."\n";

    return $output;
}


sub getJSON {
    my $self = shift;

    my $json = JSON->new;
    print STDERR Dumper($json);

    return $json;
}


sub getDBH {
    my $self = shift;

    my $db_info = {
        'db_host' => 'localhost',
        'db_name' => 'cgi_db',
        'db_user' => 'cgiuser',
        'db_pass' => 'p43kd!d5z@ld9',
    };
    
    my $data_source = "dbi:mysql:database=".$db_info->{db_name}.':host='.$db_info->{db_host};

    # make sure we reconnect if the conn dies
    my $dbh = DBI->connect( $data_source, $db_info->{db_user}, $db_info->{db_pass},
       { mysql_auto_reconnect => 1 },
       );

    return $dbh;
}



sub getAppointmentsJSONFromDB {
    my $self = shift;

    print STDERR Dumper("self is: ".$self);

    my $dbh = $self->getDBH();

    my $sth =  $dbh->prepare("
        select 
            * 
        from 
            appointments
        order by appointment_time
    ");
    $sth->execute() or die "Cant execute SQL statement: $DBI::errstr\n";

    # json-ify
    my @content;
    while ( my $contentref = $sth->fetchrow_hashref() )
    {
        push( @content, { %{$contentref} } );
    }

    return $self->getJSON->encode(@content)
}


# return 1 at EOF
1;