#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

curoid		= None	# current OKSO id
curoname	= None	# current OKSO name
curqid		= None	# current
qual		= []

Reader = csv.reader(open('okso_raw.txt'), delimiter='\t')
for s in Reader:
	oid	= int(s[0].strip())			if s[0].strip() else None
	oname	= unicode(s[1].strip(), "utf-8")	if s[1].strip() else None
	qid	= int(s[2].strip())			if s[2].strip() else None
	qname	= unicode(s[3].strip(), "utf-8")	if s[3].strip() else None
	if (oid):
		print oid, oname
		#print u'%d\t%s' % (oid, oname)
		curoid = oid
		curoname = oname
	if (qname):
		if (qid):
			curquid = qid
		qual.append((curoid, curquid, qname))
#for q in qual:
#	print u'%d\t%d\t%s' % q
