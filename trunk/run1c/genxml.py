#!/usr/bin/env python
# -*- coding: utf-8 -*-

if (__name__ == '__main__'):
	u = (
		'eugene',
		'gendir',
		'tehdir',
		'comdir',
		'finance',
		'buh1',
		'hr',
		'glaveng',
		'lawyer',
		'glavbuh',
		'sale2',
		'buh2',
		'tmc'
	)
	b = (
		'ac',
		'as',
		'an',
		'ar',
		'at',
		'sc',
		'ss',
		'sn',
		'sr',
		'st',
		'ts',
		'tw'
	)
	for i in u:
		for j in b:
			print "<ub uid=\"%s\" bid=\"%s\"/>" % (i, j)
		print
