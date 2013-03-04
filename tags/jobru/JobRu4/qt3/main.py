#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
main module.
'''

import sys
import data, db, gui, utility, parser

def	PrintDebug(l, s):
	if (data.DebugLevel >= l):
		print s

def	RemoveScripts(text):
	return text.split("<hr ", 1)[0].replace("&amp;", "and")	# cut bottom, replace amp;amp;amp

def	CmpLists (llist, rlist, rdict, func):
	'''
	Compare 2 lists (by date).
	@param llist:list**2 - records to find
	@param rlist:list**2 - list**2 to compare with (right)
	@param rdict:dict - dict of rlist ID:RecNo
	@return
		list - what to do (0 = not found, 1 = lt, 2 = eq, 3 = gt)
		dict - dict of ID:Rec# of left list
	'''
	for li in xrange(len(llist)):	# left Rec#
		lrec = llist[li]		# left record
		lid = lrec[0]			# left ID
		if (not rdict.has_key(lid)):
			cmpresult = 0
		else:
			cmpresult = cmp(lrec[1], rlist[rdict[lid]][1]) + 2
		func(cmpresult, lrec, rlist, rdict)

def	AddHTMLBuffer(c, lr, rl, rd):
	'''
	append records from one
	@param c:int - compare result (0..3)
	@param lr:list - src record
	@param rl:list**2 - dst list of records
	@param rd:dict - rl's dict of ID:RecNo
	'''
	if (c == 0):	# 0: not found => append
		rd[lr[0]] = len(rl)
		rl.append(lr)
	elif (c == 1):	# 1: younger => skip
		PrintDebug(1, "I: %d already exists in mem, but younger. Skip." % lr[0])
	elif (c == 2):	# 2: eq => skip
		PrintDebug(1, "I: %d already exists in mem, and equal. Skip." % lr[0])
	else:		# 3: older => update
		PrintDebug(1, "I: %d already exists in mem, but older. Update." % lr[0])
		rl[rd[lr[0]]] = lr

def	TrySaveData(c, lr, rl, rd):
	'''
	Try save data from mem to DB - insert or update
	@param c:int - compare result (0..3)
	@param lr:list - src record (mem)
	@param rl:list**2 - dst list of records (db)
	@param rd:dict - rl's dict of ID:RecNo
	'''
	lr[ 1] = lr[ 1].isoformat(' ')		# DateTime
	lr[19] = 1					# New
	if (c == 0):	# 0: not found => insert
		lr[20] = 0				# Priority
		data.DataBase.InsertRecord(tuple(lr))
	elif (c == 1):	# 1: younger => skip
		PrintDebug(1, "I: %d already exists in DB, but younger. Skip." % lr[0])
	elif (c == 2):	# 2: eq => skip
		PrintDebug(1, "I: %d already exists in DB, and equal. Skip." % lr[0])
	else:		# 3: older => update
		PrintDebug(1, "I: %d already exists in DB, but older. Update." % lr[0])
		lr[20] = rl[rd[lr[0]]][20]		# Priority (copy from DB)
		data.DataBase.UpdateRecord(tuple(lr))

def	ImportFromHTML(filelist):
	'''
	Import data from HTML-file
	'''
	# 0. prepare vars
	d = []
	IDs = {}
	db_dict = {}
	# 1. add all html-files into mem
	PrintDebug(1, "I: Processing files")
	for f in filelist:
		PrintDebug(1, "%s..." % f)
		# 1.1. get new data from a file
		onedlist = data.Parser.LetsGo(RemoveScripts(open(f,"r").read()))
		if (onedlist):
			# 1.2. add to summary recordset
			CmpLists(onedlist, d, IDs, AddHTMLBuffer)
	# 2. Try save into DB
	if (len(d)):
		PrintDebug(1, "Saving data to DB")
		# 2.1. check weather this IDs in DB
		data.DataBase.Exec(data.DataBase.SQL_Select + "WHERE ID IN (%s" + (len(d) - 1) * ", %s" + ")", IDs.keys())
		db_data = data.DataBase.GetAll()
		# 2.2. prepare DB-data dict
		for i in xrange(len(db_data)):
			db_dict[db_data[i][0]] = i
		CmpLists(d, db_data, db_dict, TrySaveData)

def	Run(filelist):
	data.Parser = parser.MyHTMLParser()
	data.DataBase = db.DB()
	data.DataBase.Open("localhost", "jobru", "eugene")
	if (len(filelist)):
		ImportFromHTML(filelist)
	PrintDebug(1, "I: Start GUI")
	gui.Exec()
	data.DataBase.Close()

if __name__ == "__main__":
	if ((len(sys.argv) == 2) and (sys.argv[1] == "--help")):
		print "Usage:", sys.argv[0], "<html file 1> <html file 2> ..."
	else:
		Run(sys.argv[1:])
