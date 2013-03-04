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
File	= []	# [?,]
Top	= []	# [[Required:bool, Alternate:bool],]

# TAGS: RPMVERSION, R[ELEASE]

def	Load():
	global Pkg, Svc, Top
	RPMd = {}
	PSd = {}
	PFd = {}
	RSd = {}
	RFd = {}

	service = {}							# service:([provider,], [requirer,])
	names = ['N', 'V', 'R', 'P', 'D', 'FILENAMES']	# 'BASENAMES', 'DIRNAMES'
	rpms = {'rpm':0, 'libFS':0}	# 'gpg-pubkey', 'kernel'
#	print "Load..."
	ts = rpm.TransactionSet()
	for h in ts.dbMatch():					# 10.7" on 1061 pkgs @ P4-1.8
		# 1. get all data of rpm
		recno = len(Pkg)					# recno = ID of pkg
		name = h['N']
#		if rpms.has_key(name):
		ver = h['V']
		rel = h['R']
		provides = h['P']
		requires = h['D']
		files = h['FILENAMES']
		# 2. optimize provides & requires - kill loopbacks, dupes, split to file/services
		providedict = dict([(i, 0) for i in provides])
		rfdict = {}
		rsdict = {}
		for i in requires:
			if (i[0] == '/'):					# file
				if not rfdict.has_key(i):		# inexists
					rfdict[i] = 0
			else:
				if not (rsdict.has_key(i) or providedict.has_key(i)):	# kill dupes and loopbacks
					rsdict[i] = 0
		rflist = rfdict.keys()
		rslist = rsdict.keys()
		# 3. sort all
		provides.sort()
		files.sort()
		rflist.sort()
		rslist.sort()
		# 4. insert
		# 4.1. RPMd
		if RPMd.has_key(name):
			name = name+"#"+ver+"-"+rel
		RPMd[name] = tuple((name, ver, rel, tuple(provides), tuple(files), tuple(rslist), tuple(rflist)))
		# 4.2. RSd
		for i in rslist:
			RSd[i] = 0
		# 4.3. RFd
		for i in rflist:
			RFd[i] = 0
		#pprint.pprint(RPMd[name])
		# 5. clean
		providedict = {}
		rfdict = {}
		rsdict = {}
		rflist = []
		rslist = []
	# II. rebuild
#	print "Rebuild..."
	# 1. rpms
	RPMl = RPMd.keys()
	RPMl.sort()
#	for i, name in enumerate(RPMl):
#		RPMd[name] = i
	# 2. Required.Services
	RSl = RSd.keys()
	RSl.sort()
	for i, name in enumerate(RSl):
		RSd[name] = i
		Svc.append([name, [], []])
	# 3. Required.Files
	RFl = RFd.keys()
	RFl.sort()
	for i, name in enumerate(RFl):
		RFd[name] = i
		File.append([name, [], []])
	# 4. X-lists
	for i, name in enumerate(RPMl):
		# 4.1. Pkg
		__ps = []
		__pf = []
		__rs = []
		__rf = []
		__r = RPMd[name]
		for j in __r[3]:		# process wanted provide.services
			if (RSd.has_key(j)):
				__ps.append(RSd[j])
		for j in __r[4]:		# process wanted provided.files
			if (RFd.has_key(j)):
				__pf.append(RFd[j])
		for j in __r[5]:		# process required.services
			__rs.append(RSd[j])
		for j in __r[6]:		# process required.files
			__rf.append(RFd[j])
		__pkg = tuple((__r[0], __r[1], __r[2], tuple(__ps), tuple(__pf), tuple(__rs), tuple(__rf)))
		Pkg.append(__pkg)
		# 4.2. Svc
		for j in __pkg[3]:
			Svc[j][1].append(i)
		for j in __pkg[5]:
			Svc[j][2].append(i)
		# 4.3. File
		for j in __pkg[4]:
			File[j][1].append(i)
		for j in __pkg[6]:
			File[j][2].append(i)
	# III. out
#	print "Pkgs:", len(Pkg), "Svc:", len(RSl), "Files:", len(RFl)	# 10.7", 1061, 1407, 88
#	pprint.pprint(Svc)
#	pprint.pprint(File)

##	# 1. add packet
##		Pkg.append((name, [], [], h['summary']))
##		Top.append([False, False])
##	# 2. add provides
##		for i in h['provides']:
##			if (service.has_key(i)):
##				service[i][0].append(recno)
##			else:
##				service[i] = ([recno], [])
##	# 3. check requires
##		for i in h['requires']:
##			if (i <> name):					# protect against loopback
##				if (service.has_key(i)):
##					service[i][1].append(recno)
##				else:
##					service[i] = ([], [recno])
##	# 4. rebuilt
###	pprint.pprint(Pkg)
##	Svc = service.items()
###	print "Rebuid..."
##	for i, s in enumerate(Svc):					# i = id of service
##		req = bool(len(s[1][1]))				# somebody requires
##		j = int(len(s[1][0]) > 1)				# 0 - 1 provider (requires), 1 - many providers
##		for p in s[1][0]:					# 4.1. provides
##			Pkg[p][1].append(i)				# can B requires XOR alternate
##			if (req):
##				Top[p][j] = True
##		for p in s[1][1]:					# 4.2. requires
##			Pkg[p][2].append(i)

def	Print():
	'''
	Debugging procedure - print all pkgs, their provides and requires
	'''
	global Pkg, Svc, Top

	for p in Pkg:
		print "%s" % p[0]
		for s in p[1]:
			print ">\t%s" % Svc[s][0]
		for s in p[2]:
			print "<\t%s" % Svc[s][0]

def	Dot():
	'''
	Output to dot.
	TODO:
		* kill loopbacks
		* kill double deps
		* kill
	'''
	global Pkg, Svc, Top
	
	print "digraph rpm {\n\trankdir=LR;"
	# 1. all rpms
	print "\tnode [shape = box];"
	for i, p in enumerate(Pkg):
		print "\t\t\"%s\"" % p[0]
	print "\t;"
	# 2. all services
	print "\tnode [shape = ellipse];"
	for i, s in enumerate(Svc):
		print "\t\t\"#%s\"" % s[0]
	print "\t;"
	# 3. all files
	print "\tnode [shape = ellipse];"
	for i, f in enumerate(File):
		print "\t\t\"@%s\"" % f[0]
	print "\t;"
	'''
	# 3. dependencies
	for i, p in enumerate(Pkg):
	# 3.1. provides
		for j in p[1]:
			print "\t\"%s\" -> \"%s\"" % (p[0], Svc[j][0])
	# 3.2. requires
		for j in p[2]:
			print "\t\"%s\" -> \"%s\"" % (Svc[j][0], p[0])
	'''
	# 3. dependencies
	# 3.1 Services
	for s in Svc:
	# 3.1.1. providers
		for j in s[1]:
			print "\t\"%s\" -> \"#%s\"" % (Pkg[j][0], s[0])
	# 3.1.2. requirers
		for j in s[2]:
			print "\t\"#%s\" -> \"%s\"" % (s[0], Pkg[j][0])
	# 3.2 Files
	for f in File:
	# 3.2.1. providers
		for j in f[1]:
			print "\t\"%s\" -> \"@%s\"" % (Pkg[j][0], f[0])
	# 3.2.2. requirers
		for j in f[2]:
			print "\t\"@%s\" -> \"%s\"" % (f[0], Pkg[j][0])
	print "}"

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
	#PrintTop(True)
	Dot()

if (__name__ == '__main__'):
	main(sys.argv)
