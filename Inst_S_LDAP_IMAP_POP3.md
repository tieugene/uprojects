| <[Samba](Inst_S_LDAP_SAMBA_en.md) | [TOC](TOC.md) | [SMTP](Inst_S_LDAP_SMTP_en.md)> |
|:----------------------------------|:--------------|:--------------------------------|

---

# Ingridients #
Packages:
  * cyrus-imapd
Daemons
  * saslauthd
  * curus-imapd
Configs
  * /etc/saslauthd.conf
  * /etc/cyrus.conf
  * /etc/imapd.conf
Data
# Setting up #
## SASL ##
/etc/saslauthd.conf (create):
```
ldap_servers: ldaps://127.0.0.1/
ldap_search_base: cn=Users,dc=ldap
ldap_use_sasl: yes
ldap_mech: DIGEST_MD5
ldap_auth_method: fastbind 
#ldap_bind_dn: cn=Manager,dc=com,dc=ru
#ldap_bind_pw: secret
#ldap_filter: (&(uid=%u)(objectclass=posixAccount))
#ldap_version: 3
#ldap_timeout: 5
#ldap_time_limit: 5
```
`service saslauthd start`
## Cyrus ##
/etc/imapd.conf:
```
# default
configdirectory: /var/lib/imap
partition-default: /var/spool/imap
#admins: cyrus
sievedir: /var/lib/imap/sieve
sendmail: /usr/sbin/sendmail
hashimapspool: true
sasl_pwcheck_method: saslauthd
#sasl_mech_list: PLAIN
tls_cert_file: /etc/pki/cyrus-imapd/cyrus-imapd.pem
tls_key_file: /etc/pki/cyrus-imapd/cyrus-imapd.pem
tls_ca_file: /etc/pki/tls/certs/ca-bundle.crt
# new
allowanonymouslogin: yes
allowplaintext: yes
autocreatequota: 10000000
createonpost: yes
sasl_mech_list: CRAM-MD5
force_sasl_client_mech: CRAM-MD5
virtdomains: off
```
/etc/cyrus.conf:
```
SERVICES {
...
Lmtp cmd="lmtpd -a" listen="localhost:lmtp"
...
```
`chkconfig saslauthd on; chkconfig cyrus-imapd on; service saslauthd start; service cyrus-imapd start`

---

| <[Samba](Inst_S_LDAP_SAMBA_en.md) | [TOC](TOC.md) | [SMTP](Inst_S_LDAP_SMTP_en.md)> |