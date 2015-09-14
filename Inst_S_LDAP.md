| <[Core](Inst_S_Core.md) | [TOC](TOC.md) | [PAM](Inst_S_LDAP_PAM.md)> |
|:------------------------|:--------------|:---------------------------|

# LDAP-server #

## Packages ##

  * openldap-servers
  * openldap-clients

## Configs and data ##

configs:
  * /etc/ldap.conf
  * /etc/openldap/slapd.conf
data:
  * /var/lib/ldap

## Setting up ##

### Make configs ###

  1. generate password:
```
[root]# slappasswd -h '{SMD5}' -s secred
```
> > result:
> > > {SMD5}byYxFQWSBfC/VJKooDQuMZUyq1g=
  1. /etc/openldap/slapd.conf:
```
access to *
        by self write
        by users read
        by anonymous auth
database      dbm
suffix        "dc=ldap"
rootdn        "cn=odmin,dc=ldap"
rootpw        {SMD5}byYxFQWSBfC/VJKooDQuMZUyq1g=
```
  1. /var/lib/ldap/DB\_CONFIG

> > bdb: `cp /etc/openldap/DB_CONFIG.example /var/lib/ldap/DB_CONFIG`

## Start ##

```
chkconfig slapd on
service slapd start
```

**Important**: set ldap start order _after_ network but _befor_ named:
` mv /etc/rc.d/rc3.d/S27ldap /etc/rc.d/rc3.d/S12ldap `

### Fill w/ data ###

  1. make Root.ldif
```
dn: dc=ldap
objectClass: dcObject
objectClass: organization
dc: ldap
o: Contora, Ltd.
```
  1. and:
> > `ldapadd -x -D "cn=odmin,dc=ldap" -w secred -h localhost -p 389 -f Root.ldif`