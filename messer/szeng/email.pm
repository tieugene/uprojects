package szeng::email;
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
require Encode;
use warnings;

use POSIX qw(strftime);
use Net::SMTP::SSL;
use Data::Dumper::Simple;
use szeng::protocol;

no strict 'subs';

use subs qw (protocol_quit);

use vars qw($VERSION @ISA);
@ISA     	= qw(szeng::protocol);

$VERSION = "0.0.1";



my $Self;
# ------------------------------------------------------------------------------------------------------------------------------
sub new {
    my $this = shift;
    my $class = ref($this) || $this;

    my $self = bless { }, $class;
    $self->{parent} = shift;
    my $log = Log::Log4perl->get_logger("szeng::email");
    $log->trace("Создание объекта EMAIL");
    $self;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub mainCycle{
    my $self = shift;
    $Self = $self;
    my $log = Log::Log4perl->get_logger("szeng::email");
    $log->trace("Запуск функции mainCycle");
    return if ($self->{parent}->{config}{email}{enabled} ne 1);
    $szeng::sharedvars::DATA_email{lock} = 1;

    while( $szeng::sharedvars::DATA_email{needExit} eq 0 ) {
        if ($szeng::sharedvars::DATA_email{lock} eq 1){
	    sleep 1;
	    next;
	}
	$log->trace("Рассылка сообщения");
	
	
	my $subject = Encode::decode('UTF-8',$szeng::sharedvars::DATA_common{subject});
	my $text =  Encode::decode('UTF-8',$szeng::sharedvars::DATA_common{body});

	my $cntcts = $szeng::sharedvars::DATA_email{to};
	# общие переменные скопировали себе... сокетный поток может их грохнуть.
	$szeng::sharedvars::DATA_email{lock} = 1;

	$cntcts =~ s/^\s+//;
	my $smtp;
	if (not $smtp = Net::SMTP::SSL->new(
			    $self->{parent}->{config}{email}{auth_host}, 
			    Port => $self->{parent}->{config}{email}{auth_port}, 
			    Debug => 0)) {
	    $log->error("Невозможно присоединиться к серверу!");
	    next;
	}
	if (not $smtp->auth($self->{parent}->{config}{email}{auth_user}, $self->{parent}->{config}{email}{auth_password})){
	    $log->error("Неверные аутентификационные данные, предоставляемые серверу!");
	    print("SMTP authentication failed!\n");
	    $smtp=undef;
	    next;
	}
	                        
        
    	my $contact;
    	foreach $contact (split /\s+/ , $cntcts){
    	    $log->trace("Отсылка к ".$contact);
	    $smtp->mail($self->{parent}->{config}{'email'}{'from'} . "\n");
	    $smtp->to($contact . "\n");
    	    $smtp->data();
	    $smtp->datasend("From: " . $self->{parent}->{config}{'email'}{'from'} . "\n");
    	    $smtp->datasend("To: " . $contact . "\n");
    	    $smtp->datasend("Date: " . strftime('%a, %d %b %Y %H:%M:%S %z', localtime(time)) . "\n");
	    $smtp->datasend("Content-Type: text/plain; charset=UTF-8". "\n");
	    $smtp->datasend("Content-Transfer-Encoding: 8bit". "\n");
    	    $smtp->datasend("Subject: " . $subject . "\n");
    	    $smtp->datasend("\n");
    	    $smtp->datasend($text."\n");
    	    $smtp->dataend();
    	    $smtp->quit;
	}
	$log->trace("Рассылка сообщения завершена");
	$smtp = undef;
	$szeng::sharedvars::DATA_email{to} = '';

    }

}
# ------------------------------------------------------------------------------------------------------------------------------
1;
