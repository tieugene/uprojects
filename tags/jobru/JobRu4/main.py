#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Software to analyse www.job.ru information.
Main module.
'''

import sys
from PyQt4 import QtSql, QtGui
##import data, db, gui, utility, parser
import view, model, parser, data, utility

def	createConnection(app):
	mysqlflag = False
	if (mysqlflag):
		db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
		db.setDatabaseName("jobru")
		db.setHostName("localhost")
		db.setUserName("eugene")
	else:
		db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
		db.setDatabaseName("jobru.db")
	if not db.open():
		print db.lastError().text()
		QtGui.QMessageBox.critical(0, app.tr("Cannot open database"),
			app.tr("Unable to establish a database connection."),
			QtGui.QMessageBox.Cancel, QtGui.QMessageBox.NoButton)
		return None
	else:
		if (db.tables().indexOf("main") == -1):
			query = QtSql.QSqlQuery()
			query.exec_(data.Create_SQL_String)
	return db

def	Run(filelist):
	'''
	@param filelist:str[] - list of files to convert
	'''
	app = view.Init()
	data.Parser = parser.MyHTMLParser()
	data.DataBase = createConnection(app)
	if (data.DataBase):
		if (len(filelist)):
			ImportFromHTML(filelist)
		view.Exec(app, model.CreateModel())
		data.DataBase.close()

if __name__ == "__main__":
	if ((len(sys.argv) == 2) and (sys.argv[1] == "--help")):
		print "Usage:", sys.argv[0], "[<html file 1>[ <html file 2> ...]]"
	else:
		Run(sys.argv[1:])
