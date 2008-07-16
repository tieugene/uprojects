package szeng::serversocket;

use strict;
use warnings;

no strict 'subs';
use szeng::protocol;
use szeng::sharedvars;

use subs qw (protocol_quit);

#no strict 'refs';

use vars qw($VERSION @ISA);
@ISA     	= qw(szeng::protocol);

$VERSION = "0.0.1";

use Data::Dumper::Simple;
use Socket;
use threads;
use threads::shared;
use Thread::Semaphore;
use Log::Log4perl;


# ------------------------------------------------------------------------------------------------------------------------------
sub new {
    my $self = shift;
    my $obj = bless ({}, ref($self) || $self);
    my $log = Log::Log4perl->get_logger("szeng::serversocket");
    my $proto  = getprotobyname('tcp');

    $log->trace("Создание объекта SERVERSOCKET");
    $obj->{parent} = shift;
    $obj->{neededExit} = 0;

    $obj->initBuffers();

    $log->debug("Создание tcp-сокета");
    socket($obj->{socket}, PF_INET, SOCK_STREAM, $proto) or die("невозможно создать сокет: $!");
    $log->debug("Настройка tcp-сокета");
    setsockopt($obj->{socket}, SOL_SOCKET, SO_REUSEADDR, pack("l", 1)) or die("Невозможно настроить сокет: $!");
    $obj;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub initBuffers{
    my $self = shift;
    $szeng::sharedvars::DATA_common{subject} = '';
    $szeng::sharedvars::DATA_common{body} = '';

    $szeng::sharedvars::DATA_jabber{to} = '';
    $szeng::sharedvars::DATA_icq{to} = '';
    $szeng::sharedvars::DATA_email{to} = '';
}
# ------------------------------------------------------------------------------------------------------------------------------
sub mainCycle{
    my $self = shift;
    my $log = Log::Log4perl->get_logger("szeng::serversocket");
    my $paddr;
    my $buff;
    my $CLIENT;
    
    $log->trace("Запуск функции mainCycle");
    
    $log->debug("Присоединение сокета к интерфейсу и порту :".$self->{parent}->{config}{main}{port});
    bind($self->{socket}, sockaddr_in($self->{parent}->{config}{main}{port}, INADDR_LOOPBACK)) or die "bind: $!";
    $log->debug("Запуск сокета в 'слушающем' режиме");
    
    listen($self->{socket}, SOMAXCONN) or die "невозможно запустить сокет в 'слушающем' режиме: $!";
    for(; $paddr = accept($CLIENT, $self->{socket}); close $CLIENT){
	my($port,$iaddr) = sockaddr_in($paddr);
	my $name = gethostbyaddr($iaddr,AF_INET);
	$self->{neededExit} = 0;
	$log->debug("Принято новое соединение ");
	while(defined($buff = <$CLIENT>)){
    	    $log->trace("Принята строка : ".$buff);
    	    $self->protocol_parseCommand($CLIENT, $buff);
    	    last if $self->{neededExit} eq 1;
	}
	$log->debug("соединение закрыто");
    }
}
# ------------------------------------------------------------------------------------------------------------------------------
sub protocol_quit{
    my $self = shift;
    my $socket = shift; 
    my $log = Log::Log4perl->get_logger("szeng::serversocket");
    $log->debug("Команда закрытия соединения");
    $self->protocol_ok($socket);
    $socket = $$socket; $socket = *$socket;
    close $socket;
    $self->{neededExit} = 1;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub protocol_icq{
    my $self = shift;
    my $socket = shift; 
    my $cmd = shift;
    my $params = shift;
    my $log = Log::Log4perl->get_logger("szeng::serversocket");
    $log->debug("Подготовительная команда для рассылки по ICQ");
    if ($params =~ /^\s*$/) {
	$self->protocol_error($socket, "Отсутствуют параметры команды");
	return;
    }
    if ($params =~ /[^\d\s]+/) {
	$self->protocol_error($socket, "В параметрах есть не ICQ-контакты");
	return;
    }
    $szeng::sharedvars::DATA_icq{to}.=" ".$params;
    $self->protocol_ok($socket);
}
# ------------------------------------------------------------------------------------------------------------------------------
sub checkValidEmail{
    my $self = shift;
    my $str = shift;
    my $eml;
    
    foreach $eml (split /\s+/ , $str){
	return 0 if ($eml !~ /^[a-zA-Z0-9\-\.\_\+\:]+@[a-zA-Z0-9\-\.]+/);
	return 0 if ($eml =~ /.*@.*@/);
	return 0 if ($eml =~ /@\./);
	return 0 if ($eml =~ /\.\./);
	return 0 if ($eml !~ /.*@.*\./);
    }
    return 1;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub protocol_jabber{
    my $self = shift;
    my $socket = shift; 
    my $cmd = shift;
    my $params = shift;
    my $log = Log::Log4perl->get_logger("szeng::serversocket");
    $log->debug("Подготовительная команда для рассылки по Jabber");
    if ($params =~ /^\s*$/) {
	$self->protocol_error($socket, "Отсутствуют параметры команды");
	return;
    }
    if (not $self->checkValidEmail($params)) {
	$self->protocol_error($socket, "В параметрах есть не JABBER-контакты");
	return;
    }
    $szeng::sharedvars::DATA_jabber{to}.=" ".$params;
    $self->protocol_ok($socket);
}
# ------------------------------------------------------------------------------------------------------------------------------
sub protocol_email{
    my $self = shift;
    my $socket = shift; 
    my $cmd = shift;
    my $params = shift;
    my $log = Log::Log4perl->get_logger("szeng::serversocket");
    $log->debug("Подготовительная команда для рассылки по email");
    if ($params =~ /^\s*$/) {
	$self->protocol_error($socket, "Отсутствуют параметры команды");
	return;
    }
    if (not $self->checkValidEmail($params)) {
	$self->protocol_error($socket, "В параметрах есть не EMAIL-контакты");
	return;
    }
    $szeng::sharedvars::DATA_email{to}.=" ".$params;
    $self->protocol_ok($socket);
}
# ------------------------------------------------------------------------------------------------------------------------------
sub protocol_subject{
    my $self = shift;
    my $socket = shift; 
    my $cmd = shift;
    my $params = shift;
    my $log = Log::Log4perl->get_logger("szeng::serversocket");
    $log->debug("Подготовительная команда установки темы сообщения");
    $szeng::sharedvars::DATA_common{subject}.=$params." ";
    $self->protocol_ok($socket);
}
# ------------------------------------------------------------------------------------------------------------------------------
sub protocol_body{
    my $self = shift;
    my $socket = shift; 
    my $cmd = shift;
    my $params = shift;
    my $log = Log::Log4perl->get_logger("szeng::serversocket");
    $log->debug("Подготовительная команда для установки содержимого сообщения");
    $szeng::sharedvars::DATA_common{body}.=$params."\n";
warn Dumper($szeng::sharedvars::DATA_common);
print "-------------------------\n";
    $self->protocol_ok($socket);
}
# ------------------------------------------------------------------------------------------------------------------------------
sub protocol_abort{
    my $self = shift;
    my $socket = shift; 
    my $cmd = shift;
    my $params = shift;
    my $log = Log::Log4perl->get_logger("szeng::serversocket");
    $log->debug("Команда отмены подготовительных команд");
    
    if ( $params =~ /^\s*$/){
	$log->trace("Очистка всех буферов");
	$self->initBuffers();
    } else {
	my $str;
	foreach $str (split /\s+ /, $params){
	    if ($str =~ /icq/)  {
		$log->trace("Очистка ICQ буфера");
		$szeng::sharedvars::DATA_icq{to} = '';
	    } elsif ($str =~ /jabber/)  {
		$log->trace("Очистка JABBER буфера");
		$szeng::sharedvars::DATA_jabber{to} = '';
	    } elsif ($str =~ /email/)  {
		$log->trace("Очистка EMAIL буфера");
		$szeng::sharedvars::DATA_email{to} = '';
	    } elsif ($str =~ /subject/)  {
		$log->trace("Очистка буфера заголовка сообщения");
		$szeng::sharedvars::DATA_common{subject} = '';
	    } elsif ($str =~ /body/)  {
		$log->trace("Очистка буфера содержимого сообщения");
		$szeng::sharedvars::DATA_common{body} = '';
	    }
	}
    }
    $self->protocol_ok($socket);
}
# ------------------------------------------------------------------------------------------------------------------------------
sub protocol_send{
    my $self = shift;
    my $socket = shift; 
    my $cmd = shift;
    my $params = shift;
    my $log = Log::Log4perl->get_logger("szeng::serversocket");
    $log->debug("Команда непосредственной отсылки сообщений");
warn Dumper($szeng::sharedvars::DATA_common);
warn Dumper($szeng::sharedvars::DATA_jabber);

    if ($szeng::sharedvars::DATA_jabber{needExit} eq 0){
	$szeng::sharedvars::DATA_jabber{lock}->up;
    }
    if ($szeng::sharedvars::DATA_icq{needExit} eq 0){
	$szeng::sharedvars::DATA_icq{lock}->up;
    }
    if ($szeng::sharedvars::DATA_email{needExit} eq 0){
	$szeng::sharedvars::DATA_email{lock}->up;
    }
    $self->protocol_ok($socket);
}
# ------------------------------------------------------------------------------------------------------------------------------

1;
