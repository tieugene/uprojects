We will use example.com jabber domain.

# Packages #
  * jabberd (from [redhatclub-repository](http://repo.redhat-club.org/redhat/5/i386/redhatclub-repository-release-5-3.el5.rhc.noarch.rpm)).
# Files #
  * /etc/jabberd/c2s.xml
  * /etc/jabberd/sm.xml
# Setting up #
We use default configs. Just differences from default configs will
## c2s.xml ##
```
<c2s>
 ...
 <local>
  ...
  <id register-enable='true'>lan</id> <!-- localhost.localdomain -->
 ...
 </local>
 ...
 <authreg>
  ...
  <module>ldap</module> <!-- pam -->
  ...
  <ldap>
   ...
   <host>server.lan</host> <!-- ldap.example.com -->
   ...
   <basedn>ou=Users,dc=ldap</basedn>
   ...
  <ldap>
  ...
 </authreg>
 ...
</c2s>
```
## sm.xml ##
Now I can't use ldap as storage for Session manager ;-(
So, we will use BDB as storage.
```
<sm>
 ...
 <id>lan</id> <!-- localhost.localdomain -->
 ...
 <storage>
  ...
  <driver>db</driver>
  ...
  <driver type='published-roster'>ldapvcard</driver>
  <driver type='published-roster-groups'>ldapvcard</driver>
  ...
  <ldapvcard>
   ...
   <uri>ldap://localhost/</uri>
   ...
   <type>ldap</type>
   ...
   <uidattr>uid</uidattr>
   <objectclass>posixAccount</objectclass>
   <pwattr>userPassword</pwattr>
   ...
   <basedn>dc=ldap</basedn>
   ...
   <groupattr>jabberPublishedGroup</groupattr>
   ...
   <publishedattr>jabberPublishedItem</publishedattr>
   ...
   <mapped-groups>
    ...
    <map-groups/>
    ...
    <basedn>ou=Groups,dc=ldap</basedn>
    ...
   </mapped-groups>
  </ldapvcard>
 </storage>
 ...
 <user>
  ...
  <auto-create/> <!-- !!! -->
  ...
 <user>
 ...
</sm>
```

chkconfig jabberd on; service jabberd start
## Option ##
It's can B use jabberd2.schema:
  * /etc/openldap/slapd.conf:
> > `include         /etc/openldap/schema/jabberd2.schema`
  * service ldap restart
  * for each user:
```
for ((...));
echo "
dn: uid=user$i,ou=Users,dc=ldap
changetype: modify
add: objectClass
objectClass: jabberExtendedObject
-
add: jabberPublishedItem
jabberPublishedItem: 1
-
add: jabberPublishedGroup
jabberPublishedGroup: 500
" >> tmp.txt
ldapmodify -x -D "cn=odmin,dc=ldap" -w secred -h localhost -f tmp.txt
```

---

| <[Proxy](Inst_S_LDAP_Proxy_en.md) | [TOC](TOC.md) | [FTP](Inst_S_LDAP_FTP_en.md)> |
|:----------------------------------|:--------------|:------------------------------|