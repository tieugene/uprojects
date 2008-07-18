package szeng::protocol;

use strict;
#use utf8;
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
