| <[Server](Inst_S.md) | [TOC](TOC.md) | [LDAP-based services](Inst_S_LDAP_Intro.md)> |
|:---------------------|:--------------|:---------------------------------------------|

# Core #

  1. install [CentOS 6.0](http://mirror.yandex.ru/centos/6.0/isos/i386/)
  1. remove unwanted packages (rpmreaper)
  1. add needed packages

### Network ###

/etc/sysconfig/network-scripts/ifcfg-eth0:
```
DEVICE=eth0
HWADDR=08:00:27:26:57:22
NM_CONTROLLED=no
ONBOOT=yes
BOOTPROTO=none
IPADDR=192.168.0.1
NETMASK=255.255.255.0
TYPE=Ethernet
GATEWAY=192.168.0.254
IPV6INIT=no
USERCTL=no
```
Note: after dump/restore tune up /etc/udev/rules.d/70-persistent-net.rules