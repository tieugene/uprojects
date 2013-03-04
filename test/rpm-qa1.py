#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Show all installed rpm - via db4 interface.
v.060623
'''

import bsddb, sys

if (__name__ == '__main__'):
	db = bsddb.hashopen('/var/lib/rpm/Name', 'r')
	k, v = db.first()
	while 1:
		try:
			print k
			k, v = db.next()
		except KeyError:
			break
	db.close()
