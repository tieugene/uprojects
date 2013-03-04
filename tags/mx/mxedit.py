#!/bin/env python
# -*- coding: utf-8 -*-
# Handling xattrs

import	sys, ConfigParser
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
		self.buttonBox = QtGui.QDialogButtonBox( QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
		self.gl.addWidget(self.buttonBox, maxrow, 0, 1, 4)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
		self.selectDialog = TreeSelectDialog()
		self.__load()

	def	__setwidgets(self, gl):
		for row, fldname in enumerate(self.mxlist.data.keys()):
			fld = self.mxlist.data[fldname]
			widget = None
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
				label = fld.Label if fld.Label else fld.Name
				gl.addWidget(QtGui.QLabel(label, self), row, 0)
				widget.setObjectName(fld.Name)
				if (fld.ToolTip):
					widget.setToolTip(QtCore.QString().fromUtf8(fld.ToolTip))
				if (fld.StatusTip):
					widget.setStatusTip(QtCore.QString().fromUtf8(fld.StatusTip))
				if (fld.WhatsTip):
					widget.setWhatsThis(QtCore.QString().fromUtf8(fld.WhatsTip))
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
		Load all xattrs into widgets.
		'''
		self.mxlist.loadData(self.file)
		for fldname in self.mxlist.data.keys():
			data = None
			fld = self.mxlist.data[fldname]
			widget = self.wdict[fld.Name]
			if (fld.loaded):
				data = fld.data
				if (not fld.Mandatory):
					self.fdict[fld.Name].setCheckState(QtCore.Qt.Checked)
			else:
				if (fld.Mandatory):
					data = fld.Default
				else:
					self.wdict[fld.Name].setEnabled(False)
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

	def	accept(self):
		for fldname in self.mxlist.data.keys():
			fld = self.mxlist.data[fldname]
			widget = self.wdict[fld.Name]
			if (not fld.Mandatory) and (not self.fdict[fldname].isChecked()):
				fld.data = None
			else:
				if (fld.Type == 'b'):
					fld.data = widget.isChecked()
				elif (fld.Type == 'se'):
					fld.data = widget.currentText().toUtf8()
				elif (fld.Type in ('st', 'sl', 'x')):
					fld.data = widget.text().toUtf8()
				elif (fld.Type == 'sh'):
					fld.data = widget.toHtml().toUtf8()
				elif (fld.Type == 'sp'):
					fld.data = widget.toPlainText().toUtf8()
				elif (fld.Type in ('i', 'f')):
					fld.data = widget.value(data)
				elif (fld.Type == 'd'):
					fld.data = widget.date().toPyDate()
				elif (fld.Type == 't'):
					fld.data = widget.date().toPyTime()
				elif (fld.Type == 'dt'):
					fld.data = widget.date().toPyDateTime()
		self.mxlist.saveData(self.file)
		QtGui.QDialog.accept(self)

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
