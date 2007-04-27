#!/bin/env python
# -*- coding: utf-8 -*-
'''
script to dump rpm database files - using rpm.
v.060623
TODO:
	* make modes:
		- required only
		- required and alternate
		- alternate only
	* summary
	* sort
'''

import sys, rpm, pprint

Pkg	= []	# [(name, [provides,], [requires,]),]
Svc	= []	# [(name, [provider,], [requirer,]),]
Top = []	# [[Required:bool, Alternate:bool],]

def	Load():
	global Pkg, Svc, Top

	service = {}							# service:([provider,], [requirer,])
#	print "Load..."
	ts = rpm.TransactionSet()
	for h in ts.dbMatch():
		recno = len(Pkg)
		name = h['name']
	# 1. add packet
		Pkg.append((name, [], [], h['summary']))
		Top.append([False, False])
	# 2. add provides
		for i in h['provides']:
			if (service.has_key(i)):
				service[i][0].append(recno)
			else:
				service[i] = ([recno], [])
	# 3. check requires
		for i in h['requires']:
			if (i <> name):						# protect against loopback
				if (service.has_key(i)):
					service[i][1].append(recno)
				else:
					service[i] = ([], [recno])
	# 4. rebuilt
#	pprint.pprint(Pkg)
	Svc = service.items()
#	print "Rebuid..."
	for i, s in enumerate(Svc):
		req = bool(len(s[1][1]))		# somebody requires
		j = int(len(s[1][0]) > 1)	# 0 - 1 provider (requires), 1 - many providers
		for p in s[1][0]:				# 4.1. provides
			Pkg[p][1].append(i)		# can B requires XOR alternate
			if (req):
				Top[p][j] = True
		for p in s[1][1]:				# 4.2. requires
			Pkg[p][2].append(i)

'''def	Print():
	global Pkg, Svc, Top

	for p in Pkg:
		print "%s\n\tProvides:" % p[0]
		for s in p[1]:
			print "\t\t%s" % Svc[s][0]
		print "\tRequires:"
		for s in p[2]:
			print "\t\t%s" % Svc[s][0]
'''
def	PrintTop(alt = False):
	'''
	Print top rpms - by scanning Top:
	F F - free => print
	F T - alternated => print if alt==True
	T F - wanted => not print
	T T - wanted => not print
	'''
	global Pkg, Svc, Top
	tmp = []
	maxlen = 0

	# 1. select tops (and calc max len of rpm name)
	for i, p in enumerate(Top):
		if ((not p[0]) and (alt or not(p[1]))):
			tmp.append((Pkg[i][0], Pkg[i][3].replace("\n", "")))
			maxlen = max(maxlen, len(Pkg[i][0]))
	# 2. sort
	tmp.sort()
	# 3. out
	for i in tmp:
		print "%s %s" % (i[0].ljust(maxlen), i[1])

def	main(argv):
	global Pkg, Svc, Top

	Load()
	PrintTop(True)

if (__name__ == '__main__'):
	main(sys.argv)
