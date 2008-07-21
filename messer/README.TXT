Настройки проги хранятся в конфиге либо в LDAP. У меня это в виде:
-------------------------------------------------------------------------------------------
version: 1

dn: cn=Messenger,ou=Services,dc=lc,dc=floodlightgames,dc=com
objectClass: applicationProcess
cn: Messenger
description: [main][port] = 54333
description: [email][enabled] = 1
description: [email][from] = floodlightgames@gmail.com
description: [email][auth_host] = smtp.gmail.com
description: [email][auth_port] = 465
description: [email][auth_user] = floodlightgames@gmail.com
description: [email][auth_password] = passwd
description: [ICQ][enabled] = 1
description: [ICQ][uin] = 495173817
description: [ICQ][password] = passwd
description: [jabber][enabled] = 1
description: [jabber][uin] = floodlightgames@gmail.com
description: [jabber][password] = passwd
-------------------------------------------------------------------------------------------


Можно и в конфиге. Тогда нужно запускать прогу так:

/path/to/MesSer.pl -c /path/to/MesSer.conf

Файл MesSer.conf в качестве примера имеется в наличии:

-------------------------------------------------------------------------------------------
[main]
port = 54333

[email]
enabled = 1
from = floodlightgames@gmail.com
auth_host = smtp.gmail.com
auth_port = 465
auth_user = floodlightgames@gmail.com
auth_password = passwd

[ICQ]
enabled = 1
uin = 495173817
password = passwd

[jabber]
enabled = 1
uin = floodlightgames@gmail.com
password = passwd
-------------------------------------------------------------------------------------------


Настройки на логгирование хранятся в отдельном файле MesSer.log.conf
Опять же - имеется в наличии.

