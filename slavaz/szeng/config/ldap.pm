package szeng::config::ldap;
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
use szeng::Object;

use vars qw($VERSION $BASE_DN $LDAP_HOST @ISA);
@ISA     	= qw(szeng::Object);

$VERSION = "0.0.1";
$BASE_DN = "dc=lc,dc=floodlightgames,dc=com";
$LDAP_HOST = "server";
my $searchBase = 'ou=Services';

require Net::LDAP;
use Log::Log4perl;


# ------------------------------------------------------------------------------------------------------------------------------
sub new {
    my $log = Log::Log4perl->get_logger("szeng::config::ldap");
    $log->trace("Создание объекта CONIG::LDAP");
    my $self  = shift;
    my $sdata = shift;
    $sdata = $searchBase if not defined($sdata);
    my $obj = bless{};
    $log->debug("Подключение к LDAP-серверу");
    $obj->{ldap} = Net::LDAP->new($LDAP_HOST);
    $obj->{mesg} = $obj->{ldap}->bind;
    $obj->{searchBase} = $sdata;
    $obj->outer;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub getConfig {
    my $log = Log::Log4perl->get_logger("szeng::config::ldap");
    $log->trace("Вызов метода getConfig");
    my $self  = shift;
    my $searchCond = shift;

    my $hash;
    $log->debug("Чтение конфигурационных параметров для ".$searchCond." - ".$self->{searchBase}.",".$BASE_DN);
    
    $self->{mesg} = $self->{ldap}->search( filter=>$searchCond, 
                         base=>$self->{searchBase}.",".$BASE_DN);
    
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
