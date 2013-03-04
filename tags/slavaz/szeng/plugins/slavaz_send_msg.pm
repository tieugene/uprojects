package szeng::plugins::slavaz_send_msg;
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
use warnings;
use vars qw($VERSION);
$VERSION = "0.0.1";

use Log::Log4perl;
use Socket;
use POSIX;
use Data::Dumper::Simple;

my $ConfigObject = undef;
my $mainSocket;

# ------------------------------------------------------------------------------------------------------------------------------
sub startPlugin{
    my $self = shift;
    my $config = shift;
    my $events = shift;
    my $fileName;
    
    my %users;
    
    
    foreach $fileName (keys(%{$events})){
        my $action = $events->{$fileName}->{actionMyName};
        my $user = getpwuid($events->{$fileName}->{audit}->{uid});

        my $userDir = $fileName;
        my $bdir = $config->{main}->{watchPath};
        $userDir =~ s/$bdir//g;
        $userDir =~ s/^\/([^\/]+).*/$1/;
        
        if (not defined($users{$userDir})){
    	    my $tempConf = $self->getInotsrvUserConfig($config, $userDir);
    	    next if ((not defined $tempConf) or ($tempConf eq '') or (not defined $tempConf->{main}));
    	    next if (not $tempConf->{main}->{enabled});
    	    $users{$userDir}{userInotsrvConfig} = $tempConf;
    	    $users{$userDir}{userConfig} = $self->getUserConfig($config, $userDir);
        }
	push @{$users{$userDir}{$events->{$fileName}->{actionMyName}}}, $fileName;
    }
    my $userName;
    my $msg_body='';
    foreach $userName (keys(%users)){
	$self->SendMessageToUser($config,$config->{slavaz_send_msg}, $users{$userName});
    }
    
    
    
#warn Dumper(%users);
    
    return 1;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub SendMessageToUser(){
    my $self = shift;
    my $config = shift;
    my $pluginConfig = shift;
    my $userInfo = shift;
    
    my $body='';
    my $body2=$pluginConfig->{msg_body_main}."\n\n";
    my @tmp;
    my $tmp1;

    $tmp1 = $userInfo->{userInotsrvConfig}->{dir};
    
    if (($userInfo->{userInotsrvConfig}->{dir}->{delete} ne 0) 
	and (defined ($userInfo->{rmdir}))){
	
	$body.="Удалены каталоги :"."\n";
	foreach $tmp1 (@{$userInfo->{rmdir}}){
	    $tmp1 =~ s/^$config->{main}->{watchPath}\///g;
	    $body .=$tmp1."\n";
	}
	$body.="\n";
    }

    if (($userInfo->{userInotsrvConfig}->{dir}->{create} ne 0) 
	and (defined ($userInfo->{mkdir}))){
	
	$body.="Созданны каталоги :"."\n";
	foreach $tmp1 (@{$userInfo->{mkdir}}){
	    $tmp1 =~ s/^$config->{main}->{watchPath}\///g;
	    $body .=$tmp1."\n";
	}
	$body.="\n";
    }

    if (($userInfo->{userInotsrvConfig}->{file}->{delete} ne 0) 
	and (defined ($userInfo->{unlink}))){
	
	$body.="Удалены файлы :"."\n";
	foreach $tmp1 (@{$userInfo->{unlink}}){
	    $tmp1 =~ s/^$config->{main}->{watchPath}\///g;
	    $body .=$tmp1."\n";
	}
	$body.="\n";
    }

    if (($userInfo->{userInotsrvConfig}->{file}->{create} ne 0) 
	and (defined ($userInfo->{create}))){
	
	$body.="Созданы файлы :"."\n";
	foreach $tmp1 (@{$userInfo->{create}}){
	    $tmp1 =~ s/^$config->{main}->{watchPath}\///g;
	    $body .=$tmp1."\n";
	}
	$body.="\n";
    }

    if (($userInfo->{userInotsrvConfig}->{file}->{modify} ne 0) 
	and (defined ($userInfo->{modify}))){
	
	$body.="Созданы файлы :"."\n";
	foreach $tmp1 (@{$userInfo->{modify}}){
	    $tmp1 =~ s/^$config->{main}->{watchPath}\///g;
	    $body .=$tmp1."\n";
	}
	$body.="\n";
    }
    return 0 if ($body =~ /^$/);
    $body = $body2.$body;

    
#warn Dumper($body);
    $self->openSocket($pluginConfig->{host},$pluginConfig->{port}) or return 0;
    if (($userInfo->{userInotsrvConfig}->{contact}->{icq} ne '0') 
	and (defined($userInfo->{userConfig}->{icquin}))
	and ($userInfo->{userConfig}->{icquin} ne 'x')){

	foreach $tmp1 (@{$userInfo->{userConfig}->{icquin}}){
	    send ($mainSocket, "icq ".$tmp1."\n", 0);
	    $self->processAnswerFromServer() or return 0;
	}

    }
    if (($userInfo->{userInotsrvConfig}->{contact}->{jabber} ne '0') 
	and (defined($userInfo->{userConfig}->{jabberid}))
	and ($userInfo->{userConfig}->{jabberid} ne 'x')){
	foreach $tmp1 (@{$userInfo->{userConfig}->{jabberid}}){
	    send ($mainSocket, "jabber ".$tmp1."\n", 0);
	    $self->processAnswerFromServer() or return 0;
	}
    }
    
    if (($userInfo->{userInotsrvConfig}->{contact}->{email} ne '0') 
	and (defined($userInfo->{userConfig}->{mail}))
	and ($userInfo->{userConfig}->{mail} ne 'x')){

	foreach $tmp1 (@{$userInfo->{userConfig}->{mail}}){
	    send ($mainSocket, "email ".$tmp1."\n", 0);
	    $self->processAnswerFromServer() or return 0;
	}
    }

    @tmp = split /\n/ , $pluginConfig->{msg_header};
    foreach $tmp1 (@tmp){
	send ($mainSocket, "subject ".$tmp1."\n", 0);
	$self->processAnswerFromServer() or return 0;
    }

    @tmp = split /\n/ , $body;
    foreach $tmp1 (@tmp){
	send ($mainSocket, "body ".$tmp1."\n", 0);
	$self->processAnswerFromServer() or return 0;
    }
    send ($mainSocket, "send"."\n", 0);
    $self->processAnswerFromServer() or return 0;
    send ($mainSocket, "quit"."\n", 0);
    $self->processAnswerFromServer() or return 0;
    
    close($mainSocket);

    return 1;
    
}
# ------------------------------------------------------------------------------------------------------------------------------
sub processAnswerFromServer(){
    my $self = shift;
    my $answer;
    $answer = <$mainSocket>;
    $answer =~ s/[\n\r]//g;
    return 1 if ($answer eq "ok");
    send ($mainSocket, "abort"."\n", 0);
    send ($mainSocket, "quit"."\n", 0);
    close($mainSocket);
    return 0;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub openSocket(){
    my $self = shift;
    my $host = shift;
    my $port = shift;

    my $proto  = getprotobyname('tcp') or return 0;
    socket($mainSocket, PF_INET, SOCK_STREAM, $proto) or return 0;
    setsockopt($mainSocket, SOL_SOCKET, SO_REUSEADDR, pack("l", 1)) or return 0;
    my $hst = inet_aton($host);
    connect($mainSocket,sockaddr_in($port, $hst)) or return 0;
    
    return 1;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub getUserConfig{
    my $self = shift;
    my $config = shift;
    my $userName = shift;
    
    
    if (defined($config->{slavaz_send_msg}->{users_conf})){
	die("\nNOT IMPLEMENTED: reading conf params from file!!!\n");
    } else {
	if (not defined($ConfigObject)){
	    $ConfigObject = szeng::config::ldap->new("ou=People");
	}
	return {$ConfigObject->search('(&(uid='.$userName.')(objectclass=flgamesMessenger))')};
    }
}
# ------------------------------------------------------------------------------------------------------------------------------
sub getInotsrvUserConfig{
    my $self = shift;
    my $config = shift;
    my $userName = shift;
    
    if (defined($config->{slavaz_send_msg}->{users_conf})){
	die("\nNOT IMPLEMENTED: reading conf params from file!!!\n");
    } else {
	if (not defined($ConfigObject)){
	    $ConfigObject = szeng::config::ldap->new("ou=People");
	    $ConfigObject->{searchBaseOrig} = $ConfigObject->{searchBase};
	}
	$ConfigObject->{searchBase} = 'uid='.$userName.','.$ConfigObject->{searchBaseOrig};
	return {$ConfigObject->getConfig('(cn=inotsrv)')};
    }
}
# ------------------------------------------------------------------------------------------------------------------------------


1;
