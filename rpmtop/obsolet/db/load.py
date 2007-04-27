# -*- coding: utf-8 -*-
'''
Load rpm database into RAM - from Berkley DBs.
'''

import bsddb, sys, struct, pprint
import gvar

Pkg_hash = {}	# Provides: {Name : oldN}
Svc_hash = {}	# Provides: name:([pkgno,], [rqno,])
ID2P = {}		# Old-2New pkg ID converter: [ID] = newN

# 1.	---- Utility ----
def	DebugPrint(msg):
	if (gvar.debugmode):
		print msg

def	newID(id):
	global ID2P
	if (ID2P.has_key(id)):
		return ID2P[id]
	else:
		return -1

def	s2i(s):
	'''
	converts string to array of int - splitting s by 4 bytes (H=2, I,L=4, Q=8 bytes).
	@param s:string - value
	@return - sorted list of ints (skipped 2x)
	'''
	return struct.unpack("<%dI" % (len(s)/4), s)[::2]

def	Load_DB(dbname, Process_Func):
	'''
	Load db from file db.
	@param dbname:str - filename of database.
	@param Process_Func:func - function to process each record
	'''
	db = bsddb.hashopen(dbname, 'r')
	for k, v in db.iteritems():
		Process_Func(k, s2i(v))
	db.close()

# 2.	---- DB processors ----
	'''
	Process each record of Name.
	@param k:string - key
	@param v:int_array[1] - value
	'''

def	Process_Name(k, v):
	global Pkg_hash
	Pkg_hash[k] = v[0]

def	Process_Providename(k, v):
	global ID2P, Svc_hash
	DebugPrint("Proc:\t%s\t%d" % (k, v[0]))
	# 1. drop dupes
	v = list(v)
	v.sort()
	p = []
	current = 0												# ID starts w/ 1
	for i in v:
		if (i > current):
			current = i
			id = newID(i)
			if (id < 0):										# not found
				id = len(gvar.Pkg)							# 1. newID
				ID2P[i] = 	id									# 2. add to ID2P
				gvar.Pkg.append(("____%04X" % i, [], []))	# 3. new Pkg
			p.append(id)
	Svc_hash[k] = (p, [])										# provider and emty requirer

def	Process_Requirename(k, v):
	global Pkg_Hash, Svc_Hash
	prv = Svc_hash.get(k)
	if (prv):									# found in provides
		pass
##		OneProvider = (len(prv) == 1)
##		for r in v:								# each required packet no
##			if (OneProvider):					# Case [?:1]: one provider (== no one alternatives)
##				if (prv[0] <> r):				# Case [?:1.ex]: requirer <> provider
##					Pkg_hash[r][1] = True		# Pkq = required, ?
####				else:						# Case [?:1.in]: required by provider
####					pass						# skip
##			else:							# Case [?:M]: multiprovided service
##				try:							# search for required == provider
##					prv.index(r)				# Case [?:M.i]: requirer in provider => skip
##				except ValueError:				# Case [?:M.e]: requirer not in provider
##					Pkg_hash[r][2] = True		# Pkq = ?, Alternate
	else:									# Case [1:0]: no one provides
##		if (debugmode == 2):
		print "Service '%s' nobody provides" % k	# files (e.g. /sbin/service)

# 3.	---- Rebuilders ----
def	Rebuild_Pkg():
	'''	Reorder Name hash into arrays of (Name, [], []) tuples.'''
	global Pkg_hash, ID2P
	items = Pkg_hash.items()
	items.sort()
	l = len(items)
	gvar.Pkg = [(items[i][0], [], []) for i in xrange(l)]		# make Pkg array
	for i, item in enumerate(items):							# make ID2P array
		ID2P[item[1]] = i

def	Rebuild_Svc():
	'''
	Reorder Providename hash into Pkg[1] and array of (Name, provider, [])
	'''
	global Svc_hash
	items = Svc_hash.items()					# sorted by keys !
	items.sort()
	for i, item in enumerate(items):
		for id in item[1][0]:
			gvar.Pkg[id][1].append(i)
		gvar.Svc.append((item[0], item[1], []))

# 4.	---- main ----
def	OutResults():
	global ID2P
	# Pkg
	s = ""
	for i, p in enumerate(gvar.Pkg):
		s = s + ("%d\t%s\n" % (i, p[0]))
	open("data/p.txt", 'w').write(s)
	# ID2P
	s = ""
	v = ID2P.keys()
	v.sort()
	for i in xrange(len(v)):
		s = s + ("%d\t%s\n" % (v[i], newID(v[i])))
	open("data/id.txt", 'w').write(s)
	# Providename
	s = ""
	for i in gvar.Svc:
		s = s + ("%s\t%s\n" % (i[0], str(i[1])))
	open("data/s.txt", 'w').write(s)

def	Load(base):
	gvar.debugmode = 0
	Load_DB(base + 'Name', Process_Name)					# 1. Name
	Rebuild_Pkg()												# 2. Rebuild them (and make ID2P)
	Load_DB(base + 'Providename', Process_Providename)	# 3. Providename (for loopback checking etc)
	Load_DB(base + 'Requirename', Process_Requirename)	# 4. Requirename (wanted packages)
	Rebuild_Svc()												# 5. Rebuid services
#	OutResults()
