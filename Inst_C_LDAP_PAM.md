# PAM (client) #
## Packages ##
  * nss\_ldap
## Configs ##
  1. enable ldap auth ==
> > `authconfig --enableldap --enableldapauth --disablenis --enablecache --ldapserver=localhost --ldapbasedn=dc=com,dc=ru --updateall`
  1. /etc/ldap.conf
```
host 127.0.0.1
rootbinddn cn=Manager,dc=com,dc=ru
port 389
scope sub
bind_policy soft
pam_filter objectclass=posixAccount
pam_login_attribute uid
nss_base_passwd       ou=Users,dc=com,dc=ru?sub?objectClass=posixAccount
nss_base_shadow       ou=Users,dc=com,dc=ru?sub?objectClass=posixAccount
nss_base_group        ou=Groups,dc=com,dc=ru?sub?objectClass=posixGroup
```