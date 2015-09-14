# Packages #
  * squid
# Files #
  * /etc/squid/squid.conf
# Setting up #
/etc/squid/squid.conf (diffs from default):
```
...
auth_param basic program /usr/lib/squid/squid_ldap_auth -P -b "ou=Users,dc=com,dc=ru" -v 3 -f (uid=%s) -h localhost
...
acl password proxy_auth REQUIRED
...
http_access allow password
...
http_access deny all
```

---

| <[SMTP](Inst_S_LDAP_SMTP_en.md) | [TOC](TOC.md) | [Jabber](Inst_S_LDAP_XMPP_en.md)> |
|:--------------------------------|:--------------|:----------------------------------|