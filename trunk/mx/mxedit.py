#!/bin/env python
# -*- coding: utf-8 -*-
# Handling xattrs

import	sys, xattr, ConfigParser, pprint
from		PyQt4	import QtCore, QtGui
from		treeselect	import Node, TreeModel, TreeSelectDialog
from		mxattr	import MxList

class	MainDialog(QtGui.QDialog):
	'''
	Main window.
	'''
	def __init__(self, file):
		self.file = file
		self.wdict = {}	# widgets own
		self.fdict = {}	# flags
		self.tdict = {}	# tree buttons
		self.mxlist	= MxList()
		cp = ConfigParser.ConfigParser()
		cp.readfp(open('index.conf'))
		self.mxlist.loadCfg(cp)

		QtGui.QDialog.__init__(self)
		self.resize(QtCore.QSize(QtCore.QRect(0,0,315,300).size()).expandedTo(self.minimumSizeHint()))
		self.gl = QtGui.QGridLayout(self)
		maxrow = self.__setwidgets(self.gl)
		self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Apply | QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Close, QtCore.Qt.Horizontal, self)
		self.gl.addWidget(self.buttonBox, maxrow, 0, 1, 3)
		QtCore.QObject.connect(self.buttonBox.button(QtGui.QDialogButtonBox.Apply), QtCore.SIGNAL("clicked()"), self.__apply)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"),self.accept)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"),self.reject)
		self.selectDialog = TreeSelectDialog()
		self.__load()

	def	__setwidgets(self, gl):
		for row, fldname in enumerate(self.mxlist.data.keys()):
			fld = self.mxlist.data[fldname]
			widget = None
			label = fld.Label if fld.Label else fld.Name
			gl.addWidget(QtGui.QLabel(label, self), row, 0)
			if (fld.Type == "b"):
				widget = QtGui.QCheckBox()
			elif (fld.Type == "se"):
				widget = QtGui.QComboBox()
				for i in fld.Values:
					widget.addItem(QtCore.QString().fromUtf8(i))
			elif (fld.Type == "st"):
				widget = QtGui.QLineEdit()
				widget.setReadOnly(True)
				btn = QtGui.QPushButton("V", self)		# QtGui.QCommandLinkButton("expand")
				btn.setObjectName(fld.Name)
				self.tdict[fld.Name] = btn
				gl.addWidget(btn, row, 3)
				QtCore.QObject.connect(btn, QtCore.SIGNAL("clicked()"), self.__calltree)
			elif (fld.Type == "sl"):
				widget = QtGui.QLineEdit()
			elif (fld.Type == "sh"):
				widget = QtGui.QTexEdit()
			elif (fld.Type == "sp"):
				widget = QtGui.QPlainTexEdit()
			elif (fld.Type == "i"):
				widget = QtGui.QSpinBox()
			elif (fld.Type == "f"):
				widget = QtGui.QDoubleSpinBox()
			elif (fld.Type == "d"):
				widget = QtGui.QDateEdit()
			elif (fld.Type == "t"):
				widget = QtGui.QTimeEdit()
			elif (fld.Type == "dt"):
				widget = QtGui.QDateTimeEdit()
			elif (fld.Type == "g"):
				widget = QtGui.QGraphicsView()
			elif (fld.Type == "x"):
				widget = QtGui.QLineEdit()
			else:
				print "Unknown type"
			if widget:
				widget.setObjectName(fld.Name)
				self.wdict[fld.Name] = widget
				gl.addWidget(widget, row, 1)
				if (not fld.Mandatory):
					cb = QtGui.QCheckBox("")
					cb.setObjectName(fld.Name)
					QtCore.QObject.connect(cb, QtCore.SIGNAL("clicked()"), self.__chgflag)
					self.fdict[fld.Name] = cb
					gl.addWidget(cb, row, 2)
		return row + 1

	def	__calltree(self):
		wn = str(self.sender().objectName())
		s = self.selectDialog._letsGo(self.mxlist.data[wn].Values)
		if (s):
			self.wdict[wn].setText(s)

	def	__chgflag(self):
		cb = self.sender()
		wn = str(cb.objectName())
		widget = self.wdict[wn]
		widget.setEnabled(cb.isChecked())
		if (self.mxlist.data[wn].Type == 'st'):
			self.tdict[wn].setEnabled(cb.isChecked())

	def	__load(self):
		'''
		Load all xattrs into mem.
		'''
		self.mxlist.loadData(self.file)
		for fldname in self.mxlist.data.keys():
			data = None
			fld = self.mxlist.data[fldname]
			if (fld.loaded):
				data = fld.data
				if (not fld.Mandatory):
					self.fdict[fld.Name].setCheckState(QtCore.Qt.Checked)
			else:
				if (fld.Mandatory):
					data = fld.Default
				else:
					self.wdict[fld.Name].setEnabled(False)
			widget = self.wdict[fld.Name]
			if (data):
				if (fld.Type == 'b'):
					widget.setCheckState(QtGui.Qt.Checked)
				elif (fld.Type == 'se'):
					i = widget.findText(QtCore.QString().fromUtf8(data))
					if (i >= 0):
						widget.setCurrentIndex(i)
				elif (fld.Type in ('st', 'sl', 'x')):
					widget.setText(QtCore.QString().fromUtf8(data))
				elif (fld.Type == 'sh'):
					widget.setHtml(QtCore.QString().fromUtf8(data))
				elif (fld.Type == 'sp'):
					widget.setText(QtCore.QString().fromUtf8(data))
				elif (fld.Type in ('i', 'f')):
					widget.setValue(data)
				elif (fld.Type == 'd'):
					widget.setDate(QtCore.QDate(data))
				elif (fld.Type == 't'):
					widget.setTime(QtCore.QTime(data))
				elif (fld.Type == 'dt'):
					widget.setDateTime(QtCore.QDateTime(data))

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
	translator.load("mx_" + QtCore.QLocale().system().name().left(2))
	aMain.installTranslator(translator)
	mwMain	= MainDialog(sys.argv[1])
	mwMain.show()
	sys.exit(aMain.exec_())
