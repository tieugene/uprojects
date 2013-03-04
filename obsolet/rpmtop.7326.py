#!/bin/env python
# -*- coding: utf-8 -*-
'''
script to dump rpm database __lf - using rpm.
v.070320
TODO:
	* make modes:
		- required only
		- required and alternate
		- alternate only
	* summary
	* sort
	* options
print: a2ps -R --columns=1 -f6 -B -o rpmtop.ps rpmtop.py
'''

import sys, rpm

Pkg	= []	# [(__name, [__lp,], [__lr,]),]
Svc	= []	# [(__name, [provider,], [requirer,]),]
File	= []	# [?,]

def	main(argv):
	global Pkg, Svc, File

	# 0. make vars
	_dG	= {}	# Pkgs dict: {__name: (__name, __ver, __rel, (prov.s), (prov.f), (req.s), (req.f))}
	_dRS	= {}	# ReqSvc dict: name
	_dRF	= {}	# ReqFile dict: name

	# I. Load raw data (w/ lite optimization)
	#	In:	none
	#	Thru:	none
	#	Out:	_dG, _dRS, _dRF
	#	Tmp:	i, __recno, __name, __ver, __rel, __dpf, __drf, __drs, __lp, __lf, __lrs, __lrf
	ts = rpm.TransactionSet()
	for h in ts.dbMatch():							# for each pkg
		# 1. get all data of rpm
		__name	= h['N']
		__ver	= h['V']
		__rel	= h['R']
		__lp	= h['P']						# list of provided services : strings
		__lr	= h['D']						# list of required services/files : strings
		__lf	= h['FILENAMES']					# list of provided files : strings
		__drf	= {}							# dict of required files    - for __lrf
		__drs	= {}							# dict of required services - for __lrf
		__lp.sort()
		__lf.sort()
		# 2. optimize __lp & __lr:
		#	- split file/service
		#	- kill loopbacks
		#	- kill dupes
		__dp = dict([(i, 0) for i in __lp])				# dict of provided - for __lr check (loops/dupes))
		for i in __lr:
			if (i[0] == '/'):					# file
				if not __drf.has_key(i):			# inexists
					__drf[i] = 0
			else:
				if not (__drs.has_key(i) or __dp.has_key(i)):	# kill dupes and loopbacks
					__drs[i] = 0
		__lr = []
		__dpf = {}
		# 3. sort all
		__lrf = __drf.keys()
		__drf = {}
		__lrf.sort()
		__lrs = __drs.keys()
		__drs = {}
		__lrs.sort()
		# 4. make _dG, _dRS, _dRF by __lp, __lf, __lrs, __lrf
		# 4.1. _dG < __name, __ver, __rel, __lp, __lf, __lrs, __lrf
		if _dG.has_key(__name):
			__name = __name+"#"+__ver+"-"+__rel
		_dG[__name] = tuple((__name, __ver, __rel, tuple(__lp), tuple(__lf), tuple(__lrs), tuple(__lrf)))
		# 4.2. _dRS < __lrs
		# _dRS = dict({i: 0} for i in __lrs)
		for i in __lrs:
			_dRS[i] = 0
		__lrs = []							# clean
		# 4.3. _dRF < __lrf
		for i in __lrf:
			_dRF[i] = 0
		__lrf = []							# clean

	# II. prepare tmp data
	#	In:	_dG, _dRS, _dRF
	#	Thru:	_dG, _dRS, _dRF
	#	Out:	_dRS, _dRF, _lG, Svc, File
	#	Tmp:	i, __name, __lrs, __lrf
	# 1. rpms
	_lG = _dG.keys()
	_lG.sort()
	# 2. Required.Services
	__lrs = _dRS.keys()
	__lrs.sort()
	for i, __name in enumerate(__lrs):
		_dRS[__name] = i
		Svc.append([__name, [], []])
	__lrs = []								# clean
	# 3. Required.Files
	__lrf = _dRF.keys()
	__lrf.sort()
	for i, __name in enumerate(__lrf):
		_dRF[__name] = i
		File.append([__name, [], []])
	__lrf = []								# clean

	# III. Make out data structures
	#	In:	_dG[][0..2], _dRS, _dRF, _lG
	#	Out:	Pkg, Svc, File
	#	Tmp:	i, j, __pkg, __name, __lps, __lpf, __lrs, __lrf, __r
	for i, __name in enumerate(_lG):
		# 4.1. Pkg
		# 4.1.1. declare/clean vars
		__lps = []							# list of services IDs (in Svc)  this pkg __lp
		__lpf = []							# list of __lf    IDs (in File) this pkg __lp
		__lrs = []							# list of services IDs (in Svc)  this pkg __lr
		__lrf = []							# list of __lf    IDs (in File) this pkg __lr
		__r = _dG[__name]						# record from pkg hash (__names)
		# 4.1.2. lets go
		for j in __r[3]:						# process wanted provide.services
			if (_dRS.has_key(j)):
				__lps.append(_dRS[j])
		for j in __r[4]:						# process wanted provided.__lf
			if (_dRF.has_key(j)):
				__lpf.append(_dRF[j])
		for j in __r[5]:						# process required.services
			__lrs.append(_dRS[j])
		for j in __r[6]:						# process required.__lf
			__lrf.append(_dRF[j])
		__pkg = tuple((__r[0], __r[1], __r[2], tuple(__lps), tuple(__lpf), tuple(__lrs), tuple(__lrf)))
		Pkg.append(__pkg)
		# 4.2. Svc
		for j in __pkg[3]:
			Svc[j][1].append(i)					# add pkg ID in Svc's 'provided by'
		for j in __pkg[5]:
			Svc[j][2].append(i)					# add pkg ID in Svc's 'required by'
		# 4.3. File
		for j in __pkg[4]:
			File[j][1].append(i)
		for j in __pkg[6]:
			File[j][2].append(i)

	# III. make Tops
	#	In:	Svc, File, Pkg
	#	Out:	Tops
	#	Tmp:	i, __pkg
	Tops = [False] * len(_dG)
	for i in Svc:								# each service
		for j in i[1]:							# each hist provider
			Tops[j] = True
	for i in File:								# each service
		for j in i[1]:							# each hist provider
			Tops[j] = True
	# IV. out
	for i, __pkg in enumerate(Pkg):
		if not Tops[i]:
			print __pkg[0]

if (__name__ == '__main__'):
	main(sys.argv)
