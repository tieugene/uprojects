#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

if (__name__ == '__main__'):
	#a = ['"C:\\1C\\BIN\\1cv7s.exe"', '"/DC:\\\\1C\\\\Data\\\\ATC"']
	a = ['"C:\\\\1C\\\\BIN\\\\1cv7s.exe"']
	print a[0]
	#os.execv('/usr/bin/wine', a)
	os.system('/usr/bin/wine "C:\\\\1C\\\\BIN\\\\1cv7s.exe"')
