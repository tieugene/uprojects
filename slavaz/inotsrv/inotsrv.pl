#!/usr/bin/perl -w

use strict;
use warnings;
use Log::Log4perl;
use Data::Dumper::Simple;



BEGIN {
    my $dr = `pwd`; $dr =~ s/\n//m;
    push @INC, $dr."/../messer";
};

use szeng::fsnotify;

Log::Log4perl::init_and_watch('inotsrv.log.conf',10);

my $log = Log::Log4perl->get_logger("inotsrv::main");
$log->info("Запуск программы");

my $fsn = szeng::fsnotify->new;


$fsn->addHook("/srv/work/tmp");
$fsn->mainCycle();
$fsn->delHook("/srv/work/tmp");

