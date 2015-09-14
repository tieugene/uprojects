| <[DNS](Inst_S_LDAP_DNS.md) | [TOC](TOC.md) | [Samba](Inst_S_LDAP_SAMBA.md)> |
|:---------------------------|:--------------|:-------------------------------|

# DHCP #

## Sources ##

  * [AltLinux](http://www.citforum.ru/operating_systems/linux/schema_ldap)

## Packages ##

  * dhcp

# Files #

  * /etc/dhcpd.conf /etc/openldap/schema/dhcp.schema - don't touch
  * /etc/sysconfig/network

# Setting up #

  1. /etc/sysconfig/network:
```
...
HOSTNAME=server.lan
...
```
  1. service network restart
  1. /etc/openldap/slapd.conf:
```
include		/etc/openldap/schema/dhcp.schema
index           dhcpHWAddress 	eq
index           dhcpClassData	eq
```
  1. service ldap restart
  1. /etc/dhcp/dhcpd.conf:
```
ldap-server "localhost";
ldap-port 389;
ldap-username "cn=odmin,dc=ldap";
ldap-password "secred";
ldap-base-dn "cn=server.lan,ou=DHCP,dc=ldap";
ldap-method static;
```
  1. DHCP.ldif (ou, common config, subnet):
```
dn: ou=DHCP,dc=ldap
objectClass: top
objectClass: organizationalUnit
ou: DHCP

dn: cn=server.lan,ou=DHCP,dc=ldap
objectClass: top
objectClass: dhcpServer
cn: server.lan
dhcpServiceDN: cn=config,cn=server.lan,ou=DHCP,dc=ldap

dn: cn=config,cn=server.lan,ou=DHCP,dc=ldap
cn: config
objectClass: top
objectClass: dhcpService
objectClass: dhcpOptions
dhcpPrimaryDN: cn=server.lan,ou=DHCP,dc=ldap
dhcpOption: domain-name "lan"
dhcpOption: domain-name-servers 192.168.0.1
dhcpOption: time-offset -5
dhcpOption: ntp-servers 192.168.0.1
dhcpOption: broadcast-address 192.168.0.255
dhcpOption: log-servers 192.168.0.1
dhcpStatements: default-lease-time 21600
dhcpStatements: max-lease-time 43200
dhcpStatements: ddns-update-style none
dhcpStatements: use-host-decl-names on

dn: cn=192.168.0.0,cn=config,cn=server.lan,ou=DHCP,dc=ldap
cn: 192.168.0.0
objectClass: top
objectClass: dhcpSubnet
objectClass: dhcpOptions
dhcpNetMask: 24
dhcpOption: routers 192.168.0.1
dhcpOption: routers 192.168.0.254
dhcpOption: subnet-mask 255.255.255.0
```
  1. new host group - simple workstations:
```
dn: cn=Static,cn=192.168.0.0,cn=config,cn=server.lan,ou=DHCP,dc=ldap
objectClass: top
objectClass: dhcpGroup
cn: Static
```
  1. and new host in this group:
```
dn: cn=host002,cn=Static,cn=192.168.0.0,cn=config,cn=server.lan,ou=DHCP,dc=ldap
objectClass: top
objectClass: dhcpHost
cn: host002
dhcpHWAddress: ethernet 00:11:22:33:44:55
dhcpStatements: fixed-address host002
```
  1. chkconfig dhcpd on && service dhcpd restart

# ToDo #

  * Try to merge dhcp and dns records