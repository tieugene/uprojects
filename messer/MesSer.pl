#!/usr/bin/perl


BEGIN {
#    push @INC, "/usr/local/share/szeng";
    push @INC, "./";
};

use strict;
use utf8;
use Log::Log4perl;
use szeng::manager;

my $log = Log::Log4perl->get_logger("MesSer::main");
$log->info("Останов программы");

