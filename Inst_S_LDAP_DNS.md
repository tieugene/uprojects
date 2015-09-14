| <[PAM](Inst_S_LDAP_PAM.md) | [TOC](TOC.md) | [DHCP](Inst_S_LDAP_DHCP.md)> |
|:---------------------------|:--------------|:-----------------------------|

# DNS #

## Sources ##

  * [One](http://www.opennet.ru/docs/RUS/bind2ldap)
  * [Two](http://bind9-ldap.bayour.com/dnszonehowto.html)

## Packages ##

  * bind
  * bind-chroot
  * bind-sdb

## Files ##

  * /etc/openldap/schema/dnszone.schema

## Install ##

### LDAP ###

  1. /etc/openldap/slapd.conf (inserted by bind-sdb):
```
include		/etc/openldap/schema/dnszone.schema	# dns
```
  1. restart:
> > `service ldap restart`
  1. DNS.ldif (zone and server - forward and RR):
```
dn: ou=DNS,dc=ldap
objectClass: top
objectClass: organizationalUnit
ou: DNS

dn: zoneName=lan,ou=DNS,dc=ldap
objectClass: top
objectClass: dNSZone
zoneName: lan
relativeDomainName: lan

dn: relativeDomainName=@,zoneName=lan,ou=DNS,dc=ldap
objectClass: top
objectClass: dNSZone
zoneName: lan
relativeDomainName: @
nSRecord: server.lan.
sOARecord: server.lan. hostmaster.lan. 1 8H 2H 1W 1D

dn: relativeDomainName=localhost,zoneName=lan,ou=DNS,dc=ldap
objectClass: top
objectClass: dNSZone
zoneName: lan
relativeDomainName: localhost
dNSClass: IN
aRecord: 127.0.0.1

dn: relativeDomainName=server,zoneName=lan,ou=DNS,dc=ldap
objectClass: top
objectClass: dNSZone
zoneName: lan
relativeDomainName: server
dNSClass: IN
aRecord: 192.168.0.1

dn: zoneName=0.168.192.in-addr.arpa,ou=DNS,dc=ldap
objectClass: top
objectClass: dNSZone
zoneName: 0.168.192.in-addr.arpa
relativeDomainName: 0.168.192.in-addr.arpa

dn: relativeDomainName=@,zoneName=0.168.192.in-addr.arpa,ou=DNS,dc=ldap
objectClass: top
objectClass: dNSZone
zoneName: 0.168.192.in-addr.arpa
relativeDomainName: @
nSRecord: server.lan.
sOARecord: server.lan. hostmaster.lan. 1 8H 2H 1W 1D

dn: relativeDomainName=1,zoneName=0.168.192.in-addr.arpa,ou=DNS,dc=ldap
objectClass: top
objectClass: dNSZone
zoneName: 0.168.192.in-addr.arpa
relativeDomainName: 1
pTRRecord: server.lan.
```
  1. `ldapadd -x -D "cn=odmin,dc=ldap" -w secred -h localhost -p 389 -f DNS.ldif`
  1. add new host
```
dn: relativeDomainName=gw,zoneName=lan,ou=DNS,dc=ldap
objectClass: top
objectClass: dNSZone
zoneName: lan
relativeDomainName: gw
dNSClass: IN
aRecord: 192.168.0.254

dn: relativeDomainName=254,zoneName=0.168.192.in-addr.arpa,ou=DNS,dc=ldap
objectClass: top
objectClass: dNSZone
zoneName: 0.168.192.in-addr.arpa
relativeDomainName: 254
pTRRecord: gw.lan.
```
  1. and another one:
```
dn: relativeDomainName=host002,zoneName=lan,ou=DNS,dc=ldap
objectClass: top
objectClass: dNSZone
zoneName: lan
relativeDomainName: host002
dNSClass: IN
aRecord: 192.168.0.2

dn: relativeDomainName=2,zoneName=0.168.192.in-addr.arpa,ou=DNS,dc=ldap
objectClass: top
objectClass: dNSZone
zoneName: 0.168.192.in-addr.arpa
relativeDomainName: 2
pTRRecord: host002.lan.
```
  1. or bulk hosts creation:
```
#!/bin/sh
# bulkhosts.sh - bulk ldap hosts creation
MIN=2
MAX=99
for ((n=MIN;n<=$MAX;n++)); do
    i=$(printf "%03d" $n)
    echo "\
dn: relativeDomainName=host$i,zoneName=lan,ou=DNS,dc=ldap
objectClass: top
objectClass: dNSZone
zoneName: lan
relativeDomainName: host$i
dNSClass: IN
aRecord: 192.168.0.$n

dn: relativeDomainName=$n,zoneName=0.168.192.in-addr.arpa,ou=DNS,dc=ldap
objectClass: top
objectClass: dNSZone
zoneName: 0.168.192.in-addr.arpa
relativeDomainName: $n
pTRRecord: host$i.lan.
" | ldapadd -x -D "cn=odmin,dc=ldap" -w secred -h localhost
done
```

### BIND ###

  1. `cp /usr/share/doc/bind-9.7.0/sample/etc/* /var/named/chroot/etc/named`
  1. `cp /usr/share/doc/bind-9.7.0/sample/var/named/[ln]* /var/named/chroot/var/named`
  1. `cd /var/named/chroot/var/named; wget ftp://ftp.rs.internic.net/domain/named.root`
  1. /var/named/chroot/etc/named/named.conf:
```
options {
        directory               "/var/named";
        dump-file               "data/cache_dump.db";
        statistics-file         "data/named_stats.txt";
        memstatistics-file      "data/named_mem_stats.txt";
        query-source address    * port 53;
        forwarders {
                8.8.8.8;
                8.8.4.4;
        };
};
logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
        };
};
include "/etc/named.root.hints";
include "/etc/named.rfc1912.zones";
zone "lan." IN {
        type master;
        database "ldap ldap://127.0.0.1/zoneName=lan,ou=DNS,dc=ldap 178600";
        allow-update { none; };
};
zone "0.168.192.in-addr.arpa." IN {
	type master;
        database "ldap ldap://127.0.0.1/zoneName=0.168.192.in-addr.arpa,ou=DNS,dc=ldap 178600";
        allow-update { none; };
};
```
  1. /etc/sysconfig/named:
```
...
ENABLE_SDB=yes
```
  1. chkconfig named on && service named restart
  1. checking: resolveip 

&lt;hostname&gt;

/

&lt;ip&gt;

 (mysql-server)