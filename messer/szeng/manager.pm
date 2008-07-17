package szeng::manager;

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
use szeng::ldap;
use szeng::jabber;
use szeng::serversocket;
use szeng::sharedvars;

#Log::Log4perl::init_and_watch('/usr/local/etc/MesSer.conf',10);
Log::Log4perl::init_and_watch('MesSer.conf',10);
my $log = Log::Log4perl->get_logger("MesSer::main");
$log->info("Запуск программы");



my $THREAD_socket	= undef;
my $THREAD_icq		= undef;
my $THREAD_jabber	= undef;
my $THREAD_email	= undef;

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
    $obj->{ldap} = szeng::ldap->new();
    $obj->outer;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub mainCycle{
    my $self = shift;
    my $log = Log::Log4perl->get_logger("szeng::manager");
    $log->info("Запуск основного цикла обработки");

    $self->initShareData();

    while(1){
	my @running = threads->list();
	my %running;
	$self->{config} = {$self->{ldap}->readConfig("ou=Services","(cn=Messenger)")};

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
    $szeng::sharedvars::DATA_jabber{lock} = new Thread::Semaphore();
    $szeng::sharedvars::DATA_jabber{lock}->down;

    share %szeng::sharedvars::DATA_icq;
    $szeng::sharedvars::DATA_icq{to} = undef;
    $szeng::sharedvars::DATA_icq{needExit} = 0;
    $szeng::sharedvars::DATA_icq{lock} = new Thread::Semaphore();
    $szeng::sharedvars::DATA_icq{lock}->down;

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
    $THREAD_socket = szeng::serversocket->new($MANAGER);
    $THREAD_socket->mainCycle();
}
# ------------------------------------------------------------------------------------------------------------------------------
sub __CreateJabberThread{
    $THREAD_jabber =  szeng::jabber->new($MANAGER);

    $THREAD_jabber->mainCycle();
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
дочерний поток нужно будет грохнуть. В дочернем потоке перехватывать сигналы?

+взаимодействие между потоками через семафорные переменные?

=cut

