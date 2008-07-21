package szeng::email;

use strict;
require Encode;
use warnings;

use POSIX qw(strftime);
use Net::SMTP::SSL;
use Data::Dumper::Simple;

no strict 'subs';
use szeng::protocol;

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
