#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tool to run 1C on Linux for some users and some bases.
This tool help to control visibility, accounts and passwords of 1C-users.
'''

import sys, os, pprint, qt, qttable
from xml.parsers import expat

Global = []	# [user, binpath, datapth, user1s, pass1c, [(rpath, title),]]
Base = {}	# {id:[rpath, title],}
Selected = None	# row, mode

# -----	XML part -----
def start_element(name, attrs):
	'''
	Start tag catcher
	@param name:string tag name
	@param attrs:dict of tag attributes
	'''
	global Global, Base

	if (name == 'g'):
		Global.extend([attrs.get('bp'), attrs.get('dp')])
	elif (name == 'u'):
		if (attrs['id'] == Global[0]):
			Global.extend([attrs.get('l'), attrs.get('p'), []])
	elif (name == 'b'):
		Base[attrs['id']] = (attrs.get('p'), attrs.get('t'))
	elif (name == 'ub'):
		if (attrs['uid'] == Global[0]):
			b = Base[attrs['bid']]
			if (b):
				Global[5].append(b)

def	LoadXML(fname):
	'''
	Load data from xml-file.
	@param fname:string - xml filename
	'''
	p = expat.ParserCreate()
	p.StartElementHandler = start_element
	p.ParseFile(open(fname))

# -----	GUI part -----
class MainForm(qt.QDialog):
	def __init__(self):
		qt.QDialog.__init__(self)
		self.Selected = -1
		self.setName("Form")

		FormLayout = qt.QGridLayout(self, 3, 2)
		# radio
		self.ModeBox = qt.QButtonGroup(1, qt.Qt.Horizontal, self.__tr("Mode"), self)
		#self.ModeBox.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.ModeBox.sizePolicy().hasHeightForWidth()))
		qt.QRadioButton(self.__tr("Enterprise"), self.ModeBox)
		qt.QRadioButton(self.__tr("Enterprise (singleuser)"), self.ModeBox)
		qt.QRadioButton(self.__tr("Designer"), self.ModeBox)
		qt.QRadioButton(self.__tr("Monitor"), self.ModeBox)
		FormLayout.addMultiCellWidget(self.ModeBox, 0, 0, 0, 1)
		# listview
		self.Table = qttable.QTable(0, 1, self)
		self.Table.horizontalHeader().setLabel(0, self.__tr("Name"))
		self.Table.setReadOnly(True)
		self.Table.setSelectionMode(qttable.QTable.SingleRow)
		FormLayout.addMultiCellWidget(self.Table, 1, 1, 0, 1)
		# buttons
		self.ButtonOK = qt.QPushButton(self.__tr("OK"), self)
		FormLayout.addWidget(self.ButtonOK, 2, 0)
		self.ButtonCancel = qt.QPushButton(self.__tr("Cancel"), self)
		FormLayout.addWidget(self.ButtonCancel, 2, 1)
		self.clearWState(qt.Qt.WState_Polished)

		# actions - OK, Cancel, listview.DoubleClick()
		qt.QObject.connect(self.ButtonOK, qt.SIGNAL("clicked()"), self.OnOk)
		qt.QObject.connect(self.ButtonCancel, qt.SIGNAL("clicked()"), self, qt.SLOT("reject()"));
		qt.QObject.connect(self.Table, qt.SIGNAL("doubleClicked(int, int, int, const QPoint &)"), self.OnDC)

	def __tr(self,s,c = None):
		return qt.qApp.translate("MainForm",s,c)

	def	AddRows(self, rows):
		self.Table.setNumRows(len(rows))
		for r, row in enumerate(rows):
			self.Table.setText(r, 0, row[1])

	def	SetFocuses(self):
		self.ModeBox.setButton(0)
		#self.Table.setCurrentCell(0, 0)
		self.Table.selectRow(0)
##		self.Selected = 0

	def	OnDC(self, r, c, b, p):
		self.OnOk()

	def	OnOk(self):
		global Selected
		Selected = (self.Table.currentRow(), self.ModeBox.selectedId())
		self.accept()

# -----	Main part -----
def	DebugOut():
	pass

def     main(argv):
	global Global, Selected
	Global.append(os.environ['LOGNAME'])
	# 1. prepare GUI
	app = qt.QApplication(argv)
	w = MainForm()
	app.setMainWidget(w)
	# 2. load data
	LoadXML('run1c.xml')
	# 3. fillout dialog
	w.AddRows(Global[5])
	# 4. postprepare
	w.SetFocuses()
	qt.QObject.connect(app, qt.SIGNAL("lastWindowClosed()"), app, qt.SLOT("quit()"))
	# 5. show
	app.mainWidget().show()
	app.exec_loop()
	if (Selected):
		mode = ("enterprise", "enterprise\" \"/M", "config", "monitor")
		execstring = "wine \"%s\" \"%s\" \"/D%s\"" % (\
			Global[1],\
			mode[Selected[1]],\
			Global[2] + "\\" + Global[5][Selected[0]][0])
		if (Global[3]):
			execstring += " \"/N%s\"" % Global[3]
		if (Global[4]):
			execstring += " \"/P%s\"" % Global[4]
		print execstring.replace('\\', '\\\\')

if (__name__ == '__main__'):
        main(sys.argv)
