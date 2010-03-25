#!/bin/env python
# -*- coding: utf-8 -*-
'''
Convert INN and OGRNss from int to str
'''
import sys, simplejson as json
reload(sys)
sys.setdefaultencoding("utf-8")
if (len(sys.argv) != 2):
	print "Usage: %s <infile>" % sys.argv[0]
else:
	data = json.load(open(sys.argv[1], "r"))
	for i in data:
		if (i['model'] == 'sro2.org'):
			# INN
			a = i['fields']['inn']
			if (a <= 9999999999):
				s = "%010d" % a
			else:
				s = "%012d" % a
			i['fields']['inn'] = s
			# OGRN
			a = i['fields']['ogrn']
			if (a <= 9999999999999):
				s = "%013d" % a
			else:
				s = "%015d" % a
			i['fields']['ogrn'] = s
			# KPP
			a = i['fields']['kpp']
			if (a != None):
				i['fields']['kpp'] = "%09d" % a
	json.dump(data, open(sys.argv[1], "w"), indent=1, ensure_ascii=False, encoding="utf-8")
