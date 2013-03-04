package szeng::icq;
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

no strict 'subs';
use szeng::protocol;

use subs qw (protocol_quit);

use vars qw($VERSION @ISA);
@ISA     	= qw(szeng::protocol);

$VERSION = "0.0.1";

use Net::OSCAR;
use Net::DNS;

use Data::Dumper::Simple;

my $resolver = Net::DNS::Resolver->new();

my $Self;
# ------------------------------------------------------------------------------------------------------------------------------
sub new {
    my $this = shift;
    my $class = ref($this) || $this;

    my $self = bless { }, $class;
    $self->{parent} = shift;
    my $log = Log::Log4perl->get_logger("szeng::icq");
    $log->trace("Создание объекта ICQ");
    $self;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub mainCycle{
    my $self = shift;
    $Self = $self;
    my $log = Log::Log4perl->get_logger("szeng::icq");
    $log->trace("Запуск функции mainCycle");
    return if ($self->{parent}->{config}{icq}{enabled} ne 1);
    $szeng::sharedvars::DATA_icq{lock} = 1;


    $self->{connection} = Net::OSCAR->new();
    
    $self->{connection}->set_callback_im_in( sub {
	# кто-то нам написал
    });

    $self->{connection}->set_callback_signon_done(sub{
	my ($oscar) = @_;
	my $log = Log::Log4perl->get_logger("szeng::icq");
	$log->debug("Соединение с ICQ-сервером установлено");

	while( $szeng::sharedvars::DATA_icq{needExit} eq 0 ) {
	    if ($szeng::sharedvars::DATA_icq{lock} eq 1){
		sleep 1;
		next;
	    }
	    $log->trace("Рассылка сообщения");

	    my $text =  $szeng::sharedvars::DATA_common{subject}."\n\n".$szeng::sharedvars::DATA_common{body};
	    $text = Encode::encode("cp1251",Encode::decode_utf8($text));

	    my $cntcts = $szeng::sharedvars::DATA_icq{to};
	    # общие переменные скопировали себе... сокетный поток может их грохнуть.
	    $szeng::sharedvars::DATA_icq{lock} = 1;
	
	    $cntcts =~ s/^\s+//;
    	    my $contact;
    	    foreach $contact (split /\s+/ , $cntcts){
    		$log->trace("Отсылка к ".$contact);
    		$oscar->send_im( $contact , $text );
	    }
	    $log->trace("Рассылка сообщения завершена");
	    $szeng::sharedvars::DATA_icq{to} = '';
	
	}

#	$Self->ListenForMessages($oscar);

    });

    $log->debug("Устанавливаю соединение с ICQ-сервером");
    if ( not $self->{connection}->signon($self->{parent}->{config}{'icq'}{'uin'}, $self->{parent}->{config}{'icq'}{'password'})){
	$log->error("Ошибка соединения! Жду 10 минут перед повтором");
	sleep 600;
	return;
    }

    while( $szeng::sharedvars::DATA_icq{needExit} eq 0 ) {
        $self->{connection}->do_one_loop();
    }
    $self->{connection}->sign_off();
}
# ------------------------------------------------------------------------------------------------------------------------------
sub ListenForMessages {
    my $self = shift;
    my $oscar = shift;
    my $log = Log::Log4perl->get_logger("szeng::icq");

}
# ------------------------------------------------------------------------------------------------------------------------------


1;