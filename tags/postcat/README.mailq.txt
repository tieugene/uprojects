README for WebQ (http://www.kyberdigi.cz/projects/webq/):
* unpak
* mkdir /var/www/mailq/
* mv webq.pl /var/www/mailq/
* chown root:root /var/www/mailq
* /etc/httpd/conf.d/webq.conf:
	Alias /webq /var/www/webq
	<Directory /var/www/webq>
	Options ExecCGI
	AddHandler cgi-script .pl
	DirectoryIndex webq.pl
	</Directory>
* /var/www/mailq/mailq.pl:
	my %postfix['uid'] = 89
	my readonly = 0;