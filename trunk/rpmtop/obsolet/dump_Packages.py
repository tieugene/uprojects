#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
script to dump rpm Berkley DB database file.
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
Rec_Hash = {}

# ---	Utility ---
def	s2i(s):
	'''
	converts string to array of int - splitting s by 4 bytes (H=2, I,L=4, Q=8 bytes).
	@param s:string - value
	@return - sorted list of ints (skipped 2x)
	'''
	return struct.unpack("<%dI" % (len(s)/4), s)[::2]

def	w2i(s):
	'''
	converts string[4] to int.
	@param s:string - value
	@return - ints
	'''
	return struct.unpack("<I", s)[0]

def	Load_DB(dbname, Process_Func, maxrec = None):
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
			Process_Func(k, v)
			if (maxrec):
				stop += 1
				if (stop == maxrec):
					break
			k, v = db.next()
		except KeyError:
			break
	db.close()

# ---	DB processors ---
def	Process_Package(k, v):
	'''
	Process each record of Name.
	@param k:string - key
	@param v:int_array[1] - value
	'''
	global Pkg_Hash
	Pkg_Hash[w2i(k)] = v				# store Pkg_No:[Name, Rq, Alt]

def	Process_Record(k, v):
	'''
	Process each record of Name.
	@param k:string - key
	@param v:int_array[1] - value
	'''
	global Pkg_Hash
	Pkg_Hash[k] = v

def	Out_Results():
	'''
	dump db hash
	'''
	global debugmode, Pkg_Hash, Rec_Hash
	for p in Pkg_Hash.items():
		fn = "%04X" % p[0]
		open(fn, 'w').write(p[1])
#		Rec_Hash = {}
#		Load_DB(fn, Process_Record)
#		for r in Rec_Hash.items():
#			print "Key(%d):\n%s\nValue(%d):\n%s" % (len(r[0]), r[0], len(r[1]), r[1])

# ---	main ---
def	main(argv):
	# 0. preparing
	global debugmode, Pkg_Count
	base = '/var/lib/rpm/'	# rpm DB base path
	# 1. Load 'Name'
	Load_DB(base + 'Packages', Process_Package, 5)
	# 4. out results
	Out_Results()

if (__name__ == '__main__'):
	main(sys.argv)
