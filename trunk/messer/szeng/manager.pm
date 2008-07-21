package szeng::manager;

use strict;
use Data::Dumper::Simple;

use vars qw($VERSION $BASE_DN $LDAP_HOST @ISA);
@ISA     	= qw(szeng::Object);

$VERSION = "0.0.1";


use threads;
use threads::shared;
use Thread::Semaphore; #!!!!!!!!!!!!!
use Log::Log4perl;
use szeng::Object;
use szeng::config::ldap;
use szeng::config::file;
use szeng::jabber;
use szeng::icq;
use szeng::serversocket;
use szeng::sharedvars;

Log::Log4perl::init_and_watch('MesSer.log.conf',10);

my $log = Log::Log4perl->get_logger("MesSer::main");
$log->info("Запуск программы");

my $THREAD_socket_object	= undef;
my $THREAD_icq_object		= undef;
my $THREAD_jabber_object	= undef;
my $THREAD_email_object	= undef;

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
	    $jabberThread = threads->create("__CreateIcqThread");
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
    $szeng::sharedvars::DATA_icq{to} = undef;
    $szeng::sharedvars::DATA_icq{needExit} = 0;
    $szeng::sharedvars::DATA_icq{lock} = 1;

    share %szeng::sharedvars::DATA_email;
    $szeng::sharedvars::DATA_email{to} = undef;
    $szeng::sharedvars::DATA_email{needExit} = 0;
    $szeng::sharedvars::DATA_email{lock} = new Thread::Semaphore();
    $szeng::sharedvars::DATA_email{lock}->down;
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

