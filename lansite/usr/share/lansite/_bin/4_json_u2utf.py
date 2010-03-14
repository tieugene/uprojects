#!/bin/env python
# -*- coding: utf-8 -*-
'''
Converts json from unicode to utf-8
'''
import sys, simplejson as json
reload(sys)
sys.setdefaultencoding("utf-8")
if (len(sys.argv) != 3):
	print "Usage: %s <infile> <outfile>" % sys.argv[0]
else:
	json.dump(json.load(open(sys.argv[1], "r")), open(sys.argv[2], "w"), indent=1, ensure_ascii=False, encoding="utf-8")
