# Setting up #
  * vi /etc/exports:
    * /mnt/shares 192.168.0.0/24(rw,no\_root\_squash)
  * chkconfig nfs on && service nfs start ;-)