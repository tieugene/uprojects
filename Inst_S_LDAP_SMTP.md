# Ingridients #
Packages:
  * postfix
Conflicts!:
  * sendmail
Configs:
  * /etc/postfix/main.cf
  * /etc/postfix/virtual-`*`.cf

# Setting up #
Diffs from default:
  * /etc/postfix/main.cf:
```
mydomain = eap.su
myorigin = $mydomain
inet_interfaces = all
mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain
mynetworks_style = subnet
mynetworks = 192.168.0.0/24, 127.0.0.0/8
relay_domains = $mydestination
alias_maps = ldap:/etc/postfix/ldap-aliases.cf
mailbox_transport = lmtp:unix:/var/lib/imap/socket/lmtp
### NEW ###
masquerade_domains = $mydomain
in_flow_delay = 1s
disable_vrfy_command = yes
lmtp_connect_timeout = 2s
default_database_type = hash
local_transport = lmtp:unix:/var/lib/imap/socket/lmtp
virtual_alias_maps = ldap:/etc/postfix/ldap-aliases.cf
virtual_mailbox_maps = ldap:/etc/postfix/ldap-users.cf
virtual_mailbox_base =/var/lib/imap
```
  * /etc/postfix/ldap-users.cf:
```
server_host = localhost
search_base = ou=Users,dc=ldap
domain = eap.su
query_filter = (&(mailRoutingAddress=%s)(objectClass=InetLocalMailRecipient))
result_attribute = mailRoutingAddress
bind = no
```
  * /etc/postfix/ldap-aliases.cf:
```
server_host = localhost
search_base = ou=Users,dc=ldap
query_filter = (&(mail=%s)(objectClass=InetLocalMailRecipient))
result_attribute = mailRoutingAddress
bind = no
```
  * chkconfig postfix on; service postfix start

---

| <[POP3/IMAP](Inst_S_LDAP_IMAP_POP3_en.md) | [TOC](TOC.md) | [FetchMail](Inst_S_LDAP_FetchMail_en.md)> |
|:------------------------------------------|:--------------|:------------------------------------------|