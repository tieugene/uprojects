#!/bin/env python
# -*- coding: utf-8 -*-
# 1. load ref

from __future__ import with_statement
import datetime, time

id = {}		# {key: (no, surname)}
no = []
summary = []	# [[date, [beg, end], ...], ...]
unknown = {}

def	flushline(d, l):
	#return
	print "<tr><td>%s</td>" % d
	for i in l:
		print "\t<td>%s</td><td>%s</td>" % (i[0] if i[0] else "&nbsp;", i[1] if i[1] else "&nbsp;")
	print "</tr>"

# 1. load ref
with open("keys.txt") as f:
	for i, line in enumerate(f):
		k, v = line.split('\t')
		key = int(k, 16)
		id[key] = (i, v.strip())
		no.append(key)

#for i in id.keys():
#	print i, id[i][0], id[i][1]
# 2. process log
	with open("out.log") as f:
		imax = i + 1
		curdate = None
		print "<html>\n<head>\n<title>Graphics</title>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\n</head>\n<body>\n<table border=\"1\">\n<thead>\n<tr>\n<th>Date</th>"
		for i in no:
			print "<th colspan=\"2\">%s</th>" % id[i][1]
		print "</thead>\n<tbody>"
		for line in f:
			data = line.split(' ')	# date | time | key | event
			ymd	= datetime.date(*time.strptime(data[0], "%Y/%m/%d")[0:3])
			hms	= datetime.time(*time.strptime(data[1], "%H:%M:%S")[3:6])
			key	= int(data[2], 16)
			evt	= 0 if (int(data[3], 16) == 56) else 1	# in == 0; out == 1
			if ((curdate == None) or (ymd > curdate)):
				if (curdate):
					flushline(curdate, curline)
				curdate = ymd
				#curline = [[None, None]]*imax
				curline = []
				for i in xrange(imax):
					curline.append([None, None])
			if (key in id):
				curline[id[key][0]][evt] = hms
				#print "%s\t%s\t%s\t%s" % (ymd, data[1], surname, evt)
			else:
				unknown[key] = True
		flushline(curdate, curline)
		print "</tbody>\n</table>"
		if (unknown):
			print "Unknown keys:<ul>"
			for i in unknown.keys():
				print "<li>%d</li>" % i
			print "</ul>"
		print "</body></html>"
