| <[DHCP](Inst_S_LDAP_DHCP.md) | [TOC](TOC.md) | [IMAP/POP3](Inst_S_LDAP_IMAP_POP3.md)> |
|:-----------------------------|:--------------|:---------------------------------------|

# SMB #

## Ingridients ##

### Links: ###

  * [One](http://forum.ubuntu.ru/index.php?topic=10440.msg82533)
  * [Two](http://www.unixdoc.ru/index.php?mode=2&podmode=1&arcicle_id=73)
  * [Three](http://gentoo-wiki.com/HOWTO_LDAP_SAMBA_PDC_Basic_Evaluation)

### Packages: ###

  * samba
  * smbldap-tools

### Configs: ###

  * /etc/openldap/schema/samba.schema
  * /etc/openldap/slabd.conf
  * /etc/samba/smb.conf
  * /etc/smbldap-tools/smbldap.conf
  * /etc/smbldap-tools/smbldap-bind.conf

## Setting up ##

  * cp /usr/share/doc/samba-3.0.28/LDAP/samba.schema /etc/openldap/schema
  * /usr/sbin/smbldap-useradd:
```
--- smbldap-useradd.orig	2007-09-17 15:05:48.000000000 +0400
+++ smbldap-useradd	2009-06-03 14:15:55.000000000 +0400
@@ -295,3 +295,3 @@
 					    changes => [
-							replace => [objectClass => ['top', 'person', 'organizationalPerson', 'inetOrgPerson', 'posixAccount', 'sambaSAMAccount']],
+							replace => [objectClass => ['top', 'account', 'posixAccount', 'sambaSAMAccount']],
 							add => [sambaLogonTime => '0'],
```
  * /etc/openldap/slapd.conf:
```
include	/etc/openldap/schema/samba.schema	# samba
...
access to attrs=userPassword,sambaNTPassword,sambaLMPassword 
	by self write
	by anonymous auth (read?)
	by * none
...
index	sambaSID			eq
index	sambaPrimaryGroupSID		eq
index	sambaDomainName			eq
```
  * net getlocalsid:
> > `SID for domain SERVER is: S-1-5-21-4061505246-3962981041-503675144`
  * /etc/smbldap-tools/smbldap-bind.conf:
```
slaveDN="cn=odmin,dc=ldap"
slavePw="secred"
masterDN="cn=odmin,dc=ldap"
masterPw="secred"
```
  * /etc/smbldap-tools/smbldap.conf:
```
SID="S-1-5-21-4061505246-3962981041-503675144"
sambaDomain="WINDOMAIN"
...
suffix="dc=ldap"
usersdn="ou=Users,${suffix}"
computersdn="ou=Hosts,${suffix}"
groupsdn="ou=Groups,${suffix}"
idmapdn="ou=Idmap,${suffix}"
...
userHome="/mnt/shares/home/%U"
...
defaultUserGid="513"
...
userSmbHome="\\SERVER\%U"		```````
userProfile="\\SERVER\profiles\%U"
userHomeDrive="X:"
...
mailDomain="example.com"
```
> > or as diff:
```
--- smbldap.conf.orig   2007-10-09 13:39:01.000000000 +0400
+++ smbldap.conf        2009-06-03 14:27:31.000000000 +0400
@@ -36,3 +36,3 @@
 # If not defined, parameter is taking from "net getlocalsid" return
-#SID="S-1-5-21-2252255531-4061614174-2474224977"
+SID="S-1-5-21-2125498881-1583495715-1916865485"
 
@@ -41,3 +41,3 @@
 # Ex: sambaDomain="IDEALX-NT"
-#sambaDomain="DOMSMB"
+sambaDomain="MOOZHS"
 
@@ -99,3 +99,3 @@
 # Ex: suffix=dc=IDEALX,dc=ORG
-suffix="dc=company,dc=com"
+suffix="dc=ldap"
 
@@ -104,3 +104,3 @@
 # Warning: if 'suffix' is not set here, you must set the full dn for usersdn
-usersdn="ou=People,${suffix}"
+usersdn="ou=Users,${suffix}"
 
@@ -109,3 +109,3 @@
 # Warning: if 'suffix' is not set here, you must set the full dn for computersdn
-computersdn="ou=Computers,${suffix}"
+computersdn="ou=Hosts,${suffix}"
 
@@ -114,3 +114,3 @@
 # Warning: if 'suffix' is not set here, you must set the full dn for groupsdn
-groupsdn="ou=Group,${suffix}"
+groupsdn="ou=Groups,${suffix}"
 
@@ -151,3 +151,3 @@
 # Ex: userHome="/home/%U"
-userHome="/home/%U"
+userHome="/mnt/shares/home/%U"
 
@@ -183,3 +183,3 @@
 # Ex: userSmbHome="\\PDC-SMB3\%U"
-userSmbHome="\\PDC-SRV\%U"
+userSmbHome="\\SERVER\%U"
 
@@ -189,3 +189,3 @@
 # Ex: userProfile="\\PDC-SMB3\profiles\%U"
-userProfile="\\PDC-SRV\profiles\%U"
+userProfile="\\SERVER\profiles\%U"
```
  * Lets go:
> > `smbldap-populate`
  * Make our default group samba-cpbl:
> > `smbldap-groupmod -a group00`
  * And now - make all our users samba-enabled:
> > `#smbldap-usermod -a -C '\\SERVER\home\user01' -D 'X:' -E 'logon.bat' -F '\\SERVER\profiles\user01' -J user01`
> > `smbldap-usermod -a user01`
  * Add users into Domain Users:
> > `smbldap-groupmod -m user01 Domain\ Users `
  * or in bulk mode:
> > `for ((n=$MIN;n<=$MAX;n++)); do i=$(printf "%02d" $n); smbldap-usermod -a -C '\\SERVER\home\user$i' -D 'X:' -E 'logon.bat' -F '\\SERVER\profiles\user$i' -J user$i; smbldap-groupmod -m user$i Domain\ Users; done `
  * /etc/samba/smb.conf (diff from default):
```
	workgroup = WINDOMAIN
	server string =
	netbios name = SERVER
	interfaces = lo eth0
	hosts allow = 127. 192.168.0.
	security = user
	passdb backend = ldapsam:ldap://127.0.0.1/
	domain master = yes 
	domain logons = yes
	logon script = %m.bat
	logon home = \\%L\Home\%u
	logon path = \\%L\Profiles\%u
	add user script = /usr/sbin/smbldap-useradd -m %u
	add user to group script = /usr/sbin/smbldap-groupmod -m %g %u 
	set primary group script = /usr/sbin/smbldap-usermod -g %g %u 
	add group script = /usr/sbin/smbldap-groupadd -p %g
	add machine script = /usr/sbin/smbldap-useradd -w -i %u
	delete user script = /usr/sbin/smbldap-userdel %u
	delete user from group script = /usr/sbin/smbldap-usermod -x %g %u
	delete group script = /usr/sbin/smbldap-groupdel %g
#	delete machine script = /usr/sbin/smbldap-userdel -w %u
# ----------------------- LDAP ----------------------------
	ldap suffix = dc=ldap
	ldap machine suffix = ou=Hosts
	ldap user suffix = ou=Users
	ldap group suffix = ou=Groups
	ldap admin dn = cn=odmin,dc=ldap
	ldap ssl = no
	ldap passwd sync = Yes
	passwd program = /usr/sbin/smbldap-passwd
	passwd chat = *New*password %n\n *Retype*new*password* %n\n *all*autetication*tokens*updated*
	local master = yes
	os level = 255
	preferred master = yes
	wins support = yes
	printing = cups
	dos charset = CP866
	case sensitive = no
	preserve case = yes
	short preserve case = yes
[Homes]
	comment = Home Directories
	browseable = no
	writable = yes
;	valid users = %S
;	valid users = MYDOMAIN\%S
	
[printers]
	comment = All Printers
	path = /var/spool/samba
	browseable = no
	guest ok = no
	writable = no
	printable = yes
	
[netlogon]
	comment = Network Logon Service
	path = /mnt/shares/netlogon
	guest ok = yes
	writable = no
	share modes = no
[Profiles]
	path = /mnt/shares/profiles
	browseable = no
	guest ok = yes
```
  * Note: don't forget /etc/fstab: ... ,use\_xattr
  * set password of Manager for Samba:
> > `smbpasswd -w secred`
  * lets go:
> > `chkconfig smb on; service smb start`
  * create user's profile directories !
  * make 'echo passXX | smbldap-passwd -s -p user??' for each user
Note: Fedora need nmb on & start


---
