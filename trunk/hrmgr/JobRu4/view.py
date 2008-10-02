# -*- coding: utf-8 -*-
'''
view.py - main form.
'''

from PyQt4 import QtCore, QtGui
import htmimpex, xmlimpex, model

class MainWindow(object):
	def setupUi(self, mw, model):
		mw.setObjectName("MainWindow")
		self.centralwidget = QtGui.QWidget(mw)
		# widgets
		# ...labels
		self.Label_City = QtGui.QLabel(self.centralwidget)
		self.Label_Title = QtGui.QLabel(self.centralwidget)
		self.Label_Employer = QtGui.QLabel(self.centralwidget)
		self.Label_Contact = QtGui.QLabel(self.centralwidget)
		self.Label_Phone = QtGui.QLabel(self.centralwidget)
		self.Label_Email = QtGui.QLabel(self.centralwidget)
		self.Label_Requirements = QtGui.QLabel(self.centralwidget)
		self.Label_Duty = QtGui.QLabel(self.centralwidget)
		self.Label_Conditions = QtGui.QLabel(self.centralwidget)
		# ...editable
		self.TableView_Main = QtGui.QTableView(self.centralwidget)
		self.LineEdit_City = QtGui.QLineEdit(self.centralwidget)
		self.LineEdit_Title = QtGui.QLineEdit(self.centralwidget)
		self.LineEdit_Employer = QtGui.QLineEdit(self.centralwidget)
		self.LineEdit_Contact = QtGui.QLineEdit(self.centralwidget)
		self.LineEdit_Phone = QtGui.QLineEdit(self.centralwidget)
		self.LineEdit_Email = QtGui.QLineEdit(self.centralwidget)
		self.TextEdit_Requirement = QtGui.QTextEdit(self.centralwidget)
		self.TextEdit_Duty = QtGui.QTextEdit(self.centralwidget)
		self.TextEdit_Conditions = QtGui.QTextEdit(self.centralwidget)
		# ...layouts
		self.Layout_Gr0 = QtGui.QGridLayout(self.centralwidget)
		self.Layout_Gr1 = QtGui.QGridLayout()
		self.Layout_VB1 = QtGui.QVBoxLayout()
		self.Layout_VB2 = QtGui.QVBoxLayout()
		self.Layout_VB3 = QtGui.QVBoxLayout()
		# geometrics all
		self.Layout_Gr1.addWidget(self.Label_City,		0,0,1,1)
		self.Layout_Gr1.addWidget(self.Label_Title,		1,0,1,1)
		self.Layout_Gr1.addWidget(self.Label_Employer,		2,0,1,1)
		self.Layout_Gr1.addWidget(self.Label_Contact,		3,0,1,1)
		self.Layout_Gr1.addWidget(self.Label_Phone,		4,0,1,1)
		self.Layout_Gr1.addWidget(self.Label_Email,		5,0,1,1)

		self.Layout_Gr1.addWidget(self.LineEdit_City,		0,1,1,1)
		self.Layout_Gr1.addWidget(self.LineEdit_Title,		1,1,1,1)
		self.Layout_Gr1.addWidget(self.LineEdit_Employer,	2,1,1,1)
		self.Layout_Gr1.addWidget(self.LineEdit_Contact,	3,1,1,1)
		self.Layout_Gr1.addWidget(self.LineEdit_Phone,		4,1,1,1)
		self.Layout_Gr1.addWidget(self.LineEdit_Email,		5,1,1,1)

		self.Layout_VB1.addWidget(self.Label_Duty)
		self.Layout_VB1.addWidget(self.TextEdit_Duty)

		self.Layout_VB2.addWidget(self.Label_Requirements)
		self.Layout_VB2.addWidget(self.TextEdit_Requirement)

		self.Layout_VB3.addWidget(self.Label_Conditions)
		self.Layout_VB3.addWidget(self.TextEdit_Conditions)

		self.Layout_Gr0.addWidget(self.TableView_Main,		0,0,1,2)
		self.Layout_Gr0.addLayout(self.Layout_Gr1,		1,0,1,1)
		self.Layout_Gr0.addLayout(self.Layout_VB1,		2,0,1,1)
		self.Layout_Gr0.addLayout(self.Layout_VB2,		1,1,1,1)
		self.Layout_Gr0.addLayout(self.Layout_VB3,		2,1,1,1)

		mw.setCentralWidget(self.centralwidget)

		# actions
		self.Action_Import_HTML = QtGui.QAction(mw)
		self.Action_Export_HTML = QtGui.QAction(mw)
		self.Action_Import_XML = QtGui.QAction(mw)
		self.Action_Export_XML = QtGui.QAction(mw)
		self.Action_Backup_DB = QtGui.QAction(mw)
		self.Action_Restore_DB = QtGui.QAction(mw)
		self.Action_Delete_All = QtGui.QAction(mw)
		self.Action_Exit = QtGui.QAction(mw)
		self.Action_Filter = QtGui.QAction(mw)
		self.Action_Sort = QtGui.QAction(mw)
		# TODO: disable actions
		self.Action_Export_HTML.setEnabled(False)
		self.Action_Export_XML.setEnabled(False)
		self.Action_Backup_DB.setEnabled(False)
		self.Action_Restore_DB.setEnabled(False)
		self.Action_Filter.setEnabled(False)
		self.Action_Sort.setEnabled(False)
		# menu
		# ... main
		self.MenuBar = QtGui.QMenuBar(mw)
		self.MenuFile = QtGui.QMenu(self.MenuBar)
		self.MenuEdit = QtGui.QMenu(self.MenuBar)
		self.MenuData = QtGui.QMenu(self.MenuBar)
		mw.setMenuBar(self.MenuBar)
		# ...sub
		self.MenuFile.addAction(self.Action_Import_HTML)
		self.MenuFile.addAction(self.Action_Export_HTML)
		self.MenuFile.addSeparator()
		self.MenuFile.addAction(self.Action_Import_XML)
		self.MenuFile.addAction(self.Action_Export_XML)
		self.MenuFile.addSeparator()
		self.MenuFile.addAction(self.Action_Backup_DB)
		self.MenuFile.addAction(self.Action_Restore_DB)
		self.MenuFile.addSeparator()
		self.MenuFile.addAction(self.Action_Exit)
		self.MenuEdit.addAction(self.Action_Delete_All)
		self.MenuData.addAction(self.Action_Filter)
		self.MenuData.addAction(self.Action_Sort)
		self.MenuBar.addAction(self.MenuFile.menuAction())
		self.MenuBar.addAction(self.MenuEdit.menuAction())
		self.MenuBar.addAction(self.MenuData.menuAction())
		# status bar
		self.StatusBar = QtGui.QStatusBar(mw)
		mw.setStatusBar(self.StatusBar)
		# others
		self.__retranslateUi(mw)
		self.__SetModels(model)
		self.__TuneTable()
		self.__ConnectSignals()

	def tr(self, string):
		'''
		Translates given string due to app's dict.
		@param string:string translated string
		@return*string translated to ru
		'''
		return QtGui.QApplication.translate("Main Window", string, None, QtGui.QApplication.UnicodeUTF8)

	def __retranslateUi(self, mw):
		mw.setWindowTitle(self.tr("MainWindow"))
		self.Label_City.setText(self.tr("City"))
		self.Label_Title.setText(self.tr("Title"))
		self.Label_Employer.setText(self.tr("Employer"))
		self.Label_Contact.setText(self.tr("Contact"))
		self.Label_Phone.setText(self.tr("Phone"))
		self.Label_Email.setText(self.tr("E-Mail"))
		self.Label_Requirements.setText(self.tr("Requirements"))
		self.Label_Duty.setText(self.tr("Duty"))
		self.Label_Conditions.setText(self.tr("Conditions"))
		self.MenuFile.setTitle(self.tr("&File"))
		self.MenuEdit.setTitle(self.tr("&Edit"))
		self.MenuData.setTitle(self.tr("&Data"))
		self.Action_Exit.setText(self.tr("E&xit"))
		self.Action_Import_HTML.setText(self.tr("Import from HTML"))
		self.Action_Export_HTML.setText(self.tr("Export to HTML"))
		self.Action_Import_XML.setText(self.tr("&Import from XML"))
		self.Action_Export_XML.setText(self.tr("&Export to XML"))
		self.Action_Backup_DB.setText(self.tr("&Backup DB"))
		self.Action_Restore_DB.setText(self.tr("&Restore DB"))
		self.Action_Delete_All.setText(self.tr("&Delete All"))
		self.Action_Filter.setText(self.tr("Fi&lter"))
		self.Action_Sort.setText(self.tr("S&ort"))

	def	__SetModels(self, mod):
		self.Model = mod
		self.TableView_Main.setModel(mod)
		self.selModel = QtGui.QItemSelectionModel(mod)
		self.TableView_Main.setSelectionModel(self.selModel)
		self.TableView_Main.setItemDelegate(model.CustomDelegate(self.centralwidget))

	def	__TuneTable(self):
		'''
		Tune TableView widget.
		'''
		self.TableView_Main.hideColumn(5)	# City
		self.TableView_Main.hideColumn(13)	# Requirements 
		self.TableView_Main.hideColumn(14)	# Duty
		self.TableView_Main.hideColumn(15)	# Conditions
		self.TableView_Main.hideColumn(16)	# Contact
		self.TableView_Main.hideColumn(17)	# Phone
		self.TableView_Main.hideColumn(18)	# E-Mail
	
	def	__ConnectSignals(self):
		'''
		...
		'''
		QtCore.QObject.connect(self.selModel, QtCore.SIGNAL("currentRowChanged(QModelIndex, QModelIndex)"), self.OnRowChanged)
		QtCore.QObject.connect(self.Action_Import_HTML, QtCore.SIGNAL("triggered()"), self.OnImportHTML)
		QtCore.QObject.connect(self.Action_Import_XML, QtCore.SIGNAL("triggered()"), self.OnImportXML)
		QtCore.QObject.connect(self.Action_Exit, QtCore.SIGNAL("triggered()"), QtGui.qApp, QtCore.SLOT("quit()"))
		QtCore.QObject.connect(self.Action_Delete_All, QtCore.SIGNAL("triggered()"), self.OnDeleteAll)
		#QtCore.QMetaObject.connectSlotsByName(self.centralwidget)
		#QtCore.QMetaObject.connectSlotsByName(mw)
	
	# slots
	def	OnRowChanged(self, cur, prev):
		'''
		@param cur QModelIndex - current row
		@param cur QModelIndex - previous row
		'''
		r = cur.row()
		m = self.TableView_Main.model()
		self.LineEdit_City.setText(m.data(m.index(r, 5)).toString())
		self.LineEdit_Title.setText(m.data(m.index(r, 2)).toString())
		self.LineEdit_Employer.setText(m.data(m.index(r, 4)).toString())
		self.LineEdit_Contact.setText(m.data(m.index(r, 16)).toString())
		self.LineEdit_Phone.setText(m.data(m.index(r, 17)).toString())
		self.LineEdit_Email.setText(m.data(m.index(r, 18)).toString())
		self.TextEdit_Requirement.setPlainText(m.data(m.index(r, 13)).toString())
		self.TextEdit_Duty.setPlainText(m.data(m.index(r, 14)).toString())
		self.TextEdit_Conditions.setPlainText(m.data(m.index(r, 15)).toString())

	def	OnImportHTML(self):
		fileName = QtGui.QFileDialog.getOpenFileName(self.centralwidget,
			self.centralwidget.tr("Open HTML File"),
			QtCore.QDir.currentPath(),
			self.centralwidget.tr("Hypertext file ( *.html)"))
		if not fileName.isEmpty():
			htmimpex.Import(self.centralwidget, self.Model, fileName)
			self.StatusBar.showMessage(self.tr("HTML import OK"), 2000)
			self.TableView_Main.resizeColumnsToContents()
			self.TableView_Main.resizeRowsToContents()

	def	OnImportXML(self):
		fileName = QtGui.QFileDialog.getOpenFileName(self.centralwidget,
			self.centralwidget.tr("Open XML File"),
			QtCore.QDir.currentPath(),
			self.centralwidget.tr("XML backup file ( *.xml)"))
		if not fileName.isEmpty():
			if (xmlimpex.Import(self.centralwidget, self.Model)):	#, QtCore.QString("jobru.xml")
				#self.statusBar().showMessage(self.tr("File loaded"), 2000)
				self.StatusBar.showMessage(self.tr("XML import OK"), 2000)
				self.TableView_Main.resizeColumnsToContents()
				self.TableView_Main.resizeRowsToContents()

	def	OnDeleteAll(self):
		model.DeleteAll(self.Model)
		self.TableView_Main.resizeColumnsToContents()
		self.StatusBar.showMessage(self.tr("All records deleted"), 2000)

def	Init():
	'''
	Init Qt Application. Calling on the same start.
	'''
	app = QtGui.QApplication([])
	app.setStyle("windows")
	return app

def Exec(app, mod):
	'''
	@param app:QApplication
	@param model:QSqlModel - data
	'''
	mw = QtGui.QMainWindow()
	ui = MainWindow()
	ui.setupUi(mw, mod)
	mw.show()
	ui.TableView_Main.resizeColumnsToContents()
	ui.TableView_Main.resizeRowsToContents()
	return (app.exec_())
