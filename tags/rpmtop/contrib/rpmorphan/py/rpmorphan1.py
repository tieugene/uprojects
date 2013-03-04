#!/usr/bin/python

import rpm

ts = rpm.TransactionSet()

req = {}
orphan = []

for h in ts.dbMatch():
    name = h['name']
    if not h[rpm.RPMTAG_REQUIRENAME]:
        continue
    for r in h[rpm.RPMTAG_REQUIRENAME]:
        req[r] = name

for h in ts.dbMatch():
    name = h['name']
    preq = 0
    for p in h[rpm.RPMTAG_PROVIDES] + h[rpm.RPMTAG_FILENAMES]:
        if req.has_key(p):
            preq = preq + 1

    if preq == 0:
        orphan.append(name)

orphan.sort()
for name in orphan:
    print orphan
