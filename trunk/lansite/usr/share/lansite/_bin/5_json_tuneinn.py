#!/bin/env python
# -*- coding: utf-8 -*-
'''
Convert INN from int to str
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
			inn = i['fields']['inn']
			if (inn <= 9999999999):
				sinn = "%010d" % inn
			else:
				sinn = "%012d" % inn
			i['fields']['inn'] = sinn
	json.dump(data, open(sys.argv[1], "w"), indent=1, ensure_ascii=False, encoding="utf-8")
