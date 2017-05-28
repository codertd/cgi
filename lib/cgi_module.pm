package cgi_module;

use strict;
use warnings;

# ABSTRACT: XXXX: cgi_module library 
# PODNAME: cgi_module.pm

use JSON;
use DBI;

use DateTime;

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

    my $output=$data->{'cgi'}->header($data->{'content_type'});
    $output.=$data->{'content_body'}."\n";

    return $output;
}



sub validateInputFormData {
    my $self = shift;
    my $cgi = shift;

    #my $datestring = localtime;
    #print STDERR Dumper($datestring);

    my @validation_errors;
   
    unless ( $cgi->param('appointment_time') =~ /^\d{2}\:\d{2}[ap]m$/ ) {
        push (@validation_errors, "Sorry, you must supply a valid Appt Time.");
    }

    unless ( $cgi->param('appointment_description') =~ /^[0-9A-Za-z\,\.\:\-\"\']+$/ ) {
        push (@validation_errors, "Sorry, you must supply a valid Appt Description.");
    }

    if ( $cgi->param('appointment_date') !~ /^\d{4}\-\d{2}\-\d{2}$/ ) {
        push (@validation_errors, "Sorry, you must supply a valid Appt Date (YYYY-MM-DD).");
    } else {

        my $dt_now   = DateTime->now;   # Stores current date and time as datetime object
        my $dt_submitted = DateTime->new(
            year => substr($cgi->param('appointment_date'),0,4),
            month => substr($cgi->param('appointment_date'),6,2),
            day => substr($cgi->param('appointment_date'),9,2),
            hour => 0,
            minute =>0,
            second =>1,
            time_zone => 'America/Los_Angeles'
        );
        my $cmp = DateTime->compare( $dt_submitted, $dt_now ); 
        
        unless ( $cmp < 0) {
            push (@validation_errors, "Sorry, you must supply a valid Appt Date on or after today.");
        }
    }

    return \@validation_errors;
}


sub getJSON {
    my $self = shift;

    my $json = JSON->new;

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
    my $query_data = shift;

    my $dbh = $self->getDBH();
    my $sth;

    if ( 
        defined $query_data->{ajax_search} && 
        $query_data->{ajax_search} =~ /^[0-9A-Za-z\,\.\:\-]+$/
    ) {
        my $search_string = '%'.$query_data->{ajax_search}.'%';
        $sth =  $dbh->prepare("
            select 
                * 
            from 
                appointments
            where 
                appointment_time like ? or
                appointment_description like ?
            order by appointment_time
        ");
        $sth->execute( $search_string, $search_string ) or die "Cant execute SQL statement: $DBI::errstr\n";
    } else {
        $sth =  $dbh->prepare("
            select 
                * 
            from 
                appointments
            order by appointment_time
        ");        
        $sth->execute() or die "Cant execute SQL statement: $DBI::errstr\n";
    };


    # json-ify
    my @content;
    while ( my $contentref = $sth->fetchrow_hashref() )
    {
        push( @content, { %{$contentref} } );
    }

    return $self->getJSON->encode(\@content)
}





sub createAppointment {
    my $self = shift;
    my $query_data = shift;

    my $dbh = $self->getDBH();
    my $sth;

    $sth =  $dbh->prepare("
        insert into appointments values ('',?,?)
    ");        
    $sth->execute( $query_data->{appointment_time}, $query_data->{appointment_description} ) or die "Cant execute SQL statement: $DBI::errstr\n";

    return 1;
}


# return 1 at EOF
1;