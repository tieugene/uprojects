# Conditions #
db backend:
> mysql
mysqldb:
> egw
Config user:

Header user:
> headuser; headpass
Odmin:


# Ingridients #
Repo:
  * [TI\_Eugene](http://download.opensuse.org/repositories/home:/TI_Eugene/Fedora_8/home:TI_Eugene.repo)
Packages:
  * eGroupware-`*`:
    * 
  * mysql-server
  * httpd
  * php
  * php-pear
Services:
  * httpd
  * mysql
Files:
  * /usr/share/egroupware
Data:

# Setting up #
  * install packages:
> > `cat egw.list | xargs yum install`
  * start services:
> > `service mysql start; service httpd start`
  * create DB and user:
```
mysql
CREATE DATABASE egroupware;
GRANT ALL ON egroupware.* TO 'egroupware'@'localhost' IDENTIFIED BY 'egwpassword';
```
  * [Login](http://localhost/egroupware/)
    * setup header, db
| language | Russian |
|:---------|:--------|
| Header user | headuser |
| Header user password | headpass |
| limit access | 127.0.0.1,192.168.0.0 |
| Persistant | Yes     |
| Session type | PHP     |
| MCrypt   | No      |
| Domain select | No      |
| database | egroupware |
| database user | egroupware |
| database password | egwpassword |
| cfg user | cfguser |
| cfg password | cfgpass |
(CLI: chmod a+rwX /var/lib/egroupware; chmod a+rwX /var/lib/egroupware/header.inc.php)
> > > "Write"
(return rights to default)
    * Step 2: edit cfg: (log in as cfguser)
| ftp-server | localhost |
| http-proxy | localhost |
| proxy port | 3128    |
| proxy user | ...     |
| proxy pass | ...     |
| pop3/imap server | localhost |
| proto    | imap    |
| login type | standard |
| smtp-server | localhost |
| smtp-port | 25      |
| Auth     | LDAP    |
| User accounts | LDAP    |
| SQL encryption | MD5     |
| Activate safe pass check | No      |
| Enable identif | No      |
| Autologin anon | No      |
| Enable move pass No |
| Min uid  | 1000    |
| Max uid  | 1999    |
| User account prefix | ou=Users,dc=com,dc=ru |
| Case sens | Yes     |
| Auto-created expired | never   |
| If no... | wide access |
| LDAP host | localhost |
| LDAP context | ou=Users,dc=com,dc=ru |
| LDAP search filters for accounts |         |
| LDAP group context | ou=Groups,dc=com,dc=ru |
| LDAP root DN | cn=Manager,dc=com,dc=ru |
| LDAP password | secred  |
| LDAP encryption type | MD5     |
| Manage   | No      |
| LDAP Default homedirectory prefix | /mnt/shares/home |
| LDAP default shell | /usr/sh |
| filesystem information | WebDAV  |
| store/retrieve file contents | filesystem |

  * Step 3: Create admin account
    * user - somebody exist user
    * pass - the same
    * Give admin acces - ok
    * other - no

> > Save.
> > If error of LDAP (ldap server may crash - up it) - look at err message and create Default and Admin groups in ldap tree w/ hands (w/ given GIDs). Repeate creating admin account.
  * log in as admin, goto groups and set wanted rights.
## Contacts ##
Prefs - AB:
  * LDAP
  * ou=Contacts
gq: create ou
/etc/openldap/slapd.conf:
  * access to dn="ou=Contacts,dc=com,dc=ru" by **write**

# Note #
eGW make all accounts as "uid=

&lt;uid&gt;

,..." in ldap tree - not cn=...

# tuning #
For Centos, if wanna use mysql, need to install:
**php-mysql** php-mbstring
**php-ldap** php-imap
**php-xml** php-gd
**php-pear-Auth-SASL (PEAR::Auth\_SASL)**

Good choice - php-eaccelerator


---

| <[Asterisk](Inst_S_Asterisk_en.md) || [TOC](TOC.md)|
|:-----------------------------------|