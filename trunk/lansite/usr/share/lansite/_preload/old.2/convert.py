#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
convert old refs into new:
	* job: +okdp.names
	* okso: need only
	* skill: need only
'''

import sys, csv

reload(sys)
sys.setdefaultencoding( "utf-8" )

def	__get_bool(s):
	return (s.strip() == '1')

def	__get_int(s):
	return int(s.strip())			if s.strip() else None

def	__get_str(s):
	return unicode(s.strip(), "utf-8")	if s.strip() else None

def	__get_reader(s):
	return csv.reader(open('%s' % s), delimiter='\t')

def	cvt_job():
	print 'Jobs'
	# 1. load okdp
	okdp = dict()
	for s in __get_reader('old/okdp.txt'):
		okdp[__get_str(s[0])] = __get_str(s[1])
	# 2. load job, out job
	f = open("job.txt", "w")
	for s in __get_reader('old/job.txt'):
		f.write("%s\t%s\t%s\n" % (s[0], s[1], okdp[s[1]]))
	f.close()

def	cvt_okso():
	print 'OKSO'
	# 1. load stageokso
	stageokso = dict()
	for s in __get_reader('stageokso.txt'):
		stageokso[s[1]] = True
	# 2. okso
	f = open("okso.txt", "w")
	for s in __get_reader('old/okso.txt'):
		if stageokso.has_key(s[0]):
			f.write("%s\t%s\n" % (s[0], s[1]))
	f.close()
	# 3. skill
	f = open("skill.txt", "w")
	for s in __get_reader('old/skill.txt'):
		if stageokso.has_key(s[0]):
			f.write("%s\t%s\t%s\n" % (s[0], s[1], s[2]))
	f.close()

if (__name__ == '__main__'):
	cvt_job()
	cvt_okso()
