package szeng::icq;

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