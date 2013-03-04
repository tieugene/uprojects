#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
script to dump rpm database files - via db4 interface.
'''
import bsddb, sys, struct, pprint

def	main(argv):
	hash = {}
	# 1. open db
#	db = bsddb.btopen('/var/lib/rpm/Provideversion', 'r')	# hashopen
	db = bsddb.hashopen('/var/lib/rpm/Basenames', 'r')	# hashopen
#	pprint.pprint(db.keys())
	# 2. process each record
	k, v = db.first()
	while 1:
		try:
			i = struct.unpack("<%dI" % (len(v)/4), v)			# convert
			l = len(v)
			print "%s\t%d\t%s" % (k, len(v), (" %04X" * len(i) % i))	# out
			for j in i[::2]:						# store
				hash[j] = True
			k, v = db.next()
		except KeyError:
			break
	# 3. out
	s = ""
	for i in hash.keys():
		s = s + ("%d\n" % i)
	open("Provideversion.list", 'w').write(s)
	# 4. the end
	db.close()

if (__name__ == '__main__'):
	main(sys.argv)
