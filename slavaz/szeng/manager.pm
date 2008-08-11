package szeng::manager;
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
use Data::Dumper::Simple;

use vars qw($VERSION $BASE_DN $LDAP_HOST @ISA);
@ISA     	= qw(szeng::Object);

$VERSION = "0.0.1";


use threads;
use threads::shared;
use Thread::Semaphore;
use Log::Log4perl;
use szeng::Object;
use szeng::config::ldap;
use szeng::config::file;
use szeng::jabber;
use szeng::icq;
use szeng::email;
use szeng::serversocket;
use szeng::sharedvars;

Log::Log4perl::init_and_watch('MesSer.log.conf',10);

my $log = Log::Log4perl->get_logger("MesSer::main");
$log->info("Запуск программы");

my $THREAD_socket_object	= undef;
my $THREAD_icq_object		= undef;
my $THREAD_jabber_object	= undef;
my $THREAD_email_object		= undef;

# TODO:
#warn Dumper(%SIG);
#exit;

my($socketThread,$emailThread, $icqThread, $jabberThread) = (\'',\'',\'',\'');

my $MANAGER = szeng::manager->new();
$MANAGER->mainCycle();

# ------------------------------------------------------------------------------------------------------------------------------
sub new {
    my $self  = shift;
    my $obj = bless{};
    my $log = Log::Log4perl->get_logger("szeng::manager");
    $log->trace("Создание объекта MANAGER");
    $obj->outer;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub getConfig{
    my $self = shift;
    my @args=@ARGV;
    my $arg;
    
    $arg = shift(@args);
    
    $self->{conf} = undef;
    $self->{confParam} = undef;
    while ($arg){
	if ($arg =~ /^\-c$/){
	    $self->{conf} = szeng::config::file->new();
	    $arg = shift @args;
	    $self->{confParam} = $arg;
	}
	$arg = shift @args;
    }
    if (not defined ($self->{conf})){
	$self->{conf} = szeng::config::ldap->new();
	$self->{confParam} = '(cn=Messenger)';
    }
}
# ------------------------------------------------------------------------------------------------------------------------------
sub mainCycle{
    my $self = shift;
    my $log = Log::Log4perl->get_logger("szeng::manager");
    $log->info("Запуск основного цикла обработки");

    $self->getConfig();
    $self->initShareData();

    while(1){
	my @running = threads->list();
	my %running;
	$self->{config} = {$self->{conf}->getConfig($self->{confParam})};
	my $r; foreach $r (@running){
	    $running{socketThread} = 1 if ($$r eq $$socketThread);
	    $running{emailThread} = 1 if ($$r eq $$emailThread and $self->{config}{email}{enabled} eq 1);
	    $running{icqThread} = 1 if ($$r eq $$icqThread  and $self->{config}{icq}{enabled} eq 1);
	    $running{jabberThread} = 1 if ($$r eq $$jabberThread  and $self->{config}{jabber}{enabled} eq 1);
	}

	$log->trace("Проверка, что сокетный поток работает");
	if (not exists($running{socketThread})){
	    $log->debug("Запускаю цикл обработки сетевых соединений");
	    $socketThread = threads->create("__CreateSocketThread");
	}
	$log->trace("Проверка, что помощник отсылки jabber-сообщений работает");
	if (not exists($running{jabberThread})  and $self->{config}{jabber}{enabled} eq 1){
	    $log->debug("Запускаю помощника отсылки jabber-сообщений");
	    $jabberThread = threads->create("__CreateJabberThread");
	}

	$log->trace("Проверка, что помощник отсылки icq-сообщений работает");
	if (not exists($running{icqThread})  and $self->{config}{icq}{enabled} eq 1){
	    $log->debug("Запускаю помощника отсылки icq-сообщений");
	    $icqThread = threads->create("__CreateIcqThread");
	}
	$log->trace("Проверка, что помощник отсылки email-сообщений работает");
	if (not exists($running{emailThread})  and $self->{config}{email}{enabled} eq 1){
	    $log->debug("Запускаю помощника отсылки email-сообщений");
	    $emailThread = threads->create("__CreateEmailThread");
	}

	my $slp=300; while ($slp--){
	    threads->yield();
	    sleep(1);
	}
    }
}
# ------------------------------------------------------------------------------------------------------------------------------
sub initShareData{
    my $self  = shift;

    share %szeng::sharedvars::DATA_common;
    
    $szeng::sharedvars::DATA_common{subject} = '';
    $szeng::sharedvars::DATA_common{body} = '';

    share %szeng::sharedvars::DATA_jabber;
    $szeng::sharedvars::DATA_jabber{to} = '';
    $szeng::sharedvars::DATA_jabber{needExit} = 0;
    $szeng::sharedvars::DATA_jabber{lock} = 1;

    share %szeng::sharedvars::DATA_icq;
    $szeng::sharedvars::DATA_icq{to} = '';
    $szeng::sharedvars::DATA_icq{needExit} = 0;
    $szeng::sharedvars::DATA_icq{lock} = 1;

    share %szeng::sharedvars::DATA_email;
    $szeng::sharedvars::DATA_email{to} = '';
    $szeng::sharedvars::DATA_email{needExit} = 0;
    $szeng::sharedvars::DATA_email{lock} = 1;
}
# ------------------------------------------------------------------------------------------------------------------------------
# запускальщики потоков
# ------------------------------------------------------------------------------------------------------------------------------
sub __CreateSocketThread{
    $THREAD_socket_object = szeng::serversocket->new($MANAGER);
    $THREAD_socket_object->mainCycle();
}
# ------------------------------------------------------------------------------------------------------------------------------
sub __CreateJabberThread{
    $THREAD_jabber_object =  szeng::jabber->new($MANAGER);

    $THREAD_jabber_object->mainCycle();
}
# ------------------------------------------------------------------------------------------------------------------------------
sub __CreateIcqThread{
    $THREAD_icq_object =  szeng::icq->new($MANAGER);

    $THREAD_icq_object->mainCycle();
}
# ------------------------------------------------------------------------------------------------------------------------------
sub __CreateEmailThread{
    $THREAD_email_object =  szeng::email->new($MANAGER);

    $THREAD_email_object->mainCycle();
}
# ------------------------------------------------------------------------------------------------------------------------------

1;

=head1
0) перехватывать сигнал прерывания и корректно выходить
1) +родительский поток читает конфиг
2) +создать поток, который будет висеть на сокете (из конфига)
3) если аська разрешена, то создать обслуживающий поток. Если поток есть - пропуск
4) если мыло разрешено, то создать обслуживающий поток. Если поток есть - пропуск
5) +если жаббер разрешён, то создать обслуживающий поток. Если поток есть - пропуск

+дочерний поток может грохнуться. Надо как-то отследить это...
+дочерний поток нужно будет грохнуть. В дочернем потоке перехватывать сигналы?

+взаимодействие между потоками через семафорные переменные?

=cut

