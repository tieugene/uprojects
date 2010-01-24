#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
kill all sro_* tables
'''

import sys
if (sys.version_info[:2] < (2,6):
	import sqlite
else:
	import sqlite3 as sqlite

reload(sys)
sys.setdefaultencoding( "utf-8" )

def	main():
	conn = sqlite.connect('/mnt/shares/lansite/db/lansite.db', autocommit=1)
	c = conn.cursor()
	l = list()
	c.execute('SELECT name FROM sqlite_master WHERE type="table"')
	for t in c:
		if t[0][:4] == 'sro_':
			l.append(t[0])
	for t in l:
		c.execute('DROP TABLE main.%s' % t)
	c.execute('VACUUM')
	conn.close()

if (__name__ == '__main__'):
	main()