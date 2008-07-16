package szeng::jabber;

use strict;
use warnings;

no strict 'subs';
use szeng::protocol;

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

use AnyEvent;
use Net::XMPP2::Client;
use Storable;


my $j = AnyEvent->condvar;
my $Self;

# ------------------------------------------------------------------------------------------------------------------------------
my $timer;
sub ListenForMessages { 
$Self->{Connect}->send_message (
    'test 2' => 'slavazanko@gmail.com', undef, 'chat'
);

    $timer = AnyEvent->timer (after => 1, cb => sub {
	my $log = Log::Log4perl->get_logger("szeng::jabber");
	$log->debug("Ожидание активности");
#my $conn = $Self->{Connect}->spawn_connection;
$Self->{Connect}->send_message (
    'test 3!!!!!!!!!!!!!!!!!!!!!!!' => 'slavazanko@gmail.com', undef, 'chat'
);
	$szeng::sharedvars::DATA_jabber{lock}->down();
	if ( $szeng::sharedvars::DATA_jabber{needExit} eq 1 ){
	    $log->trace("Выход из потока");
	    $Self->disconnect();
	    $timer = undef;
	    return;
	}
        $Self->send_message();
        $j->broadcast;
        threads->yield();
        ListenForMessages();
    });
}
# ------------------------------------------------------------------------------------------------------------------------------
sub new {
    my $this = shift;
    my $class = ref($this) || $this;

    my $self = bless { }, $class;
    $self->{parent} = shift;
    my $log = Log::Log4perl->get_logger("szeng::jabber");
    $log->trace("Создание объекта JABBER");
    $self;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub mainCycle{
    my $self = shift;
    $Self = $self;
    my $log = Log::Log4perl->get_logger("szeng::jabber");
    $log->trace("Запуск функции mainCycle");
    return if ($self->{parent}->{config}{jabber}{enabled} ne 1);
    
    $log->debug("Устанавливаю соединение с JABBER-сервером");

    $self->{connection} = Net::XMPP2::Client->new (debug => 1);
    $self->{connection}->add_account ($self->{parent}->{config}{jabber}{uin}, $self->{parent}->{config}{jabber}{password});

    $self->{connection}->reg_cb (
	session_ready			=> sub { my ($cl, $acc) = @_; $Self->session_ready ($cl, $acc); },
	disconnect			=> sub { my ($cl, $acc, $h, $p, $reas) = @_; $Self->disconnect($cl, $acc, $h, $p, $reas); },
	error 				=> sub { my ($cl, $acc, $err) = @_; $Self->error($cl, $acc, $err); },
	message 			=> sub { my ($cl, $acc, $msg) = @_; $Self->message($cl, $acc, $msg); },
	contact_request_subscribe	=> sub { my ($cl, $acc, $roster, $contact) = @_; $Self->contact_request_subscribe($cl, $acc, $roster, $contact); },
	contact_did_unsubscribe		=> sub { my ($cl, $acc, $roster, $contact, $rdoit) = @_; $Self->contact_did_unsubscribe($cl, $acc, $roster, $contact, $rdoit); },
    );
    $self->{connection}->start;
    $j->wait;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub session_ready(){
    my $self = shift;
    my ($cl, $acc) = @_;
    my $log = Log::Log4perl->get_logger("szeng::jabber");
    $self->{Connect} = $cl;
    $self->{Account} = $acc;
    $log->debug("Соединение с JABBER-сервером установлено");
    ListenForMessages();
    1;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub disconnect {
    my $self = shift;
    my ($cl, $acc, $h, $p, $reas) = @_;
#    print "disconnect ($h:$p): $reas\n";
    $j->broadcast;
    1;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub error {
    my $self = shift;
    my ($cl, $acc, $err) = @_;
#    print "ERROR: " . $err->string . "\n";
    1;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub message {
    my $self = shift;
    my ($cl, $acc, $msg) = @_;
# тута можно чатбота устроить... и душевно с ним поговорить
#    print "message from: " . $msg->from . ": " . $msg->any_body . "\n";
    1;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub contact_request_subscribe {
    my $self = shift;
    my ($cl, $acc, $roster, $contact) = @_;
    $contact->send_subscribed;
#    warn "Subscribed to ".$contact->jid."\n";
}
# ------------------------------------------------------------------------------------------------------------------------------
sub contact_did_unsubscribe {
    my $self = shift;
    my ($cl, $acc, $roster, $contact, $rdoit) = @_;
    1;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub send_message(){
    my $self = shift;
    my $text = $szeng::sharedvars::DATA_common{subject}."\n\n".$szeng::sharedvars::DATA_common{body};
    $szeng::sharedvars::DATA_jabber{to} =~ s/^\s+//;
    my $contact;
    my $log = Log::Log4perl->get_logger("szeng::jabber");
    $log->trace("Отсылка сообщения");


warn($text);
    foreach $contact (split /\s+/ , $szeng::sharedvars::DATA_jabber{to}){
warn Dumper($contact);
#      my $immsg = Net::XMPP2::IM::Message->new (to => $contact, body => $text);
#      $immsg->send ($Self->{Connect});

	$self->{Connect}->send_message (
		$text => $contact, undef, 'chat'
        );
    }
    $log->trace("Отсылка сообщения завершена");
}
# ------------------------------------------------------------------------------------------------------------------------------


1;
