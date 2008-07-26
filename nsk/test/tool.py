#!/bin/env python
# -*- coding: utf-8 -*-
# Tool to maintain NSK log
# Functions:
# - get morning enters - on today for today
# - get in/outs - for prev week
# - get in/outs - for prev mon
# TODO:
# 0. all - OK
# 1.Время прихода сотрудников до 10.00 ежедневно 24 - OK
# 2.Время прихода  и ухода сотрудников ( еженедельный отчет) 25
# 3.Время прихода и ухода ( ежемесячный отчет) 01.08
# 4.Время входа/выхода ежедневно (обед, перекур)

from __future__ import with_statement
import sys, sqlite3, optparse, datetime, time

MON = 7

def	tmp(c):
	for row in c:
		print row

def	loadDB(mon, path = '.'):
	'''
	@param mon:int - month to replace 00
	@return sqlite.connection object into memory
	'''
	# 0. prepare db
	conn = sqlite3.connect(':memory:')
	c = conn.cursor()
	c.execute("CREATE TABLE user (id INTEGER PRIMARY KEY, name TEXT)")
	c.execute("CREATE TABLE signal (id INTEGER PRIMARY KEY, name TEXT)")
	c.execute("CREATE TABLE log (ymd TEXT, hms TEXT, id INTEGER, sig INTEGER)")
	
	# 1. load data
	# 1.1. keys
	with open("keys.txt") as f:
		for line in f:
			k, v = line.split('\t')
			c.execute("INSERT INTO user VALUES (%d, '%s')" % (int(k, 16), v.rstrip('\n')))
	# 1.2. signals
	with open("signals.txt") as f:
		for line in f:
			k, v = line.split('\t')
			c.execute("INSERT INTO signal VALUES (%d, '%s')" % (int(k), v.rstrip('\n')))
	with open(path + "/out.log") as f:
		for line in f:
			data = line.split(' ')
			c.execute("INSERT INTO log VALUES ('%s', '%s', %d, %d)" % (data[0].replace("/00/", "-%02d-" % MON), data[1], int(data[2], 16), int(data[3], 16)))
	conn.commit()
	return c

def	print10am(c, d):
	'''
	Print all entering today
	@param c:cursor
	@param d:datetime.date - date
	'''
	#c.execute("SELECT user.name, MIN(log.hms) FROM user LEFT JOIN log ON (log.id = user.id) WHERE (log.sig = 56) AND (DATE(log.ymd) = DATE('%s')) GROUP BY (user.id) ORDER BY user.name" % d.isoformat())
	c.execute("CREATE VIEW minenter AS SELECT id, MIN(hms) as hms FROM log WHERE (log.sig = 56)  AND (DATE(log.ymd) = DATE('%s')) GROUP BY id" % d.isoformat())
	c.execute("SELECT user.name, minenter.hms FROM user LEFT JOIN minenter ON (user.id = minenter.id) ORDER BY user.name")
	s = []
	s.append(("Фамилия", "Приход"))
	for row in c:
		#print "%s\t%s" % (row[0].encode('utf8'), row[1].encode('utf8') if row[1] else "")
		s.append((row[0].encode('utf8'), row[1].encode('utf8') if row[1] else ""))
	print xhtml("Gutten morgen", d.isoformat(), s)

def	printInOut(c, d):
	'''
	Print all 1st entering and last exits
	@param c:cursor
	@param d:datetime.date - date
	'''
	c.execute("CREATE VIEW minenter AS SELECT ymd, id, MIN(hms) as hms FROM log WHERE (log.sig = 56) GROUP BY ymd, id ORDER BY ymd, id")
	c.execute("CREATE VIEW maxexit  AS SELECT ymd, id, MAX(hms) as hms FROM log WHERE (log.sig = 57) GROUP BY ymd, id ORDER BY ymd, id")
	c.execute("CREATE VIEW ymdid    AS SELECT DISTINCT ymd, id FROM log ORDER BY ymd, id")
	#tmp(c.execute("SELECT * FROM minenter"))
	#print "-----"
	#tmp(c.execute("SELECT * FROM maxexit"))
	#c.execute("SELECT log.ymd, MIN(log.hms), maxexit.hms, user.name FROM log LEFT JOIN maxexit ON ((log.ymd = maxexit.ymd) AND (log.id = maxexit.id)) LEFT JOIN user ON (log.id = user.id) WHERE (log.sig = 56) GROUP BY (log, ymd, log.id) ORDER BY (log.ymd, log.id)")
	#c.execute("SELECT log.ymd, MIN(log.hms), maxexit.hms, user.name FROM log LEFT JOIN maxexit ON ((log.ymd = maxexit.ymd) AND (log.id = maxexit.id)) LEFT JOIN user ON (log.id = user.id) WHERE (log.sig = 56) GROUP BY log.id ORDER BY log.ymd, log.id")
	c.execute("SELECT ymdid.ymd, minenter.hms, maxexit.hms, user.name\
		FROM ymdid\
		LEFT JOIN user     ON (ymdid.id = user.id)\
		LEFT JOIN minenter ON ((ymdid.ymd = minenter.ymd) AND (ymdid.id = minenter.id))\
		LEFT JOIN maxexit  ON ((ymdid.ymd = maxexit.ymd)  AND (ymdid.id = maxexit.id))\
		GROUP BY ymdid.ymd, ymdid.id\
		ORDER BY ymdid.ymd, ymdid.id")
	for row in c:
		print "%s\t%s\t%s\t%s" % (row[0].encode('utf8'), row[1].encode('utf8') if row[1] else "", row[2].encode('utf8') if row[2] else "", row[3].encode('utf8'))

def	printAll(c):
	'''
	Print all journal
	@param c:cursor
	'''
	c.execute("SELECT log.ymd, log.hms, user.name, signal.name FROM log LEFT JOIN user ON (log.id = user.id) LEFT JOIN signal ON (log.sig = signal.id) ORDER BY ymd, hms")
	for row in c:
		print "%s\t%s\t%s\t%s" % (row[0].encode('utf8'), row[1].encode('utf8'), row[2].encode('utf8'), row[3].encode('utf8'))

def	xhtml(t, h, s):
	'''
	Convert given table into xhtml string.
	@param t:string - title
	@param t:string - head
	@param s:string - string table (1st row is title row)
	@return string - xhtml.
	'''
	# 1. title, head, table start
	ret = "<HTML xmlns=\"http://www.w3.org/1999/xhtml\">\n\
<html>\n\
	<head>\n\
		<title>%s</title>\n\
		<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\n\
	</head>\n\
	<body>\n\
		<h1>%s</h1>\n\
		<table border=\"1\">\n\
			<thead>\n\
				<tr> " % (t, h)
	# 2. table head
	for i in s[0]:
		ret += "<th>%s</th> " % i
	# 3. table body
	ret += "</tr>\n\
			</thead>\n\
			<tbody>\n"
	for i in s[1:]:
		ret += "\t\t\t\t<tr> "
		for j in i:
			ret += "<td>%s</td> " % j
		ret += "</tr>\n"
	# 4. the end
	ret += "\t\t\t</tbody>\n\
		</table>\n\
	</body>\n\
</html>"
	return ret

def	main():
	parser = optparse.OptionParser(description="Tool to process NSK log.")
	parser.add_option("-m", "--mode",
		default	= "d",
		dest	= "mode",
		type	= "choice",
		choices	= ('d', 'w', 'm', 'a'),
		help	= "Report mode: d[ay], w[eek], m[onth] or a[ll] [default: %default].",
		metavar	= "MODE"
		)
	parser.add_option("-d", "--date",
		dest	= "date",
		type	= "string",
		default	= datetime.date.today().isoformat(),
		help	= "Date of report (in ISO format YYYY-MM-DD) [default: %default].",
		metavar	= "DATE")
	parser.add_option("-x", "--xhtml",
		dest	= "xhtml",
		action	= "store_true",
		default	= True,
		help	= "XHTML output [default]."
		)
	(options, args) = parser.parse_args()
	d = datetime.date(*time.strptime(options.date, "%Y-%m-%d")[:3])
	#if len(args) != 1:
	#	parser.error("incorrect number of arguments")
	c = loadDB(MON)
	if (options.mode == "d"):
		print10am(c, d)
	if (options.mode == "m"):
		printInOut(c, d)
	if (options.mode == "a"):
		printAll(c)
	c.close()

if __name__ == "__main__":
	main()
