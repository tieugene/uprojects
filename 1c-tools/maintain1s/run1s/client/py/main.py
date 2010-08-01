# -*- coding: utf-8 -*-
'''
Processed data: base, blog, calendar, docs, photos, spreadsheet
Not processed: addressbook, mail, writer
'''

import		sys, gdata
from	PyQt4	import QtCore, QtGui,  QtNetwork
import		settings
import Ui_Main

mwMain = None

class	MainWindow(QtGui.QMainWindow, Ui_Main.Ui_MainWindow):
	def	__init__(self):
		QtGui.QMainWindow.__init__(self)
		self.setupUi(self)
		self.__setSlots()

	def	__setSlots(self):
		self.actionSettings.connect( self.actionSettings, QtCore.SIGNAL( "triggered()" ), settings.dSettings.slDialog )

	def	__slOpenBlog(self):
		self.blog = blog.BlogDialog(str(settings.Setting.LoginBlog), str(settings.Setting.PasswordBlog))
		self.blog.exec_()

	def	Update(self):
		'''
		Update list from server.
		'''
		self.http = QtNetwork.QHttp("master",  80)
		#self.http.connect(self.http, QtCore.SIGNAL( "requestStarted(int)" ), self.slListStart)
		#self.http.connect(self.http, QtCore.SIGNAL( "requestFinished(int, bool)" ), self.slListEnd)
		self.http.connect(self.http, QtCore.SIGNAL( "readyRead(QHttpResponseHeader)" ), self.slReadyRead)
		self.rqid = self.http.get("/baselist")

	def	slListStart(self, id ):
		if id == self.rqid:
			print "Start: Request id OK."
		else:
			print "Start: Request id is BAD."

	def	slListEnd(self, id,  err ):
		if id == self.rqid:
			print "End: Request id ended:",  err
		else:
			print "End: Request id is BAD."

	def	slReadyRead(self,  rq):
		tokenRun1s = QtCore.QString("run1s")
		tokenHost = QtCore.QString("host")
		tokenShare = QtCore.QString("share")
		tokenBase = QtCore.QString("base")
		self.bases = []
		a = self.http.readAll()
		xml = QtCore.QXmlStreamReader(a)
		while (not xml.atEnd()):
			xml.readNext()
			if (xml.isStartElement ()):
				t = xml.name().toString()
				if (t == tokenRun1s):
					self.ver = xml.attributes().value("",  "ver").toString()
				elif (t == tokenHost):
					self.host = xml.attributes().value("",  "name").toString()
				elif (t == tokenShare):
					self.share = xml.attributes().value("",  "name").toString()
				elif (t == tokenBase):
					a = xml.attributes()
					self.base = {"path" : a.value("",  "path").toString(),  "type": a.value("",  "type").toString(),  "org": a.value("",  "org").toString(),  "comments": a.value("",  "comments").toString()}
					r = self.tableWidget.rowCount()
					self.tableWidget.setRowCount(r + 1)
					self.tableWidget.setItem(r,  0,  QtGui.QTableWidgetItem(self.base["type"]))
					self.tableWidget.setItem(r,  1,  QtGui.QTableWidgetItem(self.base["org"]))
					self.tableWidget.setItem(r,  2,  QtGui.QTableWidgetItem(self.base["comments"]))
					self.bases.append(self.host + "\\\\" + self.share + "\\" + self.base["path"])
				else:
					print "bad token:"

def	Main():
	'''
	Main module
	'''
	global mwMain

	# 0. Main
	aMain		= QtGui.QApplication( sys.argv )

	# 1. Translation
	translator	= QtCore.QTranslator()
	translator.load("./run1s_" + QtCore.QLocale().system().name().left(2))	# FIXME:
	aMain.installTranslator(translator)

	settings.dSettings	= settings.SettingsDialog()
	settings.dSettings.slLoad()
	mwMain			= MainWindow()

	# 6. Lets go
	mwMain.show()
	mwMain.Update()
	aMain.exec_()
