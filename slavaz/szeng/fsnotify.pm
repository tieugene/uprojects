package szeng::fsnotify;
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
use Data::Dumper::Simple;
use Log::Log4perl;
use szeng::Object;
use szeng::config::ldap;
use szeng::config::file;

use threads;
use threads::shared;
use szeng::serialize;


use vars qw($VERSION @ISA);
@ISA     	= qw(szeng::Object);

$VERSION = "0.0.1";

my $AUDIT_LOG="tail -f -c 0 /var/log/audit/audit.log |";
my $Self;
my $watchThread;

my $timer:shared = 0;
my $shared_Info:shared = '';
my $shared_Info_flag:shared = 0;
# ------------------------------------------------------------------------------------------------------------------------------
sub new {
    my $this = shift;
    my $class = ref($this) || $this;

    my $self = bless { }, $class;
    $self->{parent} = shift;
    my $log = Log::Log4perl->get_logger("szeng::fsnotify");
    $log->trace("Создание объекта FSNOTIFY");
    
    $self->{hooks} = undef;
    $self->{filez} = undef;
    $self;
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
	$self->{confParam} = '(cn=inotsrv)';
    }
}
# ------------------------------------------------------------------------------------------------------------------------------
sub addHook {
    my $self = shift;
    my $path = shift;
    
    if ( $self->checkHook($path)){
	$self->{hooks}{$path} = 1;
	return 1;
    }
    my $log = Log::Log4perl->get_logger("szeng::fsnotify");
    $log->trace("Создание path-хука auditctl : ".$path);
    if (not defined ($self->{hooks}{$path})){
	$self->{hooks}{$path} = 1;
	system ("/sbin/auditctl -a exit,always -F perm=wa -F dir=".$path);
	return 1;
    } else {
	return 0;
    }
}
# ------------------------------------------------------------------------------------------------------------------------------
sub delHook {
    my $self = shift;
    my $path = shift;

    my $log = Log::Log4perl->get_logger("szeng::fsnotify");
    $log->trace("Удаление path-хука auditctl : ".$path);
    if (defined ($self->{hooks}{$path})){
	$self->{hooks}{$path} = undef;
	system ("/sbin/auditctl -d exit,always -F perm=wa -F dir=".$path);
	return 1;
    } else {
	return 0;
    }
}
# ------------------------------------------------------------------------------------------------------------------------------
sub checkHook {
    my $self = shift;
    my $path = shift;
    my $hooks = `/sbin/auditctl -l`;
    return 1 if ($hooks =~ /dir=$path\s+/);
    return 0;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub reInitByConfig{
    my $self = shift;
    my $pluginName;
    $self->{config} = {$self->{conf}->getConfig($self->{confParam})};

    for $pluginName (keys %{$self->{config}->{plugins}}){
	next if ($self->{config}->{plugins}->{$pluginName} ne 1);
	eval ('use szeng::plugins::'.$pluginName);
    }
}
# ------------------------------------------------------------------------------------------------------------------------------
sub mainCycle{
    my $self = shift;
    $Self = $self;
    my $msg_id;
    my $msg_count=-1;
    my $tmp;
    
    my @auditOrig;
    my @msgs;
    my %event;

    $self->getConfig();
    
    $self->reInitByConfig();


    $self->addHook($self->{config}->{main}->{watchPath});

    my $log = Log::Log4perl->get_logger("szeng::fsnotify");
    $log->trace("Запуск основного цикла обработки.");

    $event{audit}{msg_id} = '';
    $event{isInit} = 0;

    $watchThread = threads->create("__CreateWatchThread");

    open(LOG, $AUDIT_LOG);

    while(<LOG>) {
    	my $line = $_; chomp($line);
	
        if ($line =~ /type=SYSCALL msg=audit\((\S+)\): arch=\S+ syscall=(\S+) success=\S+ exit=(\S+) a0=(\S+) a1=(\S+) a2=(\S+) a3=(\S+) items=(\S+)(.*)/){
		
	    $msg_id = $1;
		
	    push @auditOrig, $line;
	    $event{isInit} = 1;

	    $event{audit}{msg_id} = $msg_id;
	    $event{audit}{syscall} = $2;
	    $event{audit}{actionName} = $self->getNameAction($event{audit}{syscall});
	    $event{audit}{exit} = $3; $event{audit}{a0} = $4; $event{audit}{a1} = $5;
	    $event{audit}{a2} = $6; $event{audit}{a3} = $7; $event{audit}{items} = $8;
		
	    $tmp = $9; $tmp =~ /ppid=(\S+) pid=(\S+) auid=(\S+) uid=(\S+) gid=(\S+) euid=(\S+) suid=(\S+) fsuid=(\S+)(.*)/;
	    $event{audit}{ppid} = $1; $event{audit}{pid} = $2; $event{audit}{auid} = $3; $event{audit}{uid} = $4;
	    $event{audit}{gid} = $5; $event{audit}{euid} = $6; $event{audit}{suid} = $7; $event{audit}{fsuid} = $8;

	    $tmp = $9; $tmp =~ /egid=(\S+) sgid=(\S+) fsgid=(\S+) tty=(\S+) ses=(\S+) comm="(\S+)" exe="(\S+)" subj=(\S+)/;
	    $event{audit}{egid} = $1; $event{audit}{sgid} = $2; $event{audit}{fsgid} = $3; $event{audit}{tty} = $4;
	    $event{audit}{ses} = $5; $event{audit}{comm} = $6; $event{audit}{exe} = $7; $event{audit}{subj} = $8;
	    
	    $msg_count = $event{audit}{items};
	    next;
	}
	$tmp = $event{audit}{msg_id};
	my $re = 'type=(\S+) msg=audit\('.$tmp.'\): ';
	if ($line =~  $re){
	    $msg_count--;
	    push @auditOrig, $line;
	    my %msg;
	    
	    $msg{type} = $1;
		

	    if ($msg{type} eq "CWD") {
	        if ($line =~ /type=\S+ msg=audit\(\S+\):\s+cwd="?(\S+(?="))"?/){ #"
		    $msg{cwd} = $1;
		}
		$msg_count++;

	    } elsif ($msg{type} eq "PATH"){
	        if ($line =~ /type=\S+ msg=audit\(\S+\):\s+item=(\S+)\s+name="(.+)"\s+inode=(\S+) dev=(\S+) mode=(\S+) ouid=(\S+) ogid=(\S+) rdev=(\S+) obj=(\S+)/){
		    $msg{item} = $1; $msg{name} = $2; $msg{inode} = $3; $msg{dev} = $4; $msg{mode} = $5; $msg{ouid} = $6; 
		    $msg{ogid} = $7; $msg{rdev} = $8; $msg{obj} = $9;
		}elsif ($line =~ /type=\S+ msg=audit\(\S+\):\s+item=(\S+)\s+name=(.+)\s+inode=(\S+) dev=(\S+) mode=(\S+) ouid=(\S+) ogid=(\S+) rdev=(\S+) obj=(\S+)/){
		    $msg{item} = $1; $msg{name} =$2; $msg{inode} = $3; $msg{dev} = $4; $msg{mode} = $5; $msg{ouid} = $6; 
		    $msg{ogid} = $7; $msg{rdev} = $8; $msg{obj} = $9;
		    if ($msg{name} ne '(null)'){
			$msg{name} = $self->decodeStr($msg{name});
		    }
		}

	    } else {
#	        print "unparsed line: $line\n";
	    }
		push @msgs, \%msg;
	}
        if ($msg_count == 0){
	    my @auditOrig2 = @auditOrig;
	    my @msgs2 = @msgs;
	    $event{auditOrig} = \@auditOrig2;
	    $event{audit}{msgs} = \@msgs2;
	    undef @auditOrig;
	    undef @msgs;
	    $self->processEvent(\%event);
	}

    }
}
# ------------------------------------------------------------------------------------------------------------------------------
sub decodeStr(){
    my $self = shift;
    my $str =  shift;
    my $ret='';
    my $i;
    for ($i=0;$i< length ($str);$i+=2){
        $ret.= chr(hex(substr($str,$i,2)));
    }
    return $ret;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub thisIsNotMyEvent(){
    my $self = shift;
    my $event= shift;
    my @msgs = @{$event->{audit}{msgs}};
    my $baseDir = '';
    my $somePath = '';
    my $path; my $onemsg;

    foreach $onemsg (@msgs) {
	if ( $onemsg->{type} eq 'CWD' ) {
	    $baseDir = $onemsg->{cwd};
	} elsif ($onemsg->{type} eq 'PATH' ) {
	    $somePath = $onemsg->{name};
	}
    }
    return 1 if ((not defined($baseDir)) or ($baseDir eq ''));
    foreach $path (keys(%{$self->{hooks}})){
	return 0 if ($baseDir =~ /^$path.*/);
	return 0 if ($somePath =~ /^$path.*/);
    }
    return 1;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub processEvent(){
    my $self = shift;
    my $event= shift;
    
    # Временно. Оно иногда, суко, не работает из-за этого :(
    my @msgs = @{$event->{audit}{msgs}};
    return if (scalar(@msgs) eq 0);
    
    my $msgOffset=0;
    my $onemsg;
    
    foreach $onemsg (@msgs) {
	if ( $onemsg->{type} ne 'CWD' ) {
	    $msgOffset++;
	} else {
	    last;
	}
	
    }
    return if $self->thisIsNotMyEvent($event);
    
#warn Dumper(@msgs);
    

    if ($event->{audit}{syscall} == 5){
	# изменение файла или каталога
	if ($event->{audit}{items} == 2){
	    return if (! defined($event->{audit}{msgs}->[$msgOffset+2]->{name}) );
	    
#	    $event->{fullPath} = $event->{audit}{msgs}->[$msgOffset]->{cwd}."/".$event->{audit}{msgs}->[$msgOffset+2]->{name};
	    $event->{fullPath} = $event->{audit}{msgs}->[$msgOffset+2]->{name};
	    $event->{actionMyName} = 'create';
	} elsif ($event->{audit}{items} == 1){
	    return if (! defined($event->{audit}{msgs}->[$msgOffset+1]->{name}) );
#	    $event->{fullPath} = $event->{audit}{msgs}->[$msgOffset]->{cwd}."/".$event->{audit}{msgs}->[$msgOffset+1]->{name};
	    $event->{fullPath} = $event->{audit}{msgs}->[$msgOffset+1]->{name};
	    $event->{actionMyName} = 'modify';
	} else {
	    $event->{fullPath} = '';
	    $event->{actionMyName} = 'unknown';
	}
    } elsif ($event->{audit}{syscall} == 85){
	# readlink - шозанах?
	return;
    } elsif (($event->{audit}{syscall} == 301) or ($event->{audit}{syscall} == 10) or ($event->{audit}{syscall} == 278)){
	# unlink
	$event->{fullPath} = $event->{audit}{msgs}->[$msgOffset+2]->{name};
	$event->{actionMyName} = 'unlink';
    } elsif (($event->{audit}{syscall} == 39) or ($event->{audit}{syscall} == 296)){
	# mkdir
	$event->{fullPath} = $event->{audit}{msgs}->[$msgOffset+2]->{name};
	$event->{actionMyName} = 'mkdir';
    } elsif ($event->{audit}{syscall} == 40){
	# rmdir
	$event->{fullPath} = $event->{audit}{msgs}->[$msgOffset+2]->{name};
	$event->{actionMyName} = 'rmdir';
    } else {
	return;
    }
    return if (not defined($event->{fullPath}));

    # эта херня не рассчитана на слежение за несколькими путями... в будущем пофиксю, сейчас нах не нужно.
    foreach $onemsg (keys(%{$self->{hooks}})){
	if ( not ($event->{fullPath} =~ /^$onemsg.*/  )){
	    $event->{fullPath} = $event->{audit}{msgs}->[$msgOffset]->{cwd}."/".$event->{fullPath};
	}
    }
    my %event2 = %$event;
    my %event3 = %{$event->{audit}};
    $event2{audit} = \%event3;
    { 
	lock $shared_Info_flag;
	if ($shared_Info_flag eq 1){
	    $self->{filez} = undef;
	}
	$shared_Info_flag = 2;
    }
    $self->{filez}->{$event->{fullPath}} = \%event2;
    
    
	{
	 lock $timer;
	 $timer = 0;
	 $shared_Info = serialize($self->{filez});
	}
    
    
}
# ------------------------------------------------------------------------------------------------------------------------------
sub __CreateWatchThread{

    my $pluginName;
    while (1){
        while ($timer lt $Self->{config}->{main}->{waitBeforeNotify}){
print "tick\n";
	    {
	     lock $timer;
	     $timer++;
	    }
	    sleep 1;
	}

	{ 
	    lock $shared_Info_flag;
	    if ($shared_Info_flag ne 2) {
		{ lock $timer; $timer = 0; }
		next;
	    }
	
    	    $shared_Info_flag = 1;
    	    my $data = unserialize($shared_Info);
        
	    for $pluginName (keys %{$Self->{config}->{plugins}}){
		next if ($Self->{config}->{plugins}->{$pluginName} ne 1);
		eval ('async{ szeng::plugins::'.$pluginName.'->startPlugin($Self->{config}, $data); } ');
    	    }
#print "\n".$shared_Info."\n\n";
#szeng::plugins::slavaz_send_msg->startPlugin($Self->{config}, $data);


	}
	{ lock $timer; $timer = 0; }
    }
}

# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
sub getNameAction{
        my $self = shift;
        my $syscall = shift;

        if ($syscall == 0)        { return '__NR_restart_syscall';}
        elsif ($syscall == 1)     { return '__NR_exit';}
        elsif ($syscall == 2)     { return '__NR_fork';}
        elsif ($syscall == 3)     { return '__NR_read';}
        elsif ($syscall == 4)     { return '__NR_write';}
        elsif ($syscall == 5)     { return '__NR_open';}
	elsif ($syscall == 6)     { return '__NR_close';}
	elsif ($syscall == 7)     { return '__NR_waitpid';}
	elsif ($syscall == 8)     { return '__NR_creat';}
	elsif ($syscall == 9)     { return '__NR_link';}
	elsif ($syscall == 10)    { return '__NR_unlink';}
	elsif ($syscall == 11)    { return '__NR_execve';}
	elsif ($syscall == 12)    { return '__NR_chdir';}
	elsif ($syscall == 13)    { return '__NR_time';}
	elsif ($syscall == 14)    { return '__NR_mknod';}
	elsif ($syscall == 15)    { return '__NR_chmod';}
	elsif ($syscall == 16)    { return '__NR_lchown';}
	elsif ($syscall == 17)    { return '__NR_break';}
	elsif ($syscall == 18)    { return '__NR_oldstat';}
	elsif ($syscall == 19)    { return '__NR_lseek';}
	elsif ($syscall == 20)    { return '__NR_getpid';}
	elsif ($syscall == 21)    { return '__NR_mount';}
	elsif ($syscall == 22)    { return '__NR_umount';}
	elsif ($syscall == 23)    { return '__NR_setuid';}
	elsif ($syscall == 24)    { return '__NR_getuid';}
	elsif ($syscall == 25)    { return '__NR_stime';}
	elsif ($syscall == 26)    { return '__NR_ptrace';}
	elsif ($syscall == 27)    { return '__NR_alarm';}
	elsif ($syscall == 28)    { return '__NR_oldfstat';}
	elsif ($syscall == 29)    { return '__NR_pause';}
	elsif ($syscall == 30)    { return '__NR_utime';}
	elsif ($syscall == 31)    { return '__NR_stty';}
	elsif ($syscall == 32)    { return '__NR_gtty';}
	elsif ($syscall == 33)    { return '__NR_access';}
	elsif ($syscall == 34)    { return '__NR_nice';}
	elsif ($syscall == 35)    { return '__NR_ftime';}
	elsif ($syscall == 36)    { return '__NR_sync';}
	elsif ($syscall == 37)    { return '__NR_kill';}
	elsif ($syscall == 38)    { return '__NR_rename';}
	elsif ($syscall == 39)    { return '__NR_mkdir';}
	elsif ($syscall == 40)    { return '__NR_rmdir';}
	elsif ($syscall == 41)    { return '__NR_dup';}
	elsif ($syscall == 42)    { return '__NR_pipe';}
	elsif ($syscall == 43)    { return '__NR_times';}
	elsif ($syscall == 44)    { return '__NR_prof';}
	elsif ($syscall == 45)    { return '__NR_brk';}
	elsif ($syscall == 46)    { return '__NR_setgid';}
	elsif ($syscall == 47)    { return '__NR_getgid';}
	elsif ($syscall == 48)    { return '__NR_signal';}
	elsif ($syscall == 49)    { return '__NR_geteuid';}
	elsif ($syscall == 50)    { return '__NR_getegid';}
	elsif ($syscall == 51)    { return '__NR_acct';}
	elsif ($syscall == 52)    { return '__NR_umount2';}
	elsif ($syscall == 53)    { return '__NR_lock';}
	elsif ($syscall == 54)    { return '__NR_ioctl';}
	elsif ($syscall == 55)    { return '__NR_fcntl';}
	elsif ($syscall == 56)    { return '__NR_mpx';}
	elsif ($syscall == 57)    { return '__NR_setpgid';}
	elsif ($syscall == 58)    { return '__NR_ulimit';}
	elsif ($syscall == 59)    { return '__NR_oldolduname';}
	elsif ($syscall == 60)    { return '__NR_umask';}
	elsif ($syscall == 61)    { return '__NR_chroot';}
	elsif ($syscall == 62)    { return '__NR_ustat';}
	elsif ($syscall == 63)    { return '__NR_dup2';}
	elsif ($syscall == 64)    { return '__NR_getppid';}
	elsif ($syscall == 65)    { return '__NR_getpgrp';}
	elsif ($syscall == 66)    { return '__NR_setsid';}
	elsif ($syscall == 67)    { return '__NR_sigaction';}
	elsif ($syscall == 68)    { return '__NR_sgetmask';}
	elsif ($syscall == 69)    { return '__NR_ssetmask';}
	elsif ($syscall == 70)    { return '__NR_setreuid';}
	elsif ($syscall == 71)    { return '__NR_setregid';}
	elsif ($syscall == 72)    { return '__NR_sigsuspend';}
	elsif ($syscall == 73)    { return '__NR_sigpending';}
	elsif ($syscall == 74)    { return '__NR_sethostname';}
	elsif ($syscall == 75)    { return '__NR_setrlimit';}
	elsif ($syscall == 76)    { return '__NR_getrlimit';}
	elsif ($syscall == 77)    { return '__NR_getrusage';}
	elsif ($syscall == 78)    { return '__NR_gettimeofday';}
	elsif ($syscall == 79)    { return '__NR_settimeofday';}
	elsif ($syscall == 80)    { return '__NR_getgroups';}
	elsif ($syscall == 81)    { return '__NR_setgroups';}
	elsif ($syscall == 82)    { return '__NR_select';}
	elsif ($syscall == 83)    { return '__NR_symlink';}
	elsif ($syscall == 84)    { return '__NR_oldlstat';}
	elsif ($syscall == 85)    { return '__NR_readlink';}
	elsif ($syscall == 86)    { return '__NR_uselib';}
	elsif ($syscall == 87)    { return '__NR_swapon';}
	elsif ($syscall == 88)    { return '__NR_reboot';}
	elsif ($syscall == 89)    { return '__NR_readdir';}
	elsif ($syscall == 90)    { return '__NR_mmap';}
	elsif ($syscall == 91)    { return '__NR_munmap';}
	elsif ($syscall == 92)    { return '__NR_truncate';}
	elsif ($syscall == 93)    { return '__NR_ftruncate';}
	elsif ($syscall == 94)    { return '__NR_fchmod';}
	elsif ($syscall == 95)    { return '__NR_fchown';}
	elsif ($syscall == 96)    { return '__NR_getpriority';}
	elsif ($syscall == 97)    { return '__NR_setpriority';}
	elsif ($syscall == 98)    { return '__NR_profil';}
	elsif ($syscall == 99)    { return '__NR_statfs';}
	elsif ($syscall == 100)   { return '__NR_fstatfs';}
	elsif ($syscall == 101)   { return '__NR_ioperm';}
	elsif ($syscall == 102)   { return '__NR_socketcall';}
	elsif ($syscall == 103)   { return '__NR_syslog';}
	elsif ($syscall == 104)   { return '__NR_setitimer';}
	elsif ($syscall == 105)   { return '__NR_getitimer';}
	elsif ($syscall == 106)   { return '__NR_stat';}
	elsif ($syscall == 107)   { return '__NR_lstat';}
	elsif ($syscall == 108)   { return '__NR_fstat';}
	elsif ($syscall == 109)   { return '__NR_olduname';}
	elsif ($syscall == 110)   { return '__NR_iopl';}
	elsif ($syscall == 111)   { return '__NR_vhangup';}
	elsif ($syscall == 112)   { return '__NR_idle';}
	elsif ($syscall == 113)   { return '__NR_vm86old';}
	elsif ($syscall == 114)   { return '__NR_wait4';}
	elsif ($syscall == 115)   { return '__NR_swapoff';}
	elsif ($syscall == 116)   { return '__NR_sysinfo';}
	elsif ($syscall == 117)   { return '__NR_ipc';}
	elsif ($syscall == 118)   { return '__NR_fsync';}
	elsif ($syscall == 119)   { return '__NR_sigreturn';}
	elsif ($syscall == 120)   { return '__NR_clone';}
	elsif ($syscall == 121)   { return '__NR_setdomainname';}
	elsif ($syscall == 122)   { return '__NR_uname';}
	elsif ($syscall == 123)   { return '__NR_modify_ldt';}
	elsif ($syscall == 124)   { return '__NR_adjtimex';}
	elsif ($syscall == 125)   { return '__NR_mprotect';}
	elsif ($syscall == 126)   { return '__NR_sigprocmask';}
	elsif ($syscall == 127)   { return '__NR_create_module';}
	elsif ($syscall == 128)   { return '__NR_init_module';}
	elsif ($syscall == 129)   { return '__NR_delete_module';}
	elsif ($syscall == 130)   { return '__NR_get_kernel_syms';}
	elsif ($syscall == 131)   { return '__NR_quotactl';}
	elsif ($syscall == 132)   { return '__NR_getpgid';}
	elsif ($syscall == 133)   { return '__NR_fchdir';}
	elsif ($syscall == 134)   { return '__NR_bdflush';}
	elsif ($syscall == 135)   { return '__NR_sysfs';}
	elsif ($syscall == 136)   { return '__NR_personality';}
	elsif ($syscall == 137)   { return '__NR_afs_syscall';}
	elsif ($syscall == 138)   { return '__NR_setfsuid';}
	elsif ($syscall == 139)   { return '__NR_setfsgid';}
	elsif ($syscall == 140)   { return '__NR__llseek';}
	elsif ($syscall == 141)   { return '__NR_getdents';}
	elsif ($syscall == 142)   { return '__NR__newselect';}
	elsif ($syscall == 143)   { return '__NR_flock';}
	elsif ($syscall == 144)   { return '__NR_msync';}
	elsif ($syscall == 145)   { return '__NR_readv';}
	elsif ($syscall == 146)   { return '__NR_writev';}
	elsif ($syscall == 147)   { return '__NR_getsid';}
	elsif ($syscall == 148)   { return '__NR_fdatasync';}
	elsif ($syscall == 149)   { return '__NR__sysctl';}
	elsif ($syscall == 150)   { return '__NR_mlock';}
	elsif ($syscall == 151)   { return '__NR_munlock';}
	elsif ($syscall == 152)   { return '__NR_mlockall';}
	elsif ($syscall == 153)   { return '__NR_munlockall';}
	elsif ($syscall == 154)   { return '__NR_sched_setparam';}
	elsif ($syscall == 155)   { return '__NR_sched_getparam';}
	elsif ($syscall == 156)   { return '__NR_sched_setscheduler';}
	elsif ($syscall == 157)   { return '__NR_sched_getscheduler';}
	elsif ($syscall == 158)   { return '__NR_sched_yield';}
	elsif ($syscall == 159)   { return '__NR_sched_get_priority_max';}
	elsif ($syscall == 160)   { return '__NR_sched_get_priority_min';}
	elsif ($syscall == 161)   { return '__NR_sched_rr_get_interval';}
	elsif ($syscall == 162)   { return '__NR_nanosleep';}
	elsif ($syscall == 163)   { return '__NR_mremap';}
	elsif ($syscall == 164)   { return '__NR_setresuid';}
	elsif ($syscall == 165)   { return '__NR_getresuid';}
	elsif ($syscall == 166)   { return '__NR_vm86';}
	elsif ($syscall == 167)   { return '__NR_query_module';}
	elsif ($syscall == 168)   { return '__NR_poll';}
	elsif ($syscall == 169)   { return '__NR_nfsservctl';}
	elsif ($syscall == 170)   { return '__NR_setresgid';}
	elsif ($syscall == 171)   { return '__NR_getresgid';}
	elsif ($syscall == 172)   { return '__NR_prctl';}
	elsif ($syscall == 173)   { return '__NR_rt_sigreturn';}
	elsif ($syscall == 174)   { return '__NR_rt_sigaction';}
	elsif ($syscall == 175)   { return '__NR_rt_sigprocmask';}
	elsif ($syscall == 176)   { return '__NR_rt_sigpending';}
	elsif ($syscall == 177)   { return '__NR_rt_sigtimedwait';}
	elsif ($syscall == 178)   { return '__NR_rt_sigqueueinfo';}
	elsif ($syscall == 179)   { return '__NR_rt_sigsuspend';}
	elsif ($syscall == 180)   { return '__NR_pread64';}
	elsif ($syscall == 181)   { return '__NR_pwrite64';}
	elsif ($syscall == 182)   { return '__NR_chown';}
	elsif ($syscall == 183)   { return '__NR_getcwd';}
	elsif ($syscall == 184)   { return '__NR_capget';}
	elsif ($syscall == 185)   { return '__NR_capset';}
	elsif ($syscall == 186)   { return '__NR_sigaltstack';}
	elsif ($syscall == 187)   { return '__NR_sendfile';}
	elsif ($syscall == 188)   { return '__NR_getpmsg';}
	elsif ($syscall == 189)   { return '__NR_putpmsg';}
	elsif ($syscall == 190)   { return '__NR_vfork';}
	elsif ($syscall == 191)   { return '__NR_ugetrlimit';}
	elsif ($syscall == 192)   { return '__NR_mmap2';}
	elsif ($syscall == 193)   { return '__NR_truncate64';}
	elsif ($syscall == 194)   { return '__NR_ftruncate64';}
	elsif ($syscall == 195)   { return '__NR_stat64';}
	elsif ($syscall == 196)   { return '__NR_lstat64';}
	elsif ($syscall == 197)   { return '__NR_fstat64';}
	elsif ($syscall == 198)   { return '__NR_lchown32';}
	elsif ($syscall == 199)   { return '__NR_getuid32';}
	elsif ($syscall == 200)   { return '__NR_getgid32';}
	elsif ($syscall == 201)   { return '__NR_geteuid32';}
	elsif ($syscall == 202)   { return '__NR_getegid32';}
	elsif ($syscall == 203)   { return '__NR_setreuid32';}
	elsif ($syscall == 204)   { return '__NR_setregid32';}
	elsif ($syscall == 205)   { return '__NR_getgroups32';}
	elsif ($syscall == 206)   { return '__NR_setgroups32';}
	elsif ($syscall == 207)   { return '__NR_fchown32';}
	elsif ($syscall == 208)   { return '__NR_setresuid32';}
	elsif ($syscall == 209)   { return '__NR_getresuid32';}
	elsif ($syscall == 210)   { return '__NR_setresgid32';}
	elsif ($syscall == 211)   { return '__NR_getresgid32';}
	elsif ($syscall == 212)   { return '__NR_chown32';}
	elsif ($syscall == 213)   { return '__NR_setuid32';}
	elsif ($syscall == 214)   { return '__NR_setgid32';}
	elsif ($syscall == 215)   { return '__NR_setfsuid32';}
	elsif ($syscall == 216)   { return '__NR_setfsgid32';}
	elsif ($syscall == 217)   { return '__NR_pivot_root';}
	elsif ($syscall == 218)   { return '__NR_mincore';}
	elsif ($syscall == 219)   { return '__NR_madvise';}
	elsif ($syscall == 219)   { return '__NR_madvise1';}
	elsif ($syscall == 220)   { return '__NR_getdents64';}
	elsif ($syscall == 221)   { return '__NR_fcntl64';}
	elsif ($syscall == 224)   { return '__NR_gettid';}
	elsif ($syscall == 225)   { return '__NR_readahead';}
	elsif ($syscall == 226)   { return '__NR_setxattr';}
	elsif ($syscall == 227)   { return '__NR_lsetxattr';}
	elsif ($syscall == 228)   { return '__NR_fsetxattr';}
	elsif ($syscall == 229)   { return '__NR_getxattr';}
	elsif ($syscall == 230)   { return '__NR_lgetxattr';}
	elsif ($syscall == 231)   { return '__NR_fgetxattr';}
	elsif ($syscall == 232)   { return '__NR_listxattr';}
	elsif ($syscall == 233)   { return '__NR_llistxattr';}
	elsif ($syscall == 234)   { return '__NR_flistxattr';}
	elsif ($syscall == 235)   { return '__NR_removexattr';}
	elsif ($syscall == 236)   { return '__NR_lremovexattr';}
	elsif ($syscall == 237)   { return '__NR_fremovexattr';}
	elsif ($syscall == 238)   { return '__NR_tkill';}
	elsif ($syscall == 239)   { return '__NR_sendfile64';}
	elsif ($syscall == 240)   { return '__NR_futex';}
	elsif ($syscall == 241)   { return '__NR_sched_setaffinity';}
	elsif ($syscall == 242)   { return '__NR_sched_getaffinity';}
	elsif ($syscall == 243)   { return '__NR_set_thread_area';}
	elsif ($syscall == 244)   { return '__NR_get_thread_area';}
	elsif ($syscall == 245)   { return '__NR_io_setup';}
	elsif ($syscall == 246)   { return '__NR_io_destroy';}
	elsif ($syscall == 247)   { return '__NR_io_getevents';}
	elsif ($syscall == 248)   { return '__NR_io_submit';}
	elsif ($syscall == 249)   { return '__NR_io_cancel';}
	elsif ($syscall == 250)   { return '__NR_fadvise64';}
	elsif ($syscall == 252)   { return '__NR_exit_group';}
	elsif ($syscall == 253)   { return '__NR_lookup_dcookie';}
	elsif ($syscall == 254)   { return '__NR_epoll_create';}
	elsif ($syscall == 255)   { return '__NR_epoll_ctl';}
	elsif ($syscall == 256)   { return '__NR_epoll_wait';}
	elsif ($syscall == 257)   { return '__NR_remap_file_pages';}
	elsif ($syscall == 258)   { return '__NR_set_tid_address';}
	elsif ($syscall == 259)   { return '__NR_timer_create';}
	elsif ($syscall == 260)   { return '__NR_timer_settime';}
	elsif ($syscall == 261)   { return '__NR_timer_gettime';}
	elsif ($syscall == 262)   { return '__NR_timer_getoverrun';}
	elsif ($syscall == 263)   { return '__NR_timer_delete';}
	elsif ($syscall == 264)   { return '__NR_clock_settime';}
	elsif ($syscall == 265)   { return '__NR_clock_gettime';}
	elsif ($syscall == 266)   { return '__NR_clock_getres';}
	elsif ($syscall == 267)   { return '__NR_clock_nanosleep';}
	elsif ($syscall == 268)   { return '__NR_statfs64';}
	elsif ($syscall == 269)   { return '__NR_fstatfs64';}
	elsif ($syscall == 270)   { return '__NR_tgkill';}
	elsif ($syscall == 271)   { return '__NR_utimes';}
	elsif ($syscall == 272)   { return '__NR_fadvise64_64';}
	elsif ($syscall == 273)   { return '__NR_vserver';}
	elsif ($syscall == 274)   { return '__NR_mbind';}
	elsif ($syscall == 275)   { return '__NR_get_mempolicy';}
	elsif ($syscall == 276)   { return '__NR_set_mempolicy';}
	elsif ($syscall == 277)   { return '__NR_mq_open';}
	elsif ($syscall == 278)   { return '__NR_mq_unlink';}
	elsif ($syscall == 279)   { return '__NR_mq_timedsend';}
	elsif ($syscall == 280)   { return '__NR_mq_timedreceive';}
	elsif ($syscall == 281)   { return '__NR_mq_notify';}
	elsif ($syscall == 282)   { return '__NR_mq_getsetattr';}
	elsif ($syscall == 283)   { return '__NR_kexec_load';}
	elsif ($syscall == 284)   { return '__NR_waitid';}
	elsif ($syscall == 286)   { return '__NR_add_key';}
	elsif ($syscall == 287)   { return '__NR_request_key';}
	elsif ($syscall == 288)   { return '__NR_keyctl';}
	elsif ($syscall == 289)   { return '__NR_ioprio_set';}
	elsif ($syscall == 290)   { return '__NR_ioprio_get';}
	elsif ($syscall == 291)   { return '__NR_inotify_init';}
	elsif ($syscall == 292)   { return '__NR_inotify_add_watch';}
	elsif ($syscall == 293)   { return '__NR_inotify_rm_watch';}
	elsif ($syscall == 294)   { return '__NR_migrate_pages';}
	elsif ($syscall == 295)   { return '__NR_openat';}
	elsif ($syscall == 296)   { return '__NR_mkdirat';}
	elsif ($syscall == 297)   { return '__NR_mknodat';}
	elsif ($syscall == 298)   { return '__NR_fchownat';}
	elsif ($syscall == 299)   { return '__NR_futimesat';}
	elsif ($syscall == 300)   { return '__NR_fstatat64';}
	elsif ($syscall == 301)   { return '__NR_unlinkat';}
	elsif ($syscall == 302)   { return '__NR_renameat';}
	elsif ($syscall == 303)   { return '__NR_linkat';}
	elsif ($syscall == 304)   { return '__NR_symlinkat';}
	elsif ($syscall == 305)   { return '__NR_readlinkat';}
	elsif ($syscall == 306)   { return '__NR_fchmodat';}
	elsif ($syscall == 307)   { return '__NR_faccessat';}
	elsif ($syscall == 308)   { return '__NR_pselect6';}
	elsif ($syscall == 309)   { return '__NR_ppoll';}
	elsif ($syscall == 310)   { return '__NR_unshare';}
	elsif ($syscall == 311)   { return '__NR_set_robust_list';}
	elsif ($syscall == 312)   { return '__NR_get_robust_list';}
	elsif ($syscall == 313)   { return '__NR_splice';}
	elsif ($syscall == 314)   { return '__NR_sync_file_range';}
	elsif ($syscall == 315)   { return '__NR_tee';}
	elsif ($syscall == 316)   { return '__NR_vmsplice';}
	elsif ($syscall == 317)   { return '__NR_move_pages';}
	elsif ($syscall == 318)   { return '__NR_getcpu';}
	elsif ($syscall == 319)   { return '__NR_epoll_pwait';}
	elsif ($syscall == 320)   { return '__NR_utimensat';}
	elsif ($syscall == 321)   { return '__NR_signalfd';}
	elsif ($syscall == 322)   { return '__NR_timerfd_create';}
	elsif ($syscall == 323)   { return '__NR_eventfd';}
	elsif ($syscall == 324)   { return '__NR_fallocate';}
	elsif ($syscall == 325)   { return '__NR_timerfd_settime';}
	elsif ($syscall == 326)   { return '__NR_timerfd_gettime';}
	else 			  { return 'ACTION_UNKNOWN'; }
}

1;
