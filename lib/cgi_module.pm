package cgi_module;

use strict;
use warnings;

# ABSTRACT: XXXX: cgi_module library 
# PODNAME: cgi_module.pm

use JSON;
use DBI;

use DateTime;
use Date::Parse;

use Try::Tiny;
use Data::Dumper qw(Dumper);


# This is "OOP", so bless some references.
sub new {
    my $class = shift;
    my $self = {};

    bless $self, $class;

    return $self;
}


# A simple check to see that our Render has its valid parts, 
# and that an appropriate Header is set.
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


# Make sure any Input data from the form passes validation on the backend,
# and provide a  mechanism to pass an array of errors back so the user knows
# what they need to fix.
sub validateInputFormData {
    my $self = shift;
    my $cgi = shift;

    my @validation_errors;
   
    if ( $cgi->param('appointment_time') !~ /^\d{2}\:\d{2}[ap]m$/ ) {
        push (@validation_errors, "Sorry, you must supply a valid Appt Time. ".'('.$cgi->param('appointment_time').')');
    } else {
        my $appointment_time = str2time ( $cgi->param('appointment_date').' '.$cgi->param('appointment_time') );
        unless ( $appointment_time ) {
            push (@validation_errors, "Sorry, you must supply a valid Appt Time. ".'('.$cgi->param('appointment_time').')');
        }
    }

    unless ( $cgi->param('appointment_description') =~ /^[0-9A-Za-z\,\.\:\-\"\'\s]+$/ ) {
        push (@validation_errors, "Sorry, you must supply a valid Appt Description. ".'('.$cgi->param('appointment_description').')');
    }

    if ( $cgi->param('appointment_date') !~ /^\d{4}\-\d{2}\-\d{2}$/ ) {
        push (@validation_errors, "Sorry, you must supply a valid Appt Date (YYYY-MM-DD). ".'('.$cgi->param('appointment_date').')');
    } else {

        my $dt_now   = DateTime->now;   # Stores current date and time as datetime object
        my $dt_submitted = DateTime->new(
            year => substr($cgi->param('appointment_date'),0,4),
            month => substr($cgi->param('appointment_date'),5,2),
            day => substr($cgi->param('appointment_date'),8,2),
            hour => 0,
            minute =>0,
            second =>1,
            time_zone => 'America/Los_Angeles'
        );
        my $cmp = DateTime->compare( $dt_now, $dt_submitted ); 
        
        unless ( $cmp < 0) {
            push (@validation_errors, "Sorry, you must supply a valid Appt Date on or after today. ".'('.$cgi->param('appointment_date').')');
        }
    }

    return \@validation_errors;
}


# A simple JSON helper.
sub getJSON {
    my $self = shift;

    my $json = JSON->new;

    return $json;
}

# A way to get a handle for the database.
# this should be offloaded into a conf file, outside of the DocumentRoot.
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


# Lookup appointments in the database.
# If provided an optional search token, return only matching rows.
sub getAppointmentsJSONFromDB {
    my $self = shift;
    my $query_data = shift;

    my $dbh = $self->getDBH();
    my $sth;

    # We cant to an SQL select with a alias column in the where clause.
    # I.E. We see "December 24" in the Date display (formatted per spec),
    # but typing in Dec wouldnt produce results, as the appointment_time column
    # is datetime, and is mostly numeric.
    # so we need to do a little sql magic, in order to make the date/time values show up
    # as searchable data.
    if ( 
        defined $query_data->{ajax_search} && 
        $query_data->{ajax_search} =~ /^[0-9A-Za-z\,\.\:\-\s]+$/
    ) {
        my $search_string = '%'.$query_data->{ajax_search}.'%';
        $sth =  $dbh->prepare("
        select t1.custom_date,t2.* 
            from 
            (select 
                appointment_id,
                date_format(appointment_time,'%M %e %l:%i%p') as custom_date
                from 
                appointments
                order by appointment_time
            ) as t1 
            left join 
            (select 
                *,
                UNIX_TIMESTAMP(appointments.appointment_time) as appt_epoch
                from 
                appointments
            ) as t2 
                on t1.appointment_id = t2.appointment_id
            where
                t2.appointment_time like ? or
                t2.appointment_description like ? or
                t1.custom_date like ?
            order by appointment_time            
        ");
        $sth->execute( $search_string, $search_string, $search_string ) or die "Cant execute SQL statement: $DBI::errstr\n";
    } else {
        $sth =  $dbh->prepare("
            select 
                *,
                UNIX_TIMESTAMP(appointments.appointment_time) as appt_epoch
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
        # do some date conversion for output for specified format.
        my $dt = DateTime->from_epoch('epoch'=>$contentref->{'appt_epoch'});
        $contentref->{'translated_date'}  = $dt->month_name().' '.$dt->day;
        $contentref->{'translated_time'} = $dt->hour_12().':'.sprintf( "%02d",$dt->minute).$dt->am_or_pm;
        push( @content, { %{$contentref} } );
    }

    return $self->getJSON->encode(\@content)
}




# Create a new appointment.
sub createAppointment {
    my $self = shift;
    my $cgi = shift;

    die "Unable to create appointment." unless (
        ref $cgi eq 'CGI' &&
        $cgi->param('appointment_date') &&
        $cgi->param('appointment_time') &&
        $cgi->param('appointment_description')
    );

    my $dbh = $self->getDBH();

    my $appointment_time = str2time ( $cgi->param('appointment_date').' '.$cgi->param('appointment_time') );

    my $dt_appt = DateTime->from_epoch(epoch => $appointment_time,time_zone => 'America/Los_Angeles');
    my $appt_time = $dt_appt->ymd.' '.$dt_appt->hms;

    my $sth =  $dbh->prepare("
        insert into appointments values ('',?,?)
    ");        
    $sth->execute( $appt_time, $cgi->param('appointment_description') ) or die "Cant execute SQL statement: $DBI::errstr\n";

    return 1;
}


# return 1 at EOF
1;