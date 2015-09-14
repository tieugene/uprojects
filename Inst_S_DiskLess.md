# Ingridients #
Help:
  * [One](http://www.rhd.ru/docs/manuals/enterprise/RHEL-4-Manual/sysadmin-guide/ch-pxe.html)
Packages:
> Server:
    * system-config-netboot
> Client:
    * busybox-anaconda
Services:
  * nfs
  * tftp
  * syslog?
Configs:
  * /etc/exports
Data:
  * /var/lib/netboot/
  * /tftpboot/linux-install/

# Setting up #
## Client ##
  1. install system:
    1. mandatory:
      * kernel ;-)
      * busybox-anaconda
      * dhclient
      * openssh-server
      * xorg-x11-drv-vga/i810/ati
      * xorg-x11-fonts-misc
      * xorg-x11-xinit
    1. option:
      * cups
      * sane
      * hplip
  1. remove unused packages (rpmtop)
  1. stop (or remove) unused daemons:
    1. autofs
    1. avahi-daemon
    1. hddtemp
    1. mdmonitor
    1. irqbalance
    1. smartd
  1. prepare as X-terminal:
    1. /etc/inittab:
```
id:5:initdefault:
...
# Run xdm in runlevel 5
#x:5:once:/etc/X11/prefdm -nodaemon
x:5:once:/usr/bin/X -query <x-terminal server>
```
    1. /etc/X11/xorg.conf:
```
...
Section "Files"
        FontPath        "/usr/share/X11/fonts/misc"
EndSection
...
```
    1. /etc/cups/cupsd.conf:
```
???
```
    1. /etc/sane/saned.conf:
```
192.168.1.0/24
```
    1. /etc/xinetd.d/sane-port
```
disable = no
```
    1. syslog
```
???
```
## Server ##
  1. install needed pkg:
> > `yum install system-config-netboot`
  1. create DL root catalog:
> > `mkdir /var/lib/netboot/root`
  1. get client image:
> > `rsync -v -a -e ssh --exclude='/proc/*' --exclude='/sys/*' --exclude='/dev/*' --exclude='/var/log/*' --exclude='/var/run/*' <clientip:/> /var/lib/netboot/root`
  1. add to /etc/exports:
```
/var/lib/netboot/root          *(ro,async,no_root_squash)
/var/lib/netboot/snapshot      *(rw,async,no_root_squash)
```
  1. /etc/sysconfig/rsyslog:
```
SYSLOGD_OPTIONS="-m 0 -r"
...
```
  1. LDAP:
    1. cn=LTSP,cn=192.168.0.0,cn=config,cn=server.example.ru,ou=DHCP,dc=com,dc=ru:
> > > dhcpStatement: filename "/linux-install/pxelinux.0"
  1. Prepare DL root:
    1. GUI (system-config-netboot):
      1. name=Xterm; desc=...
      1. server IP: 192.168.0.1; dir=/var/lib/netboot
      1. kernel - ok
    1. CLI (e.g., has to be tested):
> > > `pxeos -a -i "X, cups, sane, hplip" -p NFS -D 1 -s server -L /var/lib/netboot -k kernel-2.6.25.6-27.fc8 Xterm`
  1. add machine[s](s.md):
    1. GUI (system-config-network):
      1. 

&lt;hostname&gt;


      1. snapshot - 

&lt;hostname&gt;


      1. remote log: Enable, server
    1. CLI:
> > > `pxeboot -a -e eth0 -O Xterm -r 24313 <hostname>`

---

| <[CUPS](Inst_S_CUPS_en.md) | [TOC](TOC.md) | [Asterisk](Inst_S_Asterisk_en.md)> |
|:---------------------------|:--------------|:-----------------------------------|