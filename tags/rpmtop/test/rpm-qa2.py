#!/bin/env python
# -*- coding: utf-8 -*-
'''
Show all installed rpms - via rpm interface
'''

import rpm

ts = rpm.TransactionSet()
for h in ts.dbMatch():
	print h['name']
