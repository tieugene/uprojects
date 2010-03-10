#!/bin/env python
import sys
if (len(sys.argv) != 3):
	print "Usage: %s <infile> <outfile>"
else:
	open(sys.argv[2],"wb").write(open(sys.argv[1]).read().decode("unicode_escape").encode("utf8"))