#!/usr/bin/perl
###############################################################################
#   test_rpmorphan.pl
#
#    Copyright (C) 2006 by Eric Gerbier
#    Bug reports to: gerbier@users.sourceforge.net
#    $Id: rpmrestore.pl 28 2006-11-13 14:39:50Z gerbier $
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
# test of rpmorphan software

use strict;
use warnings;
use Test::More qw(no_plan);
use Data::Dumper;

# arguments test
my $cmd = './rpmorphan.pl';

################### options ##############################
# 1 no arg
my $out = `$cmd 2>&1`;
like( $out, qr/need a target/, 'no arg' );

# 2 version
$out = `$cmd --version 2>&1`;
like( $out, qr/rpmorphan\.pl version/, 'version' );

# 3 help
$out = `$cmd --help`;
like( $out, qr/Usage:/, 'help' );

# 4 man
$out = `$cmd --man`;
like( $out, qr/User Contributed Perl Documentation/, 'man' );

############# keep ###########################################

# test if run on superuser
if ( $> == 0 ) {

	# 5 add-keep
	$out = `$cmd --zero-keep`;
	$out = `$cmd --add-keep "rpm,rpmrestore" --verbose`;
	like( $out, qr/add keep rpmrestore/, 'add-keep' );

	# 6 list-keep
	$out = `$cmd --list-keep`;
	like( $out, qr/rpm rpmrestore/, 'list-keep' );

	# 7 add-keep duplicate
	$out = `$cmd --add-keep rpmrestore --verbose`;
	like( $out, qr/skip add duplicate rpmrestore/, 'duplicate' );

	# 8 del-keep
	$out = `$cmd --del-keep rpmrestore --verbose`;
	like( $out, qr/del keep rpmrestore/, 'del-keep' );

	# 9 del-keep
	$out = `$cmd --del-keep rpmrestore --verbose`;
	like( $out, qr/^$/, 'del-keep2' );

	# 9 test exclude
	$out = `$cmd --package rpm --verbose`;
	like( $out, qr/permanent exclude rpm/, 'test permanent exclude' );

	# 11 zero-keep
	$out = `$cmd --zero-keep`;
	like( $out, qr/^$/, 'zero-keep' );
}
else {
	diag('you should be root to run keep tests');
}

#################### package ################################

# 12 not orphan package quicksolve
$out = `$cmd --package rpm --verbose -use-cache`;
like( $out, qr/rpm is required by/, 'not orphan quicksolve' );

# 13 not orphan package
$out = `$cmd --package rpm --verbose --fullalgo -use-cache`;
like( $out, qr/rpm is required by/, 'not orphan full' );

# 14 orphan package
$out = `$cmd --package rpmrestore -use-cache`;
like( $out, qr/rpmrestore/, 'orphan quicksolve' );

# 15 orphan package
$out = `$cmd --package rpmrestore --fullalgo  -use-cache`;
like( $out, qr/rpmrestore/, 'orphan full' );

# 16 exclude
$out = `$cmd --package rpm --exclude rpm --verbose  -use-cache`;
like( $out, qr/skip rpm : excluded/, 'exclude' );

# 17 custom
$out = `$cmd --guess-custom "^webm" -use-cache`;
like( $out, qr/webmin/, 'guess-custom' );

# 18 virtual
$out = `$cmd --package elinks --verbose --fullalgo -use-cache`;
like( $out, qr/skip virtual provide webclient/, 'virtual' );

# 19 many packages
my @out = `$cmd --package lilo --package "grub,elinks"  -use-cache`;
chomp(@out);
my @res = ( 'lilo', 'grub', 'elinks' );
ok( eq_array( \@out, \@res ), 'many packages' );

exit;

#
# 11 install-time

# 12 access-time

# 13 mode quicksolve
#
# 14 auto-depend

__END__

=head1 NAME

test_rpmorphan - test rpmorphan software

=head1 DESCRIPTION

this is designed to check if rpmorphan software is working :
test for options
test if all features works

=head1 SEE ALSO

=for man
\fIrpmorphan\fR\|(1) for rpmorphan call

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
