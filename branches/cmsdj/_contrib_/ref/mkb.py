#!/bin/env python
# -*- coding: utf-8 -*-
# convert pmu from json to 3 refs (sql)

import sys, json

reload(sys)
sys.setdefaultencoding("utf-8")

# 1. load
j = json.load(open("mkb10.json", "r"), "utf-8")
# 2. parse
def ifnone(v):
    if (v == None):
        return 'NULL'
    else:
        return "'%s'" % (v.replace("'", "''"))

for i in j:
    print "INSERT INTO ref_mkb10 (id, parent_id, name, comments) VALUES ('%s', %s, %s, %s);" % (i[2], ifnone(i[4]), ifnone(i[1]), ifnone(i[6]))
