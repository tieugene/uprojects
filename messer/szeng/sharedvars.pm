package szeng::sharedvars;

use strict;
#use utf8;
use warnings;
use threads;
use threads::shared;
use Thread::Semaphore;
use Data::Dumper::Simple;

no strict 'refs';

use vars qw($VERSION %DATA_jabber %DATA_common %DATA_icq %DATA_email);

$VERSION = "0.0.1";

1;
