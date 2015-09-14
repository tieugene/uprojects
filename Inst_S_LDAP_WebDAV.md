# Introduction #

Add your content here.

# Details #
  * mkdir /var/www/webdav
  * /etc/httd/conf.d/webdav.conf:
```
Alias /webdav /var/www/webdav

<Location /webdav>
    DAV On
    AuthType    Basic
    AuthName    "LDAP Auth"
    AuthBasicProvider ldap
    AuthLDAPURL "ldap://localhost:389/ou=Users,dc=spb,dc=rgsg,dc=ru?uid?sub?(objectClass=*)
    Require valid-user
</Location>
```

# Client #
http://server/webdav

Enjoy