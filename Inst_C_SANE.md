# Introduction #

Add your content here.


# Sane-server #
/etc/sane.d/saned.conf:
> `192.168.1.0/24`
/etc/xinet.d/sane-port (create):
```
service sane-port
{
    port        = 6566
    socket_type = stream
    wait        = no
    user        = root
    group       = root
    server      = /usr/sbin/saned
    disable     = no
}
```

/etc/services (add):
sane-port 6566/tcp # SANE network scanner daemon

# Client #

/etc/sane.d/net.conf:
> 

&lt;sane-server-hostname&gt;

