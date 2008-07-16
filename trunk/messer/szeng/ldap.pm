package szeng::ldap;

use strict;
use szeng::Object;

use vars qw($VERSION $BASE_DN $LDAP_HOST @ISA);
@ISA     	= qw(szeng::Object);

$VERSION = "0.0.1";
$BASE_DN = "dc=lc,dc=floodlightgames,dc=com";
$LDAP_HOST = "127.0.0.1";

require Net::LDAP;  # this should load everything you need

use Data::Dumper::Simple;
use Log::Log4perl;


# ------------------------------------------------------------------------------------------------------------------------------
sub new {
    my $log = Log::Log4perl->get_logger("szeng::ldap");
    $log->trace("Создание объекта LDAP");
    my $self  = shift;
    my $obj = bless{};
    $log->debug("Подключение к LDAP-серверу");
    $obj->{ldap} = Net::LDAP->new($LDAP_HOST);
    $obj->{mesg} = $obj->{ldap}->bind;
    $log->trace("Завершение создания объекта LDAP");
    $obj->outer;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub readConfig {
    my $log = Log::Log4perl->get_logger("szeng::ldap");
    $log->trace("Вызов метода readConfig");
    my $self  = shift;
    my $searchBase = shift;
    my $searchCond = shift;
    my $hash;
    $log->debug("Чтение конфигурационных параметров для ".$searchCond." - ".$searchBase.",".$BASE_DN);
    
    $self->{mesg} = $self->{ldap}->search( filter=>$searchCond, 
                         base=>$searchBase.",".$BASE_DN);
    
    $hash = $self->{mesg}->as_struct;
    my @arr  = keys %$hash;
    $self->ldapDataToArray($$hash{$arr[0]}->{description});
}

# ------------------------------------------------------------------------------------------------------------------------------
sub ldapDataToArray {
    my $self  = shift;
    my $data = shift;

    my %ret;
    my ($dt, @var1, $var2, $var3, $var4);
    
    foreach $dt (@$data){
	$dt =~ /\[(.+)\s=\s(.*)/;
	$var2 = $2;
	@var1=split /\]\[/ , $1.'[';
	$var4 = '';
	for ($var3=0; $var3<scalar(@var1);$var3++){
	    $var4=$var4.'{'.$var1[$var3].'}';
	    if ($var3 ne  scalar(@var1)-1) {
		eval('if (not exists($ret'.$var4.')){ $ret'.$var4.'={};}');
	    } else {
		$var2 =~ s/"/\\"/g; $var2 =~ s/@/\\@/g;  $var2 =~ s/%/\\%/g;  $var2 =~ s/\$/\\\$/g;  $var2 =~ s/&/\\&/g;
		eval('$ret'.$var4.'= "'.$var2.'"');
	    }
	}
    }
    %ret;
}
# ------------------------------------------------------------------------------------------------------------------------------

1;
