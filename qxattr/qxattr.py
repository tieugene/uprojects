#!/bin/env python
# -*- coding: utf-8 -*-
# Handling xattrs

import	sys, xattr
from PyQt4 import QtCore, QtGui

class	MainDialog(QtGui.QDialog):
	def __init__(self, file):
		self.file = file
		QtGui.QDialog.__init__(self)
		self.resize(QtCore.QSize(QtCore.QRect(0,0,315,300).size()).expandedTo(self.minimumSizeHint()))
		self.vbl = QtGui.QVBoxLayout(self)
		self.tw = QtGui.QTableWidget(self)
		self.tw.setColumnCount(2)
		headerItem = QtGui.QTableWidgetItem()
		headerItem.setText(QtGui.QApplication.translate("qxattr", "attr", None, QtGui.QApplication.UnicodeUTF8))
		self.tw.setHorizontalHeaderItem(0,headerItem)
		headerItem1 = QtGui.QTableWidgetItem()
		headerItem1.setText(QtGui.QApplication.translate("qxattr", "value", None, QtGui.QApplication.UnicodeUTF8))
		self.tw.setHorizontalHeaderItem(1,headerItem1)
		self.vbl.addWidget(self.tw)
		self.hbl = QtGui.QHBoxLayout(self)
		self.addButton = QtGui.QPushButton("+", self)
		self.hbl.addWidget(self.addButton)
		self.delButton = QtGui.QPushButton("-", self)
		self.hbl.addWidget(self.delButton)
		self.hbl.addItem(QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum))
		self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Close, QtCore.Qt.Horizontal, self)
		self.hbl.addWidget(self.buttonBox)
		self.vbl.addLayout(self.hbl)
		QtCore.QObject.connect(self.buttonBox.button(QtGui.QDialogButtonBox.Apply), QtCore.SIGNAL("clicked()"), self.__apply)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"),self.accept)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"),self.reject)
		QtCore.QObject.connect(self.addButton, QtCore.SIGNAL("clicked()"),self.__add)
		QtCore.QObject.connect(self.delButton, QtCore.SIGNAL("clicked()"),self.__del)
		self.__load()

	def	__load(self):
		alist = xattr.listxattr(self.file)
		if (len(alist)):
			self.tw.setRowCount(len(alist))
			for r, a in enumerate(alist):
				self.tw.setItem(r, 0, QtGui.QTableWidgetItem(a[5:]))
				self.tw.setItem(r, 1, QtGui.QTableWidgetItem(xattr.getxattr(self.file, a)))

	def	__add(self):
		self.tw.setRowCount(self.tw.rowCount() + 1)

	def	__del(self):
		r = self.tw.currentRow()
		if (r >= 0):
			self.tw.removeRow(r)
	
	def	__apply(self):
		for r in xrange(self.tw.rowCount()):
			a = str(self.tw.item(r, 0).text())
			v = str(self.tw.item(r, 1).text())
			print a, v
			xattr.setxattr(self.file, "user."+a, v)

if (__name__ == '__main__'):
	if (len(sys.argv) != 2):
		print "Usage: %s <filename>" % sys.argv[0]
		sys.exit(0)
	aMain = QtGui.QApplication( sys.argv )
	#translator	= QtCore.QTranslator()
	#translator.load("tr/ob_" + QtCore.QLocale().system().name().left(2))
	#aMain.installTranslator(translator)
	mwMain	= MainDialog(sys.argv[1])
	mwMain.show()
	sys.exit(aMain.exec_())
