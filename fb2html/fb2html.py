#!/bin/env python
# -*- coding: utf-8 -*-
'''
Tool to convert FB2 documents into HTML
'''

import sys
from elementtree.ElementTree import ElementTree

def	main(argv):
	root = ElementTree(sys.argv[0])
	iter = root.getiterator()

if (__name__ == '__main__'):
	main(sys.argv[1:])
