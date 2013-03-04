#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
script to dump rpm database files - via db4 interface.
'''
import bsddb, sys, struct

# global vars
##Pkg_Count = 0	# qty of packages (counted due loading Providename)
##Pkg_Array = []	# Packages: (name:string, required:bool, alternate:bool)
debugmode = 0
alternate = True
Pkg_Hash = {}	# Provides: PkgNo:(Name, Rq, Alternated)
Prv_Hash = {}	# Provides: name:(pkgno, ...)
Rq_Hash = {}	# Required hash: pkgno:[rq:bool, alt:bool]

# ---	Utility ---
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
	stop = 0
	db = bsddb.hashopen(dbname, 'r')
	k, v = db.first()
	while 1:
		try:
			Process_Func(k, s2i(v))
			# <debug>
##			stop += 1
##			if (stop == 10):
##				sys.exit(0)
##			# </debug>
			k, v = db.next()
		except KeyError:
			break
	db.close()

# ---	DB processors ---
def	Process_Name(k, v):
	'''
	Process each record of Name.
	@param k:string - key
	@param v:int_array[1] - value
	'''
	global Pkg_Hash
	Pkg_Hash[v[0]] = [k, False, False]			# store Pkg_No:[Name, Rq, Alt]

def	Process_Providename(k, v):
	'''
	Process each record of Providename.
	@param k:string - key
	@param v:int_array - values
	'''
	global Prv_Hash
	# 1. drop dupes
	if (len(v) == 1):
		Prv_Hash[k] = v
	else:
		# sort values
		h = {}
		for i in v:					# sort() not works (?!)
			h[i] = None
		v = h.keys()
		a  = v[0:]					# copy start element
		current = v[0]
		for i in v[1:]:
			if i <> current:
				a.append(i)
				current = i
			else:				# skip duplicated provider
				print "Providename: % provider duplicated" % k
		Prv_Hash[k] = a[:]			# 1. store Providename

def	Process_Requirename(k, v):
	'''
	Process each record of Requirename.
	@param k:string - key
	@param v:int_array - values
	'''
	global debugmode, Pkg_Hash, Prv_Hash, Rq_Hash
	prv = Prv_Hash.get(k)
	if (prv):									# found in provides
		OneProvider = (len(prv) == 1)
		for r in v:								# each required packet no
			if (OneProvider):					# Case [?:1]: one provider (== no one alternatives)
				if (prv[0] <> r):				# Case [?:1.ex]: requirer <> provider
					Pkg_Hash[r][1] = True		# Pkq = required, ?
##				else:						# Case [?:1.in]: required by provider
##					pass						# skip
			else:							# Case [?:M]: multiprovided service
				try:							# search for required == provider
					prv.index(r)				# Case [?:M.i]: requirer in provider => skip
				except ValueError:				# Case [?:M.e]: requirer not in provider
					Pkg_Hash[r][2] = True		# Pkq = ?, Alternate
	else:									# Case [1:0]: no one provides
		if (debugmode == 2):
			print "Service '%s' nobody provides" % k

def	Out_Results():
	'''
	dump db hash
	'''
	global debugmode, Pkg_Hash
	for p in Pkg_Hash.values():
		if (not (p[1])):
			print p[0]

# ---	main ---
def	main(argv):
	# 0. preparing
	global debugmode, Pkg_Count
	base = '/var/lib/rpm/'	# rpm DB base path
	# 1. Load 'Name'
	if (debugmode):
		print "Loading Name..."
	Load_DB(base + 'Name', Process_Name)
	# 2. Load 'Providename' - for loopback checking
	if (debugmode):
		print "Loading Providename..."
	Load_DB(base + 'Providename', Process_Providename)
	# 3. Process 'Requirename' - set wanted packages
	if (debugmode):
		print "Loading Requirename..."
	Load_DB(base + 'Requirename', Process_Requirename)
	# 4. out results
	Out_Results()

if (__name__ == '__main__'):
	main(sys.argv)
