#!/usr/bin/python

# by pmatilai@laiskiainen.org, licensed under the GPL

import rpm
import sys

ts = rpm.TransactionSet()
justlibs = 1

if len(sys.argv) > 1 and sys.argv[1] == "-a":
	justlibs = 0

req = {}
orphan = []

for h in ts.dbMatch('name'):
	name = h['name']
	if not h[rpm.RPMTAG_REQUIRENAME]:
		continue
	for r in h[rpm.RPMTAG_REQUIRENAME]:
		req[r] = name

for h in ts.dbMatch('name'):
	name = h['name']
	preq = 0
	prov = []
	if justlibs:
		#if h['group'].find('Libraries') == -1:
			#continue
		for p in h[rpm.RPMTAG_PROVIDES]:
			if p.find('.so') != -1:
				prov.append(p)
		if not prov:
			continue
	for p in h[rpm.RPMTAG_PROVIDES] + h[rpm.RPMTAG_FILENAMES]:
		if req.has_key(p):
			preq = preq + 1

	if preq == 0:
		orphan.append(name)

orphan.sort()
for p in orphan:
	print p

