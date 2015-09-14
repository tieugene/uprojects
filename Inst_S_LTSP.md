# Ingridients #
**Try system-config-netboot**
Help:
  * [Help](https://fedorahosted.org/k12linux/wiki)
  * [Another Help](http://omsk.lug.ru/LTSP5)
Packages:
  * ltsp-server
Services:
  * syslogd
Configs:
  * /etc/dhcpd.conf
  * /tftpboot//tftpboot/ltsp/i386/pxelinux.cfg/default
  * /etc/gdm/custom.conf
  * /tftpboot/ltsp/i386/lts.conf - example
  * /opt/ltsp/i386/etc/lts.conf - working
Data:
  * /tftpboot/ltsp/i386
  * /opt/ltsp/i386

# Setting up #
  1. Get ltsp:
```
rpm -Uvh http://togami.com/~k12linux-temporary/fedora/8/i386/k12linux-temp-release-0.1-1.noarch.rpm}}} 
yum update
yum install ltsp-server
```
  1. configure them (auto):
> > `ltsp-server-initialize`
  1. or handly:
```
echo "/opt/ltsp *(ro,async,no_root_squash)" >> /etc/exports
chkconfig tftp on
ltsp-build-client --release=8
```
  1. off ltsp bridge interface
  1. /etc/dhcpd.conf
```
	...
	group  "LTSP 5" {
		filename		"/ltsp/i386/pxelinux.0";
		option root-path	"192.168.0.1:/opt/ltsp/i386";

		host host04 {
			hardware ethernet	00:00:0E:BB:9B:CC;
			fixed-address		host04;
		}
	}
	...
```
  * /opt/ltsp/i386/etc/lts.conf:
```
...
```
# Upgrading client #
```
chroot /opt/ltsp/i386
mount /proc
yum ...
```
# TODO #
  * syslog server