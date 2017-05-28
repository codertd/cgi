#!/usr/bin/perl
use strict;
use warnings;

use Test::Most;
use Data::Dumper;

use LWP::UserAgent ();


my $test_vars = {
    'test_url' => 'http://localhost/index.cgi'
};

my $ua = LWP::UserAgent->new;


my $tests = 0;
my $response;

# grab the home page.
$tests++;
$response = $ua->get($test_vars->{test_url});

if ($response->is_success) {
     ok ($tests, 'HTTP load of home page successful');
 }
 else {
     fail('Unable to load home page.');
 }



# HTML should contain a title = .
$tests++;
$response = $ua->get($test_vars->{test_url});

my $body = $response->content();
if ($body =~ /<title>CGI in Perl<\/title>/) {
    ok ($tests, 'Found proper title tag.');
} else {
     fail('Unable to find proper title tag.');
}


done_testing()

