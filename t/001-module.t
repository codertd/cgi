#!/usr/bin/perl
use strict;
use warnings;

use Test::Most;
use Data::Dumper;


use lib '../lib';

use cgi_module;

my $tests = 0;

# Instantiate a cgi_module object.
$tests++;

my $cgi_module = new cgi_module;

isa_ok ($cgi_module, 'cgi_module');


# convenience methods present?
$tests++;
isa_ok ($cgi_module->getJSON, 'JSON');

$tests++;
isa_ok ($cgi_module->getDBH, 'DBI::db');



# can we retrieve appointments?
$tests++;
my $jsonstring = $cgi_module->getAppointmentsJSONFromDB();
my $appointments = $cgi_module->getJSON->decode($jsonstring);
#print Dumper( $appointments );

if (scalar @$appointments) {
    ok ($tests, "Able to retrieve and decode appointments json.");
}

# does appointment struct look normal?
$tests++;
my $appt = $appointments->[0];

if (defined $appt->{appointment_id} && $appt->{appointment_id} =~ /\d+/) {
    ok ($tests, "Appointments appear to have valid data in them.");
}


done_testing()