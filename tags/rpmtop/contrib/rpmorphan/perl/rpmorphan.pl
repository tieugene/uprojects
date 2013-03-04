#!/usr/bin/perl 
###############################################################################
#   rpmorphan.pl
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

use File::stat;	    # get_last_access

use Data::Dumper;    # debug

# widget list of packages for gui
my $W_list;

# the code should use no "print" calls
# but instead debug, warning, info calls
###############################################################################
# used to print debuging messages in verbose mode
sub debug($) {
	my $text = shift(@_);
	print "debug $text\n" if ( is_verbose() );
	return;
}
###############################################################################
# used to print warning messages
sub warning($) {
	my $text = shift(@_);
	warn "WARNING $text\n";
	return;
}
###############################################################################
# used to print normal messages
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
{

	# for gui, we will have to call this sub after each delete
	# as it is very expensive (file access)
	# we will use a cache
	#
	my %access_time;

	# this is a filter : we will test if any file was accessed since $access_time days
	# be careful : this code can be very slow
	sub access_time_filter($$$$) {
		my $name        = shift(@_);    # package name
		my $rh_files    = shift(@_);    # general hash of package files
		my $access_time = shift(@_);    # option access-time
		my $now         = shift(@_);    # current time

		my $ret;
		if ($access_time) {

			my $age;
			# test for cache
			if ( exists $access_time{$name} ) {

				# get from cache
				$age = $access_time{$name};
			}
			else {

				# not in cache : get it from file system
				my ( $last_time, $file ) =
				  get_last_access( $rh_files->{$name} );
				$age = diff_date( $now, $last_time );
				debug("last access on $file is $age days old");
				$access_time{$name} = $age;
			}

			if ( $age > $access_time ) {
				debug("keep package $name : old access ($age days)");
				$ret = 1;
			}
			else {
				debug("skip package $name : too recent access ($age days)");
				$ret = 0;
			}
		}
		else {

			# no filter
			$ret = 1;
		}
		return $ret;
	}
}
#########################################################
# return true is $name is an orphan
sub solve($$$$) {
	my $name        = shift(@_);    # package name
	my $rh_provides = shift(@_);    # general provide hash
	my $rh_depends  = shift(@_);    # general dependencies hash
	my $rh_virtual  = shift(@_);    # virtual package hash

	debug("(solve) : $name");

	my $flag_orphan = 1;
	foreach my $prov ( @{ $rh_provides->{$name} } ) {

	  # dependencies can be to "virtual" object : smtpdaemon, webclient
	  # for example, try "rpm -q --whatprovides webclient"
	  # you will get many packages : elinks,kdebase-common,mozilla,wget,lynx ...

		if ( exists $rh_virtual->{$prov} ) {
			debug("skip virtual provide $prov");
			next;
		}

		if ( exists $rh_depends->{$prov} ) {

			# some packages depends from $prov ...
			$flag_orphan = 0;

			my @depends = @{ $rh_depends->{$prov} };
			debug("$name is required by @depends");
			last;
		}
	}
	return $flag_orphan;
}
#########################################################
# use the slow "rpm -e --test" command
# but is quicker if used only on 1 package (no analysis)
# return true if is an orphan
sub quicksolve($) {
	my $name = shift(@_);    # package name

	debug("(quicksolve) : $name");

	my $cmd = 'rpm -e --test ';

	my @depends = `$cmd $name 2>&1`;
	my $ret;
	if ( $#depends == -1 ) {

		#info($name);
		$ret = 1;
	}
	else {
		$ret = 0;
		debug("$name is required by @depends");
	}
	return $ret;
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

	my $last_date = 0; # means a very old date for linux : 1970
	my $last_file = q{};
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
# 		keep
#
# a way to keep a list of exclusions
#########################################################
my $file_keep = '/var/lib/rpmorphan/keep';

# list content of keep file
sub list_keep($) {
	my $display = shift(@_);    # display or not ?

	my @list;
	my $fh;
	if ( open( $fh, '<', $file_keep ) ) {
		@list = <$fh>;
		chomp(@list);
		close($fh);

		info("@list") if ($display);
	}
	else {
		warning("can not read keep file $file_keep : $!");
	}
	return @list;
}
#########################################################
# empty keep file
sub zero_keep() {
	my $fh;
	if ( open( $fh, '>', $file_keep ) ) {
		close($fh);
	}
	else {
		warning("can not empty keep file $file_keep : $!");
	}
	return;
}
#########################################################
# add packages names to keep file
sub add_keep($$) {
	my $ra_list     = shift(@_);
	my $flag_append = shift(@_);    # true if append, else rewrite

	my @new_list;
	my $mode;
	if ($flag_append) {
		$mode = '>>';

		# read current list
		my @old_list = list_keep(0);

		# check for duplicates and merge
	  LOOP: foreach my $add (@$ra_list) {
			foreach my $elem (@old_list) {
				if ( $elem eq $add ) {
					debug("skip add duplicate $add");
					next LOOP;
				}
			}
			push( @new_list, $add );
			debug("add keep $add");
		}
	}
	else {
		$mode     = '>';
		@new_list = @$ra_list;
	}

	my $fh;
	if ( open( $fh, $mode, $file_keep ) ) {
		foreach my $elem (@new_list) {
			print $fh $elem . "\n";
		}
		close($fh);
	}
	else {
		warning("can not write to keep file $file_keep : $!");
	}
	return;
}
#########################################################
# remove packages names from keep file
sub del_keep($) {
	my $ra_list = shift(@_);

	# read current list
	my @old_list = list_keep(0);

	# remove entries
	my @new_list;
  LOOP: foreach my $elem (@old_list) {
		foreach my $del (@$ra_list) {
			if ( $elem eq $del ) {
				debug("del keep $del");
				next LOOP;
			}
		}
		push( @new_list, $elem );
	}

	# rewrite keep file
	add_keep( \@new_list, 0 );
	return;
}
################################################################
#                       gui
################################################################
{

	# just to avoid a global var
	my @log;

	sub write_log {
		push @log, @_;
		return;
	}

	sub get_log() {
		return @log;
	}
}
################################################################
# select all
sub do_select() {
	$W_list->selectionSet( 0, 'end' );
	return;
}
################################################################
# unselect all
sub do_unselect() {
	$W_list->selectionClear( 0, 'end' );
	return;
}
#########################################################
# change cursor to watch
sub cursor2watch() {
	my $cursor = $W_list->cget('-cursor');
	$W_list->configure( -cursor => 'watch' );
	$W_list->update();

	return $cursor;
}
#########################################################
# restore cursor
sub cursor2normal($) {
	my $cursor = shift(@_);

	# restore pointer
	$W_list->configure( -cursor => $cursor );
	$W_list->update();
	return;
}
#########################################################
# remove packages
sub do_remove() {

	# change pointer
	my $cursor = cursor2watch();

	my @sel = $W_list->curselection();

	# get full list
	my @liste = $W_list->get( 0, 'end' );

	foreach my $s (@sel) {
		my $pac = $liste[$s];
		my $cmd = "rpm -e $pac 2>&1";

		my @output = `$cmd`;
		print "@output\n";
		write_log("$pac deleted");
	}

	# build the new list
	my @new_list;
  LOOP: foreach my $l (@liste) {
		foreach my $s (@sel) {
			my $pac = $liste[$s];
			next LOOP if ( $pac eq $l );
		}
		push @new_list, $l;
	}
	@liste = @new_list;

	# effacer
	$W_list->delete( 0, 'end' );

	# re-afficher
	$W_list->insert( 'end', @liste );

	# restore pointer
	cursor2normal($cursor);
	return;
}
#########################################################
# general texte display in a new text window
# is used by all help buttons
sub display_message($$@) {
	my $main    = shift(@_);    # parent widget
	my $title   = shift(@_);    # window title
	my @baratin = @_;           # text to display

	my $top = $main->Toplevel( -title => $title );
	$top->Button( -text => 'quit', -command => [ $top => 'destroy' ] )->pack();
	my $text = $top->Scrolled(
		'ROText',
		-scrollbars => 'e',
		-height     => 25,
		-width      => 128,
		-wrap       => 'word'
	)->pack( -side => 'left', -expand => 1, -fill => 'both' );
	$top->bind( '<Key-q>', [ $top => 'destroy' ] );

	$text->insert( 'end', @baratin );
	$text->see('1.0');
	return;
}

################################################################
sub do_help($) {
	my $main = shift;

	my $baratin = 'rpmorphan will help you to clean unused package

the window will show you orphaned packages (without any rpm dependencies to them)

buttons are :

remove : remove selected package(s) 
info : show informations about current package
select all : select all packages
unselect all : unselect all packages
help   : this help screen
quit   : exit rpmorphan

selection :
- left click to select/unselect a package
- crtl + left click : to select/unselect another package
- shift + left click : to select/unselect a range

hotkeys :
x : remove
i : information
s : select all
u : unselect all
h : help
q : quit
	
note : dependencies are not (yet) updated after each package delete
you have to exit and restart program to get new orphans

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
	';

	display_message( $main, 'help', $baratin );
	return;
}
################################################################
sub do_log($) {
	my $main = shift;

	my @l = get_log();
	my $l = join( "\n", @l );

	display_message( $main, 'help', $l );
	return;
}
#########################################################
sub do_summary() {

	# on doit recuperer la position courante
	my $elem = $W_list->get('active');

	my @c = split( ' ', $elem );
	my $c = $c[0];

	#print "c=$c\n";
	my $cmd     = "rpm -q --queryformat '%{SUMMARY}' $c";
	my $summary = `$cmd`;
	chomp($summary);
	print "summary = $summary\n";

	return;
}
################################################################
sub do_info($) {
	my $main = shift;

	# get current position
	my $elem = $W_list->get('active');

	my @c = split( ' ', $elem );
	my $c = $c[0];

	#print "c=$c\n";
	my $cmd = "rpm -qil $c";
	my @res = `$cmd`;
	chomp(@res);

	my $message = join( "\n", @res );

	display_message( $main, 'info', $message );
	return;
}
#########################################################
sub build_gui($) {
	my $version = shift(@_);

	my $main      = MainWindow->new( -title => "rpmorphan $version" );
	my $w_balloon = $main->Balloon();
	my $side      = 'top';

	# frame for the list
	my $frame2 = $main->Frame();
	$frame2->pack( -side => $side, -expand => 1, -fill => 'both' );

	$W_list = $frame2->Scrolled(
		'Listbox',
		-scrollbars => 'e',
		-selectmode => 'extended'
	)->pack( -side => $side, -expand => 1, -fill => 'both' );

	$w_balloon->attach( $W_list, -msg => 'list window' );

	# frame for buttons
	my $frame3 = $main->Frame();
	$frame3->pack( -side => 'bottom', -expand => 0, -fill => 'none' );

	my $remove_button =
	  $frame3->Button( -text => 'remove', -command => [ \&do_remove ] );
	$remove_button->pack( -side => 'left' );
	$w_balloon->attach( $remove_button, -msg => 'remove selected packages' );
	$main->bind( '<Key-x>', [ \&do_remove ] );

	my $info_button =
	  $frame3->Button( -text => 'info', -command => [ \&do_info, $main ] );
	$info_button->pack( -side => 'left' );
	$w_balloon->attach( $info_button, -msg => 'get info on current package' );

	# todo idea : write the summary of package in ROtext when cursor is on
	$main->bind( '<Key-i>', [ \&do_info, $main ] );

	# button 1 : summary
	#$W_list->bind( '<Button-1>', [ \&do_summary ] );
	# button 3 : full info
	#$W_list->bind( '<Button-3>', [ \&do_info, $main ] );

	my $select_button =
	  $frame3->Button( -text => 'select all', -command => [ \&do_select ] );
	$select_button->pack( -side => 'left' );
	$w_balloon->attach( $select_button, -msg => 'select all packages' );
	$main->bind( '<Key-s>', [ \&do_select ] );

	my $unselect_button =
	  $frame3->Button( -text => 'unselect all', -command => [ \&do_unselect ] );
	$unselect_button->pack( -side => 'left' );
	$w_balloon->attach( $unselect_button, -msg => 'unselect all packages' );
	$main->bind( '<Key-u>', [ \&do_unselect ] );

	my $help_button =
	  $frame3->Button( -text => 'help', -command => [ \&do_help, $main ] );
	$help_button->pack( -side => 'left' );
	$w_balloon->attach( $help_button, -msg => 'help on rpmorphan interface' );
	$main->bind( '<Key-h>', [ \&do_help, $main ] );

	my $log_button =
	  $frame3->Button( -text => 'log', -command => [ \&do_log, $main ] );
	$log_button->pack( -side => 'left' );
	$w_balloon->attach( $log_button, -msg => 'display log' );
	$main->bind( '<Key-l>', [ \&do_log, $main ] );

	# todo
	#my $resolve_button =
	#$frame3->Button( -text => 'resolve', -command => [ \&do_help, $main ] );
	#$resolve_button->pack( -side => 'left' );
	#$w_balloon->attach( $resolve_button, -msg => 'resolve dependencies' );
	#$main->bind( '<Key-r>', [\&do_help, $main] );

	my $exit_button =
	  $frame3->Button( -text => 'Quit', -command => [ $main => 'destroy' ] );
	$exit_button->pack( -side => 'left' );
	$w_balloon->attach( $exit_button, -msg => 'quit the software' );
	$main->bind( '<Key-q>', [ $main => 'destroy' ] );

	return;
}
#########################################################
sub test_gui() {

	# check if perl-tk is available
	eval {
		require Tk;
		import Tk;
		require Tk::Balloon;
		import Tk::Balloon;
		require Tk::Frame;
		import Tk::Frame;
		require Tk::Listbox;
		import Tk::Listbox;
		require Tk::ROText;
		import Tk::ROText;
	};
	if ($@) {
		warning("can not find Tk perl module");
		return 0;
	}
	else {
		debug('Tk ok');
		return 1;
	}
}
#########################################################
# 
#########################################################
sub read_rpm_data($$$$$$) {
	my $rh_opt          = shift(@_);    # hash of program arguments
	my $rh_provides     = shift(@_);
	my $rh_install_time = shift(@_);
	my $rh_files        = shift(@_);
	my $rh_depends      = shift(@_);
	my $rh_virtual      = shift(@_);

	# the main idea is to reduce the number of call to rpm in order to gain time
	# the ';' separator is used to separate fields
	# the ' ' separator is used to separate data in fields arrays
	my $rpm_cmd =
'rpm -qa --queryformat "%{NAME};[%{REQUIRENAME} ];[%{PROVIDES} ];[%{FILENAMES} ];%{INSTALLTIME}\n" ';
	my $cmd;

	my $cache_file = '/tmp/rpmorphan.cache';
	my $fh_cache;

	if ( is_set( $rh_opt, 'clear-cache' ) ) {
		unlink $cache_file if ( -f $cache_file );
	}

	if ( is_set( $rh_opt, 'use-cache' ) ) {
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
	my %objects;
	my $fh;
	open( $fh, $cmd ) or die "can not open $cmd : $!\n";
	debug('1 : analysis');
	while (<$fh>) {

		# write cache
		print $fh_cache $_ if ($fh_cache);

		my ( $name, $req, $prov, $files, $install_time ) = split( /;/, $_ );

		# we do not use version in keys
		# so we only keep the last seen data for a package name
		if ( exists $rh_provides->{$name} ) {
			debug("duplicate package $name");
		}

		# install time are necessary for install-time option
		$rh_install_time->{$name} = $install_time;

		my @prov  = split( ' ', $prov );
		my @req   = split( ' ', $req );
		my @files = split( ' ', $files );

		# try to detect virtuals
		# virtuals can be provided by several packages
		# see comments in solve sub
		foreach my $p (@prov) {

			# do not add files
			next if ( $p =~ m!^/! );

			#  some bad package may provide more than on time the same object
			if (   ( exists $objects{$p} )
				&& ( $objects{$p} ne $name ) )
			{

				# we do not use who provide this virtual for now
				# if it necessary use
				# push @{virtual{$p}}, $name, $objects{$p};
				$rh_virtual->{$p} = 1;
			}
			else {

				# keep memory of seen "provided"
				$objects{$p} = $name;
			}
		}

		# $name package provide @prov
		# file are also included in "provide"
		push @{ $rh_provides->{$name} }, @prov, @files;

		# list are necessary for access-time option
		push @{ $rh_files->{$name} }, @files;

		# build a hash for dependencies
		foreach (@req) {

			# we have to suppress auto-depends (ex : ark package)
			my $flag_auto = 0;
			foreach my $p (@prov) {
				if ( $_ eq $p ) {
					$flag_auto = 1;

					#debug("skip auto-depency on $name");
					last;
				}
			}

			# $name depends from $_
			push( @{ $rh_depends->{$_} }, $name ) unless $flag_auto;
		}

	}
	close($fh);
	close($fh_cache) if ($fh_cache);
	return;
}
#########################################################
# resolv dependencies for all packages in ra_liste_pac
sub search_orphans($$$$$$$$) {
	my $rh_provides     = shift(@_);
	my $rh_files        = shift(@_);
	my $rh_depends      = shift(@_);
	my $rh_virtual      = shift(@_);
	my $now             = shift(@_);
	my $ra_liste_pac    = shift(@_);
	my $opt_gui         = shift(@_);
	my $opt_access_time = shift(@_);

	debug('4 : solve');
	foreach my $pac (@$ra_liste_pac) {
		if (    solve( $pac, $rh_provides, $rh_depends, $rh_virtual, )
			and access_time_filter( $pac, $rh_files, $opt_access_time, $now ) )
		{
			if ($opt_gui) {
				$W_list->insert( 'end', $pac );
			}
			else {
				info($pac);
			}
		}
	}
	return;
}
#########################################################
{
	# to avoid a global variable
	my $verbose;

	sub is_verbose() {
		return $verbose;
	}
	sub set_verbose($) {
		$verbose = $_[0];
	}
}

#########################################################
#
#	main
#
#########################################################
my $version = '0.8';

my $opt_help;
my $opt_man;
my $opt_verbose;
my $opt_version;
my $opt_fullalgo;
my $opt_use_cache;
my $opt_clear_cache;
my $opt_gui;

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

my $opt_list_keep;
my $opt_zero_keep;
my @opt_add_keep;
my @opt_del_keep;

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
	'add-keep'     => \@opt_add_keep,
	'del-keep'     => \@opt_del_keep,
	'list-keep'    => \$opt_list_keep,
	'zero-keep'    => \$opt_zero_keep,
	'use-cache'    => \$opt_use_cache,
	'clear-cache'  => \$opt_clear_cache,
	'gui'          => \$opt_gui,
);

Getopt::Long::Configure('no_ignore_case');
GetOptions(
	\%opt,            'help|?',         'man',         'verbose',
	'fullalgo!',      'version|V',      'all!',        'guess-perl!',
	'guess-python!',  'guess-pike!',    'guess-ruby!', 'guess-common!',
	'guess-data!',    'guess-doc!',     'guess-dev!',  'guess-lib!',
	'guess-all!',     'guess-custom=s', 'package=s',   'exclude=s',
	'install-time=i', 'access-time=i',  'list-keep',   'zero-keep',
	'add-keep=s',     'del-keep=s',     'use-cache!',  'clear-cache',
	'gui',
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

set_verbose($opt_verbose);

# keep file management
if ($opt_list_keep) {
	list_keep(1);
	exit;
}
if ($opt_zero_keep) {
	zero_keep();
	exit;
}
if (@opt_add_keep) {
	my @liste_add = split( /,/, join( ',', @opt_add_keep ) );
	add_keep( \@liste_add, 1 );
	exit;
}
if (@opt_del_keep) {
	my @liste_del = split( /,/, join( ',', @opt_del_keep ) );
	del_keep( \@liste_del );
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

# excluded files
my %excluded;

# first : permanent "keep" file
my @list_keep = list_keep(0);
foreach my $ex (@list_keep) {
	$excluded{$ex} = 1;
	debug("conf : permanent exclude $ex");
}

# command options
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
			foreach my $pac (@opt_package) {
				if ( exists $excluded{$pac} ) {
					debug("skip $pac : excluded");
					next;
				}
				info($pac) if ( quicksolve($pac) );
			}
			exit;
		}
		else {
			debug("too much package for quicksolve algo");
		}
	}
	else {
		debug("full algo required");
	}
}

if ($opt_gui) {
	if ( $opt_gui = test_gui() ) {
		build_gui($version);
	}
}

# hash structures to be filled with rpm query
my %provides;
my %depends;
my %install_time;
my %files;
my %virtual;

# phase 1 : get data and build structures
read_rpm_data( \%opt, \%provides, \%install_time, \%files, \%depends,
	\%virtual );

# phase 2 : guess filter
# if a package is set, it will be first used, then it will use in order -all, then (guess*)
# (see filter sub)
debug('2 : guess filter');
my @liste_pac;
if (@opt_package) {
	@liste_pac = @opt_package;
}
else {
	@liste_pac = filter( \%opt, \%provides );
}

# needed by access-time and install-time options
my $now = time();

# phase 3 : excluded and install-time filter
debug('3 : excluded and install-time');
my @liste_pac2;
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
	push @liste_pac2, $pac;
}

# note : access-time filter is a very slow method
# so we apply this filter after dependencies research
#  see below access_time_filter call

# we want the result sorted in alphabetic order
@liste_pac = sort @liste_pac2;

# phase 4 : solve dependencies
search_orphans( \%provides, \%files, \%depends, \%virtual, $now, \@liste_pac,
	$opt_gui, $opt_access_time );

#debug('4 : solve');
#foreach my $pac (@liste_pac) {
#	if (
#		solve(
#			$pac,    \%provides,       \%depends, \%virtual,
#		) and access_time_filter($pac, \%files, $opt_access_time, $now )
#	  ){
#		  if ($opt_gui) {
#			$W_list->insert( 'end', $pac);
#		  } else {
#			info($pac);
#		  }
#	  }
#}

MainLoop() if ($opt_gui);

__END__

=head1 NAME

rpmorphan - find orphaned packages

=head1 DESCRIPTION

rpmorphan finds "orphaned" packages on your system. It determines which packages have no other 
packages depending on their installation, and shows you a list of these packages. 
It is clone of deborphan debian software for rpm packages.

It will try to help you to remove unused packages, for exemple :

- after a distribution upgrade

- when you want to suppress packages after some tests

=head1 SYNOPSIS

rpmorphan.pl  [options] [targets]

options:

   -help                brief help message
   -man                 full documentation
   -V, --version        print version

   -verbose             verbose
   -fullalgo		force full algorythm
   -use-cache		use cache to avoid rpm query
   -clear-cache		remove cache file
   -gui			display the graphical interface

targets:

   -package pac		search if pac is an orphan package
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

keep file management

   -list-keep 		list permanent exclude list
   -zero-keep 		empty permanent exclude list
   -add-keep pac	add pac package to permanent exclude list
   -del-keep pac	remove pac package from permanent exclude list

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

=item B<-use-cache>

the rpm query may be long (10 to 30 s). If you will run an rpmorphan tool
several time, this option will allow to gain a lot of time :
it save the rpm query on a file cache (first call), then
use this cache instead quering rpm (others calls).

=item B<-clear-cache>

to remove cache file. Can be used with -use-cache to write
a new cache.

=item B<-gui>

display a graphical interface which allow to show informations, remove packages
(an internal help is provided). The perl-Tk package is necessary to run the gui.

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

for a small list of packages, rpmorphan use a different quicker methode : rpm -e --test

this option can be used to force the use of the full algo

=item B<-list-keep>

list the permanent list of excluded packages and exit.

=item B<-zero-keep>

empty the permanent list of excluded packages and exit.

=item B<-add-keep>

add package(s) to the permanent list of excluded packages and exit.

Can be used as '--add-keep pac1 --add-keep pac2'
or '--add-keep "pac1, pac2"'

=item B<-del-keep>

remove package(s) from the permanent list of excluded packages and exit.

Can be used as '--add-keep pac1 --add-keep pac2'
or '--add-keep "pac1, pac2"'

=back

=head1 USE

rpmorphan can be useful after a distribution upgrade, to remove packages forgotten
by the upgrade tool. It is interesting to use the options "-all -install-time +xx'.

If you want to remove some recent tested packages, my advice is "-all -install-time -xx'.

if you just want to clean your disk, use '-all -access-time xxx'

use the -use-cache option, if you intend to run it several times

=head1 FILES

/var/lib/rpmorphan/keep : the permanent exclude list

/tmp/rpmorphan.cache : cache file to store rpm query. The cache
file is common to all rpmorphan tools

=head1 NOTES

this program can be used as "normal" user
except the use of changes of the permanent exclude list

access-time and install-time options are "new" features, not available
in deborphan tool

=head1 SEE ALSO

=for man
\fIrpm\fR\|(1) for rpm call
.PP
\fIrpmusage\fR\|(1) for rpmusage use

=for html
<a href="rpmusage.1.html">rpmusage(1)</a>

=head1 COPYRIGHT

Copyright (C) 2006 by Eric Gerbier
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

=head1 AUTHORS

Eric Gerbier

you can report any bug or suggest to gerbier@users.sourceforge.net

=cut

