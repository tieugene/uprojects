#!/bin/env python
# -*- coding: utf-8 -*-
# convert skmu from json to 3 refs (sql)

import sys, json

reload(sys)
sys.setdefaultencoding("utf-8")

# 0. prepare
f1 = open("skmu1.sql", "w")
m1 = "INSERT INTO ref_skmu1 (id, name) VALUES (%d, '%s');\n"
f2 = open("skmu2.sql", "w")
m2 = "INSERT INTO ref_skmu2 (id, name) VALUES (%d, '%s');\n"
f3 = open("skmu3.sql", "w")
m3 = "INSERT INTO ref_skmu3 (id, c1, c2, c3, name) VALUES (%d, %d, %d, %d, '%s');\n"
d2 = dict()

# 1. load
j = json.load(open("skmu_data.json", "r"), "utf-8")
# 2. parse
for i in j:
    c = i[2].split('.')
    n = i[1]
    l = len(c)
    if l == 1:  # id, name
        f1.write(m1 % (int(c[0]), n))
    elif l == 2:    # id, name
        ic = int(c[1])
        if not ic in d2:
            d2[ic] = n
            f2.write(m2 % (ic, n))
    else:   # id, id1, id2, id3, name
        f3.write(m3 % (int(i[2].replace('.', '')), int(c[0]), int(c[1]), int(c[2]), n))
