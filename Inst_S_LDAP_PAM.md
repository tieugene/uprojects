| <[LDAP](Inst_S_LDAP.md) | [TOC](TOC.md) | [DNS](Inst_S_LDAP_DNS.md)> |
|:------------------------|:--------------|:---------------------------|

# PAM #

## Server ##

After installing server part of config we must configure server as client - to use LDAP-auth for other LDAP-based services.

### Configs ###

  * /etc/openldap/slapd.conf

### Configure ###

  1. /etc/openldap/slapd.conf (diff -U1 slapd.conf.orig slapd.conf):
```
--- slapd.conf.orig     2009-01-21 11:59:59.000000000 +0300
+++ slapd.conf  2009-06-02 19:14:50.000000000 +0400
@@ -68,6 +69,10 @@
 # access to dn.base="cn=Subschema" by * read
-# access to *
-#      by self write
-#      by users read
-#      by anonymous auth
+access to *
+       by self write
+       by users read
+       by anonymous read
+access to attrs=userPassword
+       by self write
+       by anonymous read
+       by * none
 #
```

  1. service ldap restart

### Fill out w/ data ###

  1. Users.ldif:
```
dn: ou=Users,dc=ldap
objectClass: top
objectClass: organizationalUnit
ou: Users
```
> > Add:
> > > `ldapadd -x -D "cn=odmin,dc=ldap" -w secred -h localhost -p 389 -f Users.ldif`
  1. Groups.ldif
```
dn: ou=Groups,dc=ldap
objectClass: top
objectClass: organizationalUnit
ou: Groups
```

> > Add: ...
  1. user00.ldif (using gid=100):
```
dn: uid=user00,ou=Users,dc=ldap
objectClass: top
objectClass: posixAccount
objectClass: person
objectClass: organizationalPerson
objectClass: inetOrgPerson
cn: cn00
sn: sn00
uid: user00
uidNumber: 500
gidNumber: 100
loginShell: /bin/bash
homeDirectory: /mnt/shares/home/user00
```
> > Note: if we plane use special primary group (gid=500), we must use gidNumber: 500 and next:
  1. adding groups (group00.ldif):
```
dn: cn=group00,ou=Groups,dc=ldap
objectClass: posixGroup
cn: group00
gidNumber: 500
description: Primary group of ldap domain
memberUid: user00
memberUid: user01
...
```
  1. setting passwords:
```
ldappasswd -x -D "cn=odmin,dc=ldap" -w secred -h localhost -p 389 -s pass00 uid=user00,ou=Users,dc=ldap
```
Bulk user creation:
```
#!/bin/sh
# bulkusers.sh - bulk user creation in ldap
MIN=0
MAX=30
for ((n=$MIN;n<=$MAX;n++)); do
    i=$(printf "%02d" $n)
    echo "\
dn: uid=user$i,ou=Users,dc=ldap
objectClass: top
objectClass: posixAccount
objectClass: person
objectClass: organizationalPerson
objectClass: inetOrgPerson
cn: cn$i
sn: sn$i
uid: user$i
uidNumber: 5$i
gidNumber: 100
loginShell: /bin/sh
homeDirectory: /mnt/shares/home/user$i
" | ldapadd -x -D "cn=odmin,dc=ldap" -w secred -h localhost
ldappasswd  -x -D "cn=odmin,dc=ldap" -w secred -h localhost -s pass$i uid=user$i,ou=Users,dc=ldap
done
```

### Configure as PAM-client ###

See below.

### Make homes ###

```
mkdir /mnt/shares/home
for i in `cat uids.txt`; do mkdir /mnt/shares/home/user$i; chown user$i:users /mnt/shares/home/user$i; chmod 700 /mnt/shares/home/user$i; done
```

## PAM (client) ##

### Packages ###

  * nss-pam-ldapd
  * authconfig

### Configs ###

For localhost (server).
  1. enable ldap auth ==
> > `authconfig --enableldap --enableldapauth --disablenis --enablecache --ldapserver=localhost --ldapbasedn=dc=ldap --updateall`
  1. /etc/openldap/ldap.conf:
```
host 127.0.0.1
base dc=ldap
scope sub
pam_filter objectclass=posixAccount
pam_login_attribute uid
pam_password exop
nss_base_passwd         ou=Users,dc=ldap?one
nss_base_shadow         ou=Users,dc=ldap?one
nss_base_group          ou=Groups,dc=ldap?one
nss_initgroups_ignoreusers root,ldap
uri ldap://localhost/
ssl no
tls_cacertdir /etc/openldap/cacerts
pam_password md5
```
> > or (diff):
```
--- ldap.conf.orig      2009-06-02 19:36:20.000000000 +0400
+++ ldap.conf   2009-06-02 19:41:42.000000000 +0400
@@ -52 +52 @@
-#scope sub
+scope sub
@@ -76 +76 @@
-#pam_filter objectclass=account
+pam_filter objectclass=posixAccount
@@ -79 +79 @@
-#pam_login_attribute uid
+pam_login_attribute uid
@@ -151 +151 @@
-#pam_password exop
+pam_password exop
@@ -167,3 +167,3 @@
-#nss_base_passwd       ou=People,dc=example,dc=com?one
-#nss_base_shadow       ou=People,dc=example,dc=com?one
-#nss_base_group                ou=Group,dc=example,dc=com?one
+nss_base_passwd        ou=Users,dc=ldap?one
+nss_base_shadow        ou=Users,dc=ldap?one
+nss_base_group         ou=Groups,dc=ldap?one
```

  1. chkconfig nscd on && service nscd restart
  1. chkconfig nslcd on && service nslcd restart
  1. init 6