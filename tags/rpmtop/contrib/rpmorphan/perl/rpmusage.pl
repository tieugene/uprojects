#!/usr/bin/perl 
###############################################################################
#   rpmusage.pl
#
#    Copyright (C) 2006 by Eric Gerbier
#    Bug reports to: gerbier@users.sourceforge.net
#    $Id: rpmrestore.pl 43 2007-01-05 10:32:01Z gerbier $
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
###############################################################################
use strict;
use warnings;

use Getopt::Long;    # arg analysis
use Pod::Usage;      # man page

use File::stat;

use Data::Dumper;    # debug

# is global to be used by debug sub
my $opt_verbose;

# the code should use no "print" calls
# but instead debug, warning, info calls
###############################################################################
sub debug($) {
	my $text = shift(@_);
	print "debug $text\n" if ($opt_verbose);
	return;
}
###############################################################################
sub warning($) {
	my $text = shift(@_);
	warn "WARNING $text\n";
	return;
}
###############################################################################
sub info($) {
	my $text = shift(@_);
	print "$text\n";
	return;
}
###############################################################################
sub print_version($) {
	my $version = shift(@_);
	info("$0 version $version");
	return;
}
#########################################################
# used to check on option
sub is_set($$) {
	my $rh_opt = shift(@_);    # hash of program arguments
	my $key    = shift(@_);    # name of desired option

	my $r_value = $rh_opt->{$key};
	return $$r_value;
}
#########################################################
# apply a filter on package list according program options
sub filter($$) {
	my $rh_opt      = shift(@_);
	my $rh_list_pac = shift(@_);

	# we just want the list of keys
	my @list = keys %$rh_list_pac;

	if ( is_set( $rh_opt, 'all' ) ) {
		debug('all');
		return @list;
	}
	else {
		debug('guess');

		my @filtered_list;
		if ( is_set( $rh_opt, 'guess-perl' ) ) {
			debug('guess-perl');
			my @res = grep ( /^perl/, @list );
			push @filtered_list, @res;
		}
		if ( is_set( $rh_opt, 'guess-python' ) ) {
			my @res = grep ( /^python/, @list );
			push @filtered_list, @res;
		}
		if ( is_set( $rh_opt, 'guess-pike' ) ) {
			my @res = grep ( /^pike/, @list );
			push @filtered_list, @res;
		}
		if ( is_set( $rh_opt, 'guess-ruby' ) ) {
			my @res = grep ( /^ruby/, @list );
			push @filtered_list, @res;
		}
		if ( is_set( $rh_opt, 'guess-common' ) ) {
			my @res = grep ( /-common$/, @list );
			push @filtered_list, @res;
		}
		if ( is_set( $rh_opt, 'guess-data' ) ) {
			my @res = grep ( /-data$/, @list );
			push @filtered_list, @res;
		}
		if ( is_set( $rh_opt, 'guess-doc' ) ) {
			my @res = grep ( /-doc$/, @list );
			push @filtered_list, @res;
		}
		if ( is_set( $rh_opt, 'guess-dev' ) ) {
			my @res = grep ( /-devel$/, @list );
			push @filtered_list, @res;
		}
		if ( is_set( $rh_opt, 'guess-lib' ) ) {
			my @res = grep ( /^lib/, @list );
			push @filtered_list, @res;
		}
		if ( is_set( $rh_opt, 'guess-custom' ) ) {
			my $regex = ${ $rh_opt->{'guess-custom'} };
			my @res = grep ( /$regex/, @list );
			push @filtered_list, @res;
		}
		return @filtered_list;
	}
}
#########################################################
# difference between 2 date in unix format
# return in days
sub diff_date($$) {
	my $now  = shift(@_);    # current
	my $time = shift(@_);    #

	# convert from seconds to days
	return int( ( $now - $time ) / 86400 );
}
#########################################################
# return the date (unix format) of last access on a package
# (scan all inodes for atime) and the name of the file
sub get_last_access($) {
	my $ra_files = shift(@_);    # array of file names

	my $last_date = 0;
	my $last_file = '';
	foreach my $file (@$ra_files) {
		next unless ( -e $file );
		my $stat  = stat($file);
		my $atime = $stat->atime();

		if ( $atime > $last_date ) {
			$last_date = $atime;
			$last_file = $file;
		}
	}
	return ( $last_date, $last_file );
}
#########################################################
sub solve($$$$) {
	my $name        = shift(@_);    # package name
	my $rh_files    = shift(@_);    # general hash of package files
	my $access_time = shift(@_);    # option access-time
	my $now         = shift(@_);    # current time

	my ( $last_time, $file ) = get_last_access( $rh_files->{$name} );
	if ( !$file ) {
		debug("skip $name : no files");

		# can not give a time access : no files !
		return;
	}
	my $diff = diff_date( $now, $last_time );
	if ($access_time) {
		if ( $diff > $access_time ) {
			info("$name $diff on $file");
		}
		else {
			debug("skip package $name : too recent access ($diff days)");
		}
	}
	else {
		info("$name $diff on $file");
	}

	return;
}
#########################################################
sub quicksolve($$$) {
	my $name        = shift(@_);    # package name
	my $access_time = shift(@_);    # option access-time
	my $now         = shift(@_);    # current time

	debug("(quicksolve) : $name");

	my $cmd = 'rpm -ql ';

	my @files = `$cmd $name`;
	chomp(@files);

	# change structure to call generic call
	my %files;
	push @{ $files{$name} }, @files;

	solve( $name, \%files, $access_time, $now );
	return;
}
#########################################################
#
#	main
#
#########################################################
my $version = '0.3';

my $opt_help;
my $opt_man;
my $opt_version;
my $opt_fullalgo;
my $opt_use_cache;
my $opt_clear_cache;

my $opt_all;

my $opt_guess_perl;
my $opt_guess_python;
my $opt_guess_pike;
my $opt_guess_ruby;
my $opt_guess_common;
my $opt_guess_data;
my $opt_guess_doc;
my $opt_guess_dev;
my $opt_guess_lib;
my $opt_guess_all;
my $opt_guess_custom;

my @opt_package;
my @opt_exclude;
my $opt_install_time;
my $opt_access_time;

my %opt = (
	'help'         => \$opt_help,
	'man'          => \$opt_man,
	'verbose'      => \$opt_verbose,
	'version'      => \$opt_version,
	'fullalgo'     => \$opt_fullalgo,
	'all'          => \$opt_all,
	'guess-perl'   => \$opt_guess_perl,
	'guess-python' => \$opt_guess_python,
	'guess-pike'   => \$opt_guess_pike,
	'guess-ruby'   => \$opt_guess_ruby,
	'guess-common' => \$opt_guess_common,
	'guess-data'   => \$opt_guess_data,
	'guess-doc'    => \$opt_guess_doc,
	'guess-dev'    => \$opt_guess_dev,
	'guess-lib'    => \$opt_guess_lib,
	'guess-all'    => \$opt_guess_all,
	'guess-custom' => \$opt_guess_custom,
	'package'      => \@opt_package,
	'exclude'      => \@opt_exclude,
	'install-time' => \$opt_install_time,
	'access-time'  => \$opt_access_time,
	'use-cache'    => \$opt_use_cache,
	'clear-cache'  => \$opt_clear_cache,
);

Getopt::Long::Configure('no_ignore_case');
GetOptions(
	\%opt,            'help|?',         'man',         'verbose',
	'fullalgo!',      'version|V',      'all!',        'guess-perl!',
	'guess-python!',  'guess-pike!',    'guess-ruby!', 'guess-common!',
	'guess-data!',    'guess-doc!',     'guess-dev!',  'guess-lib!',
	'guess-all!',     'guess-custom=s', 'package=s',   'exclude=s',
	'install-time=i', 'access-time=i',  'use-cache!',  'clear-cache'
) or pod2usage(2);

if ($opt_help) {
	pod2usage(1);
}
elsif ($opt_man) {
	pod2usage( -verbose => 2 );
}
elsif ($opt_version) {
	print_version($version);
	exit;
}

if ($opt_guess_all) {
	$opt_guess_perl   = 1;
	$opt_guess_python = 1;
	$opt_guess_pike   = 1;
	$opt_guess_ruby   = 1;
	$opt_guess_common = 1;
	$opt_guess_data   = 1;
	$opt_guess_doc    = 1;
	$opt_guess_dev    = 1;
	$opt_guess_lib    = 1;
}

my $is_guess = $opt_guess_perl
  || $opt_guess_python
  || $opt_guess_pike
  || $opt_guess_ruby
  || $opt_guess_common
  || $opt_guess_data
  || $opt_guess_doc
  || $opt_guess_dev
  || $opt_guess_lib
  || $opt_guess_custom;

# test if a target is set
if ( ( !@opt_package ) && ( !$opt_all ) && ( !$is_guess ) ) {
	pod2usage('need a target : --package , --all, or --guess_? ');
}

my %excluded;
if (@opt_exclude) {

	#allow comma separated options on tags option
	# and build a hash for faster access
	my @liste_ex = split( /,/, join( ',', @opt_exclude ) );
	foreach my $ex (@liste_ex) {
		$excluded{$ex} = 1;
		debug("conf : exclude $ex");
	}
}

# install-time and access-time options are only available with the full algo
if ( ($opt_install_time) or ($opt_access_time) ) {
	debug("forced full algo");
	$opt_fullalgo = 1;
}

# if only few packages, the big algo is not necessary
# quicksolve algo will be faster
if (@opt_package) {

	#allow comma separated options on tags option
	@opt_package = split( /,/, join( ',', @opt_package ) );

	if ( !$opt_fullalgo ) {
		if ( $#opt_package <= 5 ) {

			# use  quicksolve
			my $now = time();
			foreach my $pac (@opt_package) {
				if ( exists $excluded{$pac} ) {
					debug("skip $pac : excluded");
					next;
				}
				quicksolve( $pac, $opt_access_time, $now );
			}
			exit;
		}
		else {
			debug("too much package for quicksolve algo");
		}
	}
	else {
		debug("full algo ");
	}
}

# hash structures to be filled with rpm query
my %files;
my %install_time;

# phase 1 : get data and build structures
# the main idea is to reduce the number of call to rpm in order to gain time
# the ';' separator is used to separate fields
# the ' ' separator is used to separate data in fields arrays
#my $cmd = 'rpm -qa --queryformat "%{NAME};%{INSTALLTIME};[%{FILENAMES} ]\n" ';

my $rpm_cmd =
'rpm -qa --queryformat "%{NAME};[%{REQUIRENAME} ];[%{PROVIDES} ];[%{FILENAMES} ];%{INSTALLTIME}\n" ';
my $cmd;

my $cache_file = '/tmp/rpmorphan.cache';
my $fh_cache;

if ($opt_clear_cache) {
	unlink $cache_file if ( -f $cache_file );
}

if ($opt_use_cache) {
	if ( -f $cache_file ) {

		# cache exists : use it
		$cmd = $cache_file;
		debug("use cache file $cache_file");
	}
	else {

		# use rpm command
		$cmd = "$rpm_cmd |";

		# and create cache file
		open( $fh_cache, '>', $cache_file )
		  or warning("can not create cache file $cache_file : $!");
		debug("create cache file $cache_file");
	}
}
else {
	$cmd = "$rpm_cmd |";

	unlink $cache_file if ( -f $cache_file );
}

# output may be long, so we use a pipe to avoid to store a big array
my $fh;
open( $fh, $cmd ) or die "can not open $cmd : $!\n";
debug('1 : analysis');
while (<$fh>) {

	# write cache
	print $fh_cache $_ if ($fh_cache);

	#my ( $name, $install_time, $files ) = split( /;/, $_ );
	my ( $name, undef, undef, $files, $install_time ) = split( /;/, $_ );

	# we do not use version in keys
	# so we only keep the last seen data for a package name
	if ( exists $files{$name} ) {
		debug("duplicate package $name");
	}

	# install time are necessary for install-time option
	$install_time{$name} = $install_time;

	my @files = split( ' ', $files );

	# list are necessary for access-time option
	push @{ $files{$name} }, @files;
}
close($fh);
close($fh_cache) if ($fh_cache);

# phase 2 : filter
# if a package is set, it will be first used, then it will use in order -all, then (guess*)
# (see filter sub)
debug('2 : filter');
my @liste_pac;
if (@opt_package) {
	@liste_pac = @opt_package;
}
else {
	@liste_pac = filter( \%opt, \%files );
}

# needed by access-time and install-time options
my $now = time();

# phase 3 : solve problem
debug('3 : solve');
foreach my $pac (@liste_pac) {
	if ( exists $excluded{$pac} ) {
		debug("skip $pac : excluded");
		next;
	}

	if ($opt_install_time) {
		my $diff = diff_date( $now, $install_time{$pac} );
		if ( $opt_install_time > 0 ) {
			if ( $diff < $opt_install_time ) {
				debug("skip $pac : too recent install ($diff days)");
				next;
			}
		}
		elsif ( $diff > -$opt_install_time ) {
			debug("skip $pac : too old install ($diff days)");
			next;
		}
	}
	solve( $pac, \%files, $opt_access_time, $now );
}

__END__

=head1 NAME

rpmusage - display rpm packages use frequency

=head1 DESCRIPTION

rpmusage will display for each package, the last date it was used (in days). It can be used
to find unused packages. It use the atime field of all package's files to do this job.
Note : as it scan all files inodes, the run may be long ...

=head1 SYNOPSIS

rpmusage.pl  [options] [targets]

options:

   -help                brief help message
   -man                 full documentation
   -V, --version        print version

   -verbose             verbose
   -fullalgo		force full algorythm
   -use-cache 		use cache to avoid rpm query
   -clear-cache	remove cache file

targets:

   -package pac		search last access on pac package
   -all			apply on all packages
   -guess-perl		apply on perl packages
   -guess-python	apply on python packages
   -guess-pike		apply on pike packages
   -guess-ruby		apply on ruby packages
   -guess-common	apply on common packages
   -guess-data		apply on data packages
   -guess-doc		apply on documentation packages
   -guess-dev		apply on development packages
   -guess-lib		apply on library packages
   -guess-all		apply all -guess-* options (perl, python ...)
   -guess-custom regex	apply the given regex to filter to package's names to filter the output

   -exclude pac		exclude pac from results
   -install-time +/-d	apply on packages which are installed before (after) d days
   -access-time d	apply on packages which are not been accessed for d days (slow)

=head1 OPTIONS

=over 8

=item B<-help>

Print a brief help message and exits.

=item B<-man>

Print the manual page and exits.

=item B<-version>

Print the program release and exit.

=item B<-verbose>

The program works and print debugging messages.

=item B<-package>

search if the given package(s) is(are) orphaned.
Can be used as '--package pac1 --package pac2'
or '--package "pac1, pac2"'

=item B<-all>

apply on all installed packages. The output should be interpreted.
For example lilo or grub are orphaned packages, but are necessary
to boot ...

the L<-install-time> and L<-access-time> options may be useful to filter the list

=item B<-guess-perl>

This option tries to find perl modules. It tries to match "^perl"

=item B<-guess-python>

This option tries to find python modules. It tries to match "^python"

=item B<-guess-pike>

This option tries to find pike modules. It tries to match "^pike"

=item B<-guess-ruby>

This option tries to find ruby modules. It tries to match "^ruby"

=item B<-guess-common>

This option tries to find common packages. It tries to match "-common$"

=item B<-guess-data>

This option tries to find data packages. It tries to match "-data$"

=item B<-guess-doc>

This option tries to find documentation packages. It tries to match "-doc$"

=item B<-guess-data>

This option tries to find data packages. It tries to match "-data$"

=item B<-guess-dev>

This option tries to find development packages. It tries to match "-devel$"

=item B<-guess-lib>

This option tries to find library packages. It tries to match "^lib"

=item B<-guess-all>

This is a short to tell : Try all of the above (perl, python ...)

=item B<-guess-custom>

this will allow you to specify your own filter. for exemple "^wh" 
will match whois, whatsnewfm ...

=item B<-exclude>

this option will specify the packages to exclude from the output.
Can be used as '--exclude pac1 --exclude pac2'
or '--exclude "pac1, pac2"'

=item B<-install-time>

install-time is a filter on the period from the package installation date to now (in days).
if set positive, it only allow packages installed before x days.
if set negative, it only allow packages installed since x days.

=item B<-access-time>

access-time is designed to filter packages which have not been used since x days.

be careful : this option will slow the program

=item B<-fullalgo>

for a small list of packages, rpmusage use a different quicker methode : rpm -e --test

this option can be used to force the use of the full algo

=item B<-use-cache>

the rpm query may be long (10 to 30 s). If you will run an rpmorphan tool
several time, this option will allow to gain a lot of time :
it save the rpm query on a file cache (first call), then
use this cache instead quering rpm (others calls).

=item B<-clear-cache>

to remove cache file. Can be used with -use-cache to write
a new cache.

=back

=head1 USE

rpmusage.pl --all | sork -k 2 -n

=head1 FILES

/tmp/rpmorphan.cache : cache file to store rpm query. The cache
file is common to all rpmorphan tools

=head1 NOTES

this program should be used as root superuser

=head1 SEE ALSO

=for man
\fIrpm\fR\|(1) for rpm call
.PP
\fIrpmorphan\fR\|(1) for rpmorphan use

=for html
<a href="rpmorphan.1.html">rpmorphan(1)</a> for rpmorphan use

=head1 COPYRIGHT

Copyright (C) 2007 by Eric Gerbier
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

=head1 AUTHORS

Eric Gerbier

you can report any bug or suggest to gerbier@users.sourceforge.net

=cut

