# Ingridients #
Packages:
  * pure-ftpd
Configs:
  * /etc/pure-ftpd/pure-ftpd.conf
  * /etc/pure-ftpd/pureftpd-ldap.conf
Data:
    * /var/ftp
# Setting up #
  * /etc/pure-ftpd/pure-ftpd.conf (diff from orig):
```
LDAPConfigFile /etc/pure-ftpd/pureftpd-ldap.conf
```
  * /etc/pure-ftpd/pureftpd-ldap.conf
```
LDAPServer server
LDAPBaseDN ou=Users,dc=com,dc=ru
```
  * chkconfig... service...

---

# Ingridients #
Packages:
  * vsftpd
Configs:
  * /etc/pam.d/vsftpd
  * /etc/vsftpd/vsftpd.conf
Data:
    * /mnt/shares/ftp
# Setting up #
  * /etc/pam.d/vsftpd (add to default):
> > `auth required pam_ldap.so`
  * /etc/vsftpd/vsftpd.conf (add to default):
```
anon_root=/mnt/shares/ftp
local_root=/mnt/shares/ftp
```
  * mkdir /mnt/shares/ftp && chown root:group00 /mnt/shares/ftp && chmod 775  /mnt/shares/ftp
    * chkconfig... service...

---

| <[Jabber](Inst_S_LDAP_XMPP_en.md) | [TOC](TOC.md) | [HTTP](Inst_S_LDAP_HTTP_en.md)> |
|:----------------------------------|:--------------|:--------------------------------|

---