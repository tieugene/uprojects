package szeng::protocol;
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

use strict;
use warnings;

no strict 'refs';

use szeng::Object;

use vars qw($VERSION @ISA);
@ISA     	= qw(szeng::Object);

$VERSION = "0.0.1";

use Data::Dumper::Simple;


=head1
Реализация протокола сообщений

данный класс должен быть унаследован. В потомке должен быть определён массив 
@ProtocolCommandList - список команд, которые потомок может обслужить.

%ProtocolCommandList  = (
    'команда', 'обслуживающая функция',
    ... , ...
);


=cut



# ------------------------------------------------------------------------------------------------------------------------------
sub new {
    my $self = shift;
    my $obj = bless{};
    
    $obj->outer;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub protocol_parseCommand {
    my $self = shift;
    my $socket = shift;
    my $str = shift;

    my ($cmd, $lst_cmd);
    $str =~ s/[\n\r]//g;

    if ( $str =~ /^\s*$/ ){
	$self->protocol_error($socket, "команда отсутствует");
	return;
    }
    $str =~ /^(\S+)/; $cmd=lc($1);
    $str =~ s/^(\S+)\s*//;
    
    if ($cmd =~ /quit/ or $cmd =~ /exit/)  {
	$self->protocol_quit($socket, $cmd, $str);
    } elsif ($cmd =~ /icq/){
	$self->protocol_icq($socket, $cmd, $str);
    } elsif ($cmd =~ /jabber/){
	$self->protocol_jabber($socket, $cmd, $str);
    } elsif ($cmd =~ /email/){
	$self->protocol_email($socket, $cmd, $str);
    } elsif ($cmd =~ /subject/){
	$self->protocol_subject($socket, $cmd, $str);
    } elsif ($cmd =~ /body/){
	$self->protocol_body($socket, $cmd, $str);
    } elsif ($cmd =~ /send/){
	$self->protocol_send($socket, $cmd, $str);
    } elsif ($cmd =~ /abort/){
	$self->protocol_abort($socket, $cmd, $str);
    } else{ 
	$self->protocol_error($socket, "неизвестная команда");
    }
}
# ------------------------------------------------------------------------------------------------------------------------------
sub protocol_ok{
    my $self = shift;
    my $socket = shift; $socket = $$socket; $socket = *$socket;
    send ($socket, "ok\n", 0);
}
# ------------------------------------------------------------------------------------------------------------------------------
sub protocol_error{
    my $self = shift;
    my $socket = shift; $socket = $$socket; $socket = *$socket;
    my $text = shift;
    $text =~ s/\n/\\n/g;     send ($socket, "error ".$text."\n", 0);
}
# ------------------------------------------------------------------------------------------------------------------------------

1;
