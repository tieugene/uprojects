#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''script to dump rpm database files - via db4 interface.'''
import bsddb, sys, struct, pprint

def	s2i(s):
	return ("%02X" * len(i) % i)

def	main(argv):
	hash = {}
	# 1. open db
	db = bsddb.btopen('/var/lib/rpm/Installtid', 'r')
#	pprint.pprint(db.keys())
	# 2. process each record
	for k, v in db.iteritems():
		print db.get(k)
#			i = struct.unpack("<%dI" % (len(v)/4), v)			# convert
#			l = len(v)
#			print "%s\t%d\t%s" % (k, len(v), (" %04X" * len(i) % i))	# out
#			for j in i[::2]:						# store
#				hash[j] = True
#			print v
#			k, v = db.next()
	# 3. out
#	s = ""
#	for i in hash.keys():
#		s = s + ("%d\n" % i)
#	open("Provideversion.list", 'w').write(s)
	# 4. the end
	db.close()

if (__name__ == '__main__'):
	main(sys.argv)
