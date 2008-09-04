#!/bin/env python
# -*- coding: utf-8 -*-
# Handling xattrs

import	sys, xattr, ConfigParser, pprint
from		treeselect import Node, TreeModel, TreeSelectDialog

class	MainDialog(QtGui.QDialog):
	'''
	Main window.
	'''
	def __init__(self, file):
		self.file = file
		self.wdict = {}
		self.trees = {}
		QtGui.QDialog.__init__(self)
		self.resize(QtCore.QSize(QtCore.QRect(0,0,315,300).size()).expandedTo(self.minimumSizeHint()))
		self.gl = QtGui.QGridLayout(self)

		cp = self.__loadcfg("index.conf")
		maxrow = self.__setwidgets(cp, self.gl)

		self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Close, QtCore.Qt.Horizontal, self)
		self.gl.addWidget(self.buttonBox, maxrow, 0, 1, 3)
		QtCore.QObject.connect(self.buttonBox.button(QtGui.QDialogButtonBox.Apply), QtCore.SIGNAL("clicked()"), self.__apply)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"),self.accept)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"),self.reject)
		self.selectDialog = TreeSelectDialog()
		self.__load()

	def	__loadcfg(self, f):
		'''
		Load config file.
		@param f:str - file.
		'''
		cp = ConfigParser.ConfigParser()
		cp.readfp(open('index.conf'))
		return cp

	def	__test(self):
		wn = str(self.sender().objectName())
		s = self.selectDialog._letsGo(self.trees[wn])
		if (s):
			self.wdict[wn].setText(s)

	def	__setwidgets(self, cp, gl):
		for row, sect in enumerate(cp.sections()):
			widget = None
			st, sn = sect.split(".")
			label = cp.get(sect, "Label") if cp.has_option(sect, "Label") else sn
			gl.addWidget(QtGui.QLabel(label, self), row, 0)
			if (st == "b"):
				widget = QtGui.QCheckBox()
			elif (st == "se"):
				values = eval(cp.get(sect, "Values"))			#values = map(lambda x: x.strip(' "\n'), cp.get(sect, "Values").split(";"))
				widget = QtGui.QComboBox()
				for i in values:							#widget.addItems(QtCore.QStringList(list(values)))
					widget.addItem(QtCore.QString().fromUtf8(i))
			elif (st == "st"):
				widget = QtGui.QLineEdit()
				btn = QtGui.QPushButton("V", self)				#QtGui.QCommandLinkButton("expand")
				btn.setObjectName(sn)
				gl.addWidget(btn, row, 2)
				QtCore.QObject.connect(btn, QtCore.SIGNAL("clicked()"), self.__test)
				values = eval(cp.get(sect, "Values"))
				self.trees [sn] = values
			elif (st == "sl"):
				widget = QtGui.QLineEdit()
			elif (st == "sh"):
				widget = QtGui.QTexEdit()
			elif (st == "sp"):
				widget = QtGui.QPlainTexEdit()
			elif (st.startswith("i")):
				widget = QtGui.QSpinBox()
			elif (st.startswith("u")):
				widget = QtGui.QSpinBox()
			elif (st == "f"):
				widget = QtGui.QDoubleSpinBox()
			elif (st == "d"):
				widget = QtGui.QDateEdit()
			elif (st == "t"):
				widget = QtGui.QTimeEdit()
			elif (st == "dt"):
				widget = QtGui.QDateTimeEdit()
			elif (st == "g"):
				widget = QtGui.QGraphicsView()
			elif (st == "x"):
				widget = QtGui.QLineEdit()
			elif (st == "r"):
				pass
			else:
				print "Unknown type: %s" % st
			if widget:
				widget.setObjectName(sect)
				self.wdict[sn] = widget
				gl.addWidget(widget, row, 1)
		return row + 1

	def	__load(self):
		'''
		Load all xattrs into mem.
		'''
		self.xattr0 = self.__file2hash(self.file)		# 1. load data
		self.__hash2fields(self.xattr0)		# 3. paint

	def	__apply(self):
		'''
		Save attrs and continue edititng.
		'''
		h = self.__table2hash(self.tw)			# 1. get new values
		h1 = self.__file2hash(self.file)		# 2. check that xattrs not changed.
		#print h, h1
		if (self.xattr0 != h1):				# FIXME: Force | Reload
			QtGui.QMessageBox.warning(self,\
				QtGui.QApplication.translate("mxattr", "Xattrs changed", None, QtGui.QApplication.UnicodeUTF8),\
				QtGui.QApplication.translate("mxattr", "File attributes changed due editing new. They will be rewrited.", None, QtGui.QApplication.UnicodeUTF8),\
			)
		self.__hash2file(h, h1, self.file)
		self.xattr0 = h1

	def	__file2hash(self, f):
		'''
		Load file's xattrs into hash
		@param f:file
		@return QHash
		'''
		h = {}
		alist = xattr.listxattr(self.file)
		for r, a in enumerate(alist):
			h[a[5:]] = xattr.getxattr(f, a)
		return h

	def	__hash2fields(self, h):
		'''
		Put hash into table
		@param h:QHash - source
		@param t:QTableWidget - dest
		@return None
		'''
		for a in enumerate(h.keys()):
			st, sn = a.split(".")
##			if self.wdict[]
			if (st == "b"):
				widget = QtGui.QCheckBox()
			elif (st == "se"):
				values = eval(cp.get(sect, "Values"))			#values = map(lambda x: x.strip(' "\n'), cp.get(sect, "Values").split(";"))
				widget = QtGui.QComboBox()
				for i in values:							#widget.addItems(QtCore.QStringList(list(values)))
					widget.addItem(QtCore.QString().fromUtf8(i))
			elif (st == "st"):
				widget = QtGui.QLineEdit()
				btn = QtGui.QPushButton("V", self)				#QtGui.QCommandLinkButton("expand")
				btn.setObjectName(sn)
				gl.addWidget(btn, row, 2)
				QtCore.QObject.connect(btn, QtCore.SIGNAL("clicked()"), self.__test)
				values = eval(cp.get(sect, "Values"))
				self.trees [sn] = values
			elif (st == "sl"):
				widget = QtGui.QLineEdit()
			elif (st == "sh"):
				widget = QtGui.QTexEdit()
			elif (st == "sp"):
				widget = QtGui.QPlainTexEdit()
			elif (st.startswith("i")):
				widget = QtGui.QSpinBox()
			elif (st.startswith("u")):
				widget = QtGui.QSpinBox()
			elif (st == "f"):
				widget = QtGui.QDoubleSpinBox()
			elif (st == "d"):
				widget = QtGui.QDateEdit()
			elif (st == "t"):
				widget = QtGui.QTimeEdit()
			elif (st == "dt"):
				widget = QtGui.QDateTimeEdit()
			elif (st == "g"):
				widget = QtGui.QGraphicsView()
			elif (st == "x"):
				widget = QtGui.QLineEdit()
			elif (st == "r"):
				pass
			else:
				print "Unknown type: %s" % st

	def	__table2hash(self, t):
		'''
		Get data from GUI into inner dict.
		@param f:QTableWidget
		@return dict
		'''
		h = {}
		for r in xrange(t.rowCount()):
			if ((t.item(r, 0) == None) or (t.item(r, 0).text().isEmpty())):		# 1. check empty key
				QtGui.QMessageBox.critical(self,\
					QtGui.QApplication.translate("mxattr", "Empty key", None, QtGui.QApplication.UnicodeUTF8),\
					QtGui.QApplication.translate("mxattr", "Attribute name is empty", None, QtGui.QApplication.UnicodeUTF8),\
				)
				return None
			a = str(t.item(r, 0).text().toUtf8())
			if h.has_key(a):										# 2. check double keys
				QtGui.QMessageBox.critical(self,\
					QtGui.QApplication.translate("mxattr", "Double key", None, QtGui.QApplication.UnicodeUTF8),\
					QtGui.QApplication.translate("mxattr", "Attribute name already exists", None, QtGui.QApplication.UnicodeUTF8),\
				)
				return None
			if ((t.item(r, 1) == None) or (t.item(r, 1).text().isEmpty())):		# 3. check empty value
				QtGui.QMessageBox.critical(self,\
					QtGui.QApplication.translate("mxattr", "Empty value", None, QtGui.QApplication.UnicodeUTF8),\
					QtGui.QApplication.translate("mxattr", "Attribute value is empty", None, QtGui.QApplication.UnicodeUTF8),\
				)
				return None
			h[a] = str(t.item(r, 1).text().toUtf8())
		return h

	def	__hash2file(self, h, h1, f):
		'''
		Save dict into file's xattrs.
		@param h:dict new values
		@param h1:dict old values
		@param f:file
		@return None
		'''
		# 1. delete deleted
		for k in h1.keys():
			if k not in h:
				xattr.removexattr(f, "user."+k)
		for r, k in enumerate(h.keys()):
			#print type(a).__name__, a, type(h[a]).__name__, h[a]
			if ((k not in h1) or (h[k] != h1[k])):
				xattr.setxattr(f, "user."+k, h[k])
				print k, "=", h[k]

if (__name__ == '__main__'):
	if (len(sys.argv) != 2):
		print "Usage: %s <filename>" % sys.argv[0]
		sys.exit(0)
	aMain = QtGui.QApplication( sys.argv )
	translator	= QtCore.QTranslator()
	translator.load("tr_" + QtCore.QLocale().system().name().left(2))
	aMain.installTranslator(translator)
	mwMain	= MainDialog(sys.argv[1])
	mwMain.show()
	sys.exit(aMain.exec_())
