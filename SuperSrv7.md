# Introduction #

Super server based on CentOS7: VMS, LDAP, all-in-one.

# 0. Pre-req #
  * LAN:
    * LAN: 192.168.0.0/24
    * gw: 192.168.0.254
    * vms: 192.168.0.2
    * server: 192.168.0.1
  * smb:
    * domain: office
  * ldap:
    * base: dc=ldap
    * manager:
      * binddn: "cn=..."
      * password: secredpass

# 1. Any CentOS #
  * download [CentOS7-mini](http://mirror.yandex.ru/centos/7.0.1406/isos/x86_64/CentOS-7.0-1406-x86_64-Minimal.iso), burn it.
  * install
  * patch selinux (/etc/sysconfig/selinux: ...)
  * patch network:
    * /etc/sysconfig/networking:
    * /etc/sysconfig/network-scripts/e**-**
    * /etc/resolve.conf:
  * add repos (epel, rpmfusion)
  * rpm -Uvh .../rpmreaper
  * yum install mc net-tools
  * chk network:
    * chkconfig network on; service network restart; service NetworkManager stop; ping ya.ru;
  * init 6
  * remove unwanted (rpmreaper)
  * yum update

# 2. VMS #
  * add wanted

# 3. Server #

# 4. Client #