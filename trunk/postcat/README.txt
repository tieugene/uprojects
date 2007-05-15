=== Postfix
main.cf:
	mime_header_checks = regexp:/etc/postfix/mime_header_checks
	smtpd_sender_restrictions =
		regexp:/etc/postfix/sender_access,
		permit_mynetworks,
		permit_sasl_authenticated
sender_access:
	/.*@rgsg.ru/i FILTER smtp:[127.0.0.1]:52525
	#/.*eugene@rgsg.ru/i FILTER scan:dummy
	#/.*eugene@rgsg.ru/i FILTER scan:127.0.0.1:10026
	#/.*eugene@rgsg.ru/i HOLD held due sec reason
	#/.*outcontrol@rgsg.ru/i OK
	#/.*eugene@rgsg.ru/i REDIRECT outcontrol@rgsg.ru - loopback
	#/.*@rgsg.ru/i HOLD held due sec reason
master.cf:
	smtp      inet  n       -       n       -       -       smtpd
		-o receive_override_options=no_header_body_checks
	...
	127.0.0.1:52525    inet  n     -     n     -     -     smtpd
		-o smtpd_authorized_xforward_hosts=127.0.0.0/8
		-o smtpd_client_restrictions=
		-o smtpd_helo_restrictions=
		-o smtpd_sender_restrictions=
		-o smtpd_recipient_restrictions=permit_mynetworks,reject
		-o smtpd_data_restrictions=
		-o mynetworks=127.0.0.0/8
		-o receive_override_options=no_unknown_recipient_checks
mime_header_checks:
	/^\s*Content-(Type|Disposition):.*name\s*=\s*.*/i HOLD held to check
	#/^\s*Content-(Disposition|Type).*name\s*=\s*"?(.+\.(lnk|asd|hlp|ocx|reg|bat|c[ho]m|cmd|exe|dll|vxd|pif|scr|hta|jse?|sh[mbs]|vb[esx]|ws[fh]|wav|mov|wmf|xl|jpg|bmp|gif|mp3))"?\s*$/ HOLD on the check

== WWW
* yum install php-pecl-mailparse
* /etc/sudoers:
	apache	ALL = NOPASSWD: /bin/ls, /usr/sbin/postcat, /usr/sbin/postsuper, /var/spool/postfix/hold
//* /etc/php.ini:
//	register_globals = Off
* /etc/httpd/conf.d/mailstop.conf:
	Alias /mailstop /var/www/mailstop
	<Directory "/var/www/mailstop">
		Options Indexes
		DirectoryIndex index.php
		AllowOverride None
		Order allow,deny
		Allow from 192.168.1.0/24
		Deny from
	</Directory>
* /var/www/index.php:
	...

====
* operations:
 - list:
  - mailq	// any
  - postqueue -p
  - sendmail -bp
  - ls /var/spool/postfix/hold	// root, postfix
  - sudo -u postfix ls /var/spool/postfix/hold
 - get:
  - postcat /var/spool/postfix/hold/<id>	// root, postfix
  - sudo -u postfix /usr/sbin/postcat /var/spool/postfix/hold/BB6ADAF6C8
 - del|release
  - postsuper <id>	// root
  - rm -f /var/spool/postfix/hold/<id>	// postfix

* So, We need:
 - ID		<filename>
 - Date		Sect['1'].['headers'].['date']
 - From		Sect['1'].['headers'].['from']
 - To		Sect['1'].['headers'].['to']
 - Subj		Sect['1'].['headers'].['subject']
 - Contents	switch Sect['...'].['content-type']:
			case 'multipart/*':
				skip
			case 'text/*':
				show
			else
				if 'content-name':
					show attach as filename
				else:
					'error'

* $pirimennoya = $HTTP_GET_VARS['foo'];

<?php
 session_start();
 if (!($_SESSION['user_accepted']=="yes")) {
   require_once( 'includes/authorize.php' );
   die;
 }
 if (isset($_GET['logout'])){
   $_SESSION['user_accepted']="no";
   $_SESSION['user_login']="";
   $_SESSION['user_passwd']="";
   Header("Location: index.php"); 
 }
?>

== Howto
* Converting UTF-8 to HTML-Entities:
	if (function_exists('mb_convert_encoding')) 
		return mb_convert_encoding($s, 'HTML-ENTITIES', 'UTF-8');

* Autorefresh:
	<meta http-equiv="refresh" content="600">
* Autoredirect
	<meta http-equiv="refresh" content="2;url=http://webdesign.about.com">
* important keys:
	disable_mime_input_processing (default: no)
	header_checks (default: empty)
	mime_header_checks (default: $header_checks)
* ripmime
* вызов с ключами для тестирования:
	php index.php key1=val1 key2=val2
* иконка сайта
	<head>...<link rel="SHORTCUT ICON" href="/favicon.ico" type="image/x-icon">...</head>

знач админ запретил
после неких действий - джаваскрипт
оидн подобный скрипт уже нашёл...
window.location.href='filename.php';
перебросить на необходимый файл
а так, создаём функцию, любого имени
а в хтмл коде добавляем событиеи действие при событии
действием при событии будет данная фун-я
в которой осуществляется переход по ссылку с возможной передачей параметров
напимер при наведение указателя мыши на ссылку вызвать фуг-ю такую-то
и так далие

щас перечислю возможные события
	OnClick
	OnDblClick
	OnDragStart
	OnHelp
	OnKeyDown
	OnKeyPress
	OnKeyUp
	KeyCode
	OnMouseDown
	OnMouseMove
	OnMouseOut
	OnMouseOver
	OnMouseUp
	OnSelectStart

* Authorization
<?
	session_start();
	if(!isset($_SESSION['AUTH_STATUS'])) 
	{
		echo "Мужик, для просмотра этой страницы надо залогиниться";
		SHOW_AUTH_FORM(); //Думаю функцию вывода формы авторизации сам написать сможешь
	} else {
		echo "Вы залогинены"; 
	}

== TODO
* authorize
* Subj
* msg preview
 - seg fault
 - Кодировка plain text

== Done
* msg caching
* При Drop и Send - авторефреш
* Авторефреш 1/min
* alert icon

== Ideas
x py - нипалучаиццо
* ajax

== NextGen
* get msg
* filter and split to envelop and body
* envelop:
 - message_size:
 - message_arrival_time:
 - sender:
 - recipient:
* Table:
 - ID
 - Date
 - From
 - To
 - e-mail
 - Send/Drop (icons)
* body - view via kmail
* caching msgs

== Errors:
* insert all after deleting

== Py
/etc/httpd/conf/httpd.conf
	AddHandler .cgi .py
	<Directory "/var/www/cgi-bin">
		Option ExecCGI
		...
/var/www/cgi-bin/index.py:
	...


== What Im
=== Языки
* Могу и люблю:
 - C
 - C++
 - Python
 - SQL
* Могу, но не люблю:
 - Perl
 - PHP
 - ECMAScript
 - ASM
 - Basic
 - Fortran
 - PL/1
 - Forth
 - 1С 7.7
 - 1С 8.0
* читаю:
 - Java
 - Pascal
* разное:
 - sh
 - awk
 - grep

=== Libs
* Qt

=== Tech
* XML

=== Formats
* docbook
* html
