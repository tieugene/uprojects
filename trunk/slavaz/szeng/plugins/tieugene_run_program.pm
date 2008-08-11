package szeng::plugins::tieugene_run_program;
#----------------------------------------------------------------------
# Description:
# Author: SlavaZ 
# Created at: Mon Jul 21 16:23:16 EEST 2008
#    
# Copyright (c) 2008 SlavaZ  All rights reserved.
#
#----------------------------------------------------------------------
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions, and the following disclaimer,
#    without modification.
# 2. Redistributions in binary form must reproduce at minimum a disclaimer
#    substantially similar to the "NO WARRANTY" disclaimer below
#    ("Disclaimer") and any redistribution must be conditioned upon
#    including a substantially similar Disclaimer requirement for further
#    binary redistribution.
# 3. Neither the names of the above-listed copyright holders nor the names
#    of any contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# Alternatively, this software may be distributed under the terms of the
# GNU General Public License ("GPL") version 2 as published by the Free
# Software Foundation.
#
# NO WARRANTY
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTIBILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDERS OR CONTRIBUTORS BE LIABLE FOR SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGES.
# 

use Data::Dumper::Simple;

sub startPlugin{
    my $self = shift;
    my $config = shift;
    my $events = shift;

    my $fileName;
    foreach $fileName (keys(%{$events})){
	# отбираем только файловые операции
	my $action = $events->{$fileName}->{actionMyName};
	next if (
	    ( $action ne "create") &&
	    ( $action ne "modify") &&
	    ( $action ne "unlink"));

	$fileName =~ s/'/'\\''/g; #'
	my $user = getpwuid($events->{$fileName}->{audit}->{uid});
	$user =~ s/'/'\\''/g; #'

	my $args = $config->{args};
	
	
	$args =~ s/\[file\]/'$fileName'/;
	$args =~ s/\[action\]/'$action'/;
	$args =~ s/\[owner\]/'$user'/;
	
	my $runStr = $config->{path}." ".$args;
	system($runStr);
    }
    return 1;
}

1;
