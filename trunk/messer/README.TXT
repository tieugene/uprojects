Что надо для работы:

perl -MPAN -e \
'install Net::XMPP2 Log::Log4perl Net::LDAP Data::Dumper::Simple AnyEvent XML:Twig'




Настройки проги хранятся в LDAP. У меня это в виде:
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


