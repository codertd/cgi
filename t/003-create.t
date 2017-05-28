#!/usr/bin/perl
use strict;
use warnings;

use Test::Most;
use Data::Dumper;


use lib '../lib';

use cgi_module;
use CGI;

my $tests = 0;

# Instantiate a cgi_module object.
$tests++;

my $cgi_module = new cgi_module;


# can we create an  appointment?
my $nowstring = localtime();


$tests++;

my $cgi = new CGI;
$cgi->param(-name=>'appointment_time',          -value=>'01:01am');
$cgi->param(-name=>'appointment_date',          -value=>'2018-12-25');
$cgi->param(-name=>'appointment_description',   -value=>$nowstring);

$cgi_module->createAppointment($cgi);

# can we find the appointment we just created?
$tests++;
my $jsonstring = $cgi_module->getAppointmentsJSONFromDB({'ajax_search' => $nowstring});
my $appointments = $cgi_module->getJSON->decode($jsonstring);
print Dumper( $appointments );

if (scalar @$appointments) {
    ok ($tests, "Was able to find the appointment we just made by searching for it.");
}


done_testing()