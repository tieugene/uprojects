#!/bin/env python
# -*- coding: utf-8 -*-
# 1. load ref

from __future__ import with_statement

id = {}
sig = {}

# 1. load ref
with open("keys.txt") as f:
	for line in f:
		k, v = line.split('\t')
		id[int(k, 16)] = v.rstrip('\n')
#for i in id.keys():
#	print i, id[i]
# 2. load signals
with open("signals.txt") as f:
	for line in f:
		k, v = line.split('\t')
		sig[int(k, 16)] = v.rstrip('\n')
# 3. process log
with open("out.log") as f:
	for line in f:
		data = line.split(' ')
		print "%s %s %s\t%s" % (data[0], data[1], id[int(data[2], 16)], sig[int(data[3], 16)])