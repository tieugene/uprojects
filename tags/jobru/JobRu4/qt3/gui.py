# -*- coding: utf-8 -*-
'''
GUI.
@author TI_Eugene
'''

import os, qt, qttable
import main, data, backup, utility

class MainWindow (qt.QDialog):
	def	__init__(self):
		qt.QDialog.__init__(self)

		# 0. constants
		self.Const_Sex = (("*", "Не имеет значения"), ("М", "Муж"), ("Ж", "Жен"))
		self.Const_Edu = (("*", "Не имеет значения"), ("У", "Учащийся"), ("С", "Среднее"), ("СС", "Среднее специальное"), ("НВ", "Неполное высшее"), ("В", "Высшее"))
		self.Const_Exp = (("X", "Нет"), ("1", "1 год"), ("2", "2 года"), ("3", "3 года"), ("4", "4 года"), ("5", "5 лет"), (">5", "Свыше 5 лет"))
		self.Const_Emp = (("*", "Любая"), ("П", "Полная"), ("С", "По совместительству"))
		self.Const_ET = (("П", "Пердприятие"), ("А", "Агентство"))
		header = (("N", "New", 1), ("P", "Priority", 1), ("ID", None, 3), ("Date", "Date Time", 6), ("Title", "Job title"), ("ET", "Employer type", 1), ("Employer", None), ("S", "Sex", 1), ("Age", None, 2), ("Edu", "Education", 2), ("Exp", "Expreience", 1), ("Emp", "Employment", 1), ("Salary", None, 2))
		self.SQL_Order = "DateTime DESC"	# EmployerType, Employer, Title, DateTime DESC
		self.SQL_Filter = "(Priority >= 0) OR (New = 1)"
##		self.SQL_Selection = ""

		self.setCaption("Job.Ru")
		# 1. create layouts
		FormLayout = qt.QGridLayout(self, 1, 1, 6, 6)

		self.BHSplitter = qt.QSplitter(qt.QSplitter.Vertical, self)

		# 2. create widgets
		# 2.1. Buttons
		self.UpdateButton	= qt.QPushButton("&Update", self)
		self.ReloadButton	= qt.QPushButton("Re&load", self)
		self.SortButton		= qt.QPushButton("&Order", self)
		self.FilterButton	= qt.QPushButton("&Filter", self)
		self.DBBackupButton	= qt.QPushButton("DB &Backup", self)
		self.DBRestoreButton	= qt.QPushButton("DB &Restore", self)
		self.XMLBackupButton	= qt.QPushButton("&XML Backup", self)
		self.XMLRestoreButton	= qt.QPushButton("XML Restore", self)
		self.HTMLImportButton	= qt.QPushButton("HTML &Import", self)
		self.HTMLExportButton	= qt.QPushButton("HTML &Export", self)
		self.KillButton		= qt.QPushButton("&Kill All", self)
		# 2.2. Table
		self.DataTable = qttable.QTable(0, len(header), self.BHSplitter, "DataTable")
		for i in xrange(len(header)):
			self.DataTable.horizontalHeader().setLabel(i,self.__tr(header[i][0]))
			if (len(header[i]) == 3):
				self.DataTable.horizontalHeader().resizeSection(i, header[i][2] * 20)
			self.DataTable.setColumnReadOnly(i, True)	# was (i > 1)

		self.BTVSplitter = qt.QSplitter(qt.QSplitter.Horizontal, self.BHSplitter)
		self.BBVSplitter = qt.QSplitter(qt.QSplitter.Horizontal, self.BHSplitter)
		# others
		BTVWidgetL = qt.QWidget(self.BTVSplitter)
		BTVWidgetR = qt.QWidget(self.BTVSplitter)
		BBVWidgetL = qt.QWidget(self.BBVSplitter)
		BBVWidgetR = qt.QWidget(self.BBVSplitter)

		BottomTLLayout = qt.QGridLayout(BTVWidgetL, 1, 1, 6, 6)
		BottomTRLayout = qt.QVBoxLayout(BTVWidgetR, 6, 6)
		BottomBLLayout = qt.QVBoxLayout(BBVWidgetL, 6, 6)
		BottomBRLayout = qt.QVBoxLayout(BBVWidgetR, 6, 6)
		# 2.3. Others
		self.CityLabel		= qt.QLabel("City", BTVWidgetL)
		self.TitleLabel		= qt.QLabel("Title", BTVWidgetL)
		self.EmployerLabel	= qt.QLabel("Employer", BTVWidgetL)
		self.ContactLabel	= qt.QLabel("Contact", BTVWidgetL)
		self.PhoneLabel		= qt.QLabel("Phone", BTVWidgetL)
		self.EmailLabel		= qt.QLabel("E-Mail", BTVWidgetL)
		self.RequirementsLabel	= qt.QLabel("Requirements", BTVWidgetR)
		self.DutyLabel		= qt.QLabel("Duty", BBVWidgetL)
		self.ConditionsLabel	= qt.QLabel("Conditions", BBVWidgetR)

		self.CityValue		= qt.QLineEdit(BTVWidgetL)
		self.TitleValue		= qt.QLineEdit(BTVWidgetL)
		self.EmployerValue	= qt.QLineEdit(BTVWidgetL)
		self.ContactValue	= qt.QLineEdit(BTVWidgetL)
		self.PhoneValue		= qt.QLineEdit(BTVWidgetL)
		self.EmailValue		= qt.QLineEdit(BTVWidgetL)
		self.RequirementsValue	= qt.QTextEdit(BTVWidgetR)
		self.DutyValue		= qt.QTextEdit(BBVWidgetL)
		self.ConditionsValue	= qt.QTextEdit(BBVWidgetR)

		self.CityValue.setReadOnly(True)
		self.TitleValue.setReadOnly(True)
		self.EmployerValue.setReadOnly(True)
		self.ContactValue.setReadOnly(True)
		self.PhoneValue.setReadOnly(True)
		self.EmailValue.setReadOnly(True)
		self.RequirementsValue.setReadOnly(True)
		self.DutyValue.setReadOnly(True)
		self.ConditionsValue.setReadOnly(True)

		# 3. set widgets
		BottomTLLayout.addWidget(self.CityLabel, 0, 0)
		BottomTLLayout.addWidget(self.TitleLabel, 1, 0)
		BottomTLLayout.addWidget(self.EmployerLabel, 2, 0)
		BottomTLLayout.addWidget(self.ContactLabel, 3, 0)
		BottomTLLayout.addWidget(self.PhoneLabel, 4, 0)
		BottomTLLayout.addWidget(self.EmailLabel, 5, 0)
		BottomTLLayout.addWidget(self.CityValue, 0, 1)
		BottomTLLayout.addWidget(self.TitleValue, 1, 1)
		BottomTLLayout.addWidget(self.EmployerValue, 2, 1)
		BottomTLLayout.addWidget(self.ContactValue, 3, 1)
		BottomTLLayout.addWidget(self.PhoneValue, 4, 1)
		BottomTLLayout.addWidget(self.EmailValue, 5, 1)
		BottomTRLayout.addWidget(self.RequirementsLabel)
		BottomTRLayout.addWidget(self.RequirementsValue)
		BottomBLLayout.addWidget(self.DutyLabel)
		BottomBLLayout.addWidget(self.DutyValue)
		BottomBRLayout.addWidget(self.ConditionsLabel)
		BottomBRLayout.addWidget(self.ConditionsValue)

		FormLayout.addWidget(self.UpdateButton,	0, 0)
		FormLayout.addWidget(self.ReloadButton,	1, 0)
		FormLayout.addWidget(self.SortButton,		0, 1)
		FormLayout.addWidget(self.FilterButton,	1, 1)
		FormLayout.addWidget(self.DBBackupButton,	0, 2)
		FormLayout.addWidget(self.DBRestoreButton,	1, 2)
		FormLayout.addWidget(self.XMLBackupButton,	0, 3)
		FormLayout.addWidget(self.XMLRestoreButton,	1, 3)
		FormLayout.addWidget(self.HTMLImportButton,	0, 4)
		FormLayout.addWidget(self.HTMLExportButton,	1, 4)
		FormLayout.addWidget(self.KillButton,		0, 5)

		FormLayout.addMultiCellWidget(self.BHSplitter, 2, 2, 0, 5)

		self.resize(qt.QSize(790, 550).expandedTo(self.minimumSizeHint()))

		# X. set slots
		self.connect(self.DataTable,		qt.SIGNAL("currentChanged(int,int)"), self.OnCurrentChanged)

		self.connect(self.UpdateButton,		qt.SIGNAL("clicked()"), self.OnUpdateClicked)
		self.connect(self.ReloadButton,		qt.SIGNAL("clicked()"), self.OnReloadClicked)
		self.connect(self.SortButton,		qt.SIGNAL("clicked()"), self.OnSortClicked)
		self.connect(self.FilterButton,		qt.SIGNAL("clicked()"), self.OnFilterClicked)
		self.connect(self.DBBackupButton,	qt.SIGNAL("clicked()"), self.OnDBBackupClicked)
		self.connect(self.DBRestoreButton,	qt.SIGNAL("clicked()"), self.OnDBRestoreClicked)
		self.connect(self.XMLBackupButton,	qt.SIGNAL("clicked()"), self.OnXMLBackupClicked)
		self.connect(self.XMLRestoreButton,	qt.SIGNAL("clicked()"), self.OnXMLRestoreClicked)
		self.connect(self.HTMLImportButton,	qt.SIGNAL("clicked()"), self.OnHTMLImportClicked)
		self.connect(self.HTMLExportButton,	qt.SIGNAL("clicked()"), self.OnHTMLExportClicked)
		self.connect(self.KillButton,		qt.SIGNAL("clicked()"), self.OnKillClicked)
		
		# Y. Actions
		# const QString & menuText, QKeySequence accel, QObject * parent, const char * name = 0 
		self.ActionDelete	= qt.QAction("&Delete",	qt.Qt.CTRL+qt.Qt.Key_Delete,	self.DataTable)
##		self.ActionDelete	= qt.QAction("&Delete",	qt.Qt.Key_Delete,		self.DataTable)
		self.ActionPrio1	= qt.QAction("Prio &1",	qt.Qt.CTRL+qt.Qt.Key_1,		self.DataTable)
		self.ActionPrio2	= qt.QAction("Prio &2",	qt.Qt.CTRL+qt.Qt.Key_2,		self.DataTable)
		self.ActionPrio3	= qt.QAction("Prio &3",	qt.Qt.CTRL+qt.Qt.Key_3,		self.DataTable)
		self.ActionPrio4	= qt.QAction("Prio &4",	qt.Qt.CTRL+qt.Qt.Key_4,		self.DataTable)
		self.ActionPrio5	= qt.QAction("Prio &5",	qt.Qt.CTRL+qt.Qt.Key_5,		self.DataTable)
		self.ActionMailTo	= qt.QAction("&MailTo",	qt.Qt.CTRL+qt.Qt.Key_M,		self.DataTable)
		self.connect(self.ActionDelete,		qt.SIGNAL("activated()"), self.OnDelPressed)
		self.connect(self.ActionPrio1,		qt.SIGNAL("activated()"), self.OnPrio1Pressed)
		self.connect(self.ActionPrio2,		qt.SIGNAL("activated()"), self.OnPrio2Pressed)
		self.connect(self.ActionPrio3,		qt.SIGNAL("activated()"), self.OnPrio3Pressed)
		self.connect(self.ActionPrio4,		qt.SIGNAL("activated()"), self.OnPrio4Pressed)
		self.connect(self.ActionPrio5,		qt.SIGNAL("activated()"), self.OnPrio5Pressed)
		self.connect(self.ActionMailTo,		qt.SIGNAL("activated()"), self.OnMailToPressed)

	def	__tr(self,s,c = None):
		return qt.qApp.translate("Form",s,c)

	def	__X(self, s):
		return qt.QString().fromUtf8(s)
##		return qt.QString().fromLocal8Bit(s)

	def	__AgeAsStr(self, f, t):
		if (f):
			if (t):
				retvalue = "%d..%d" % (f, t)
			else:
				retvalue = ">%d" % f
		else:
			if (t):
				retvalue = "<%d" % t
			else:
				retvalue = ""
		return retvalue

	def	__GetID(self, row):
		if (row >= 0):
			return long(str(self.DataTable.text(row, 2)))
		else:
			return None

	def	__Ask(self, head, text):
		return (qt.QMessageBox(head, text,
			qt.QMessageBox.Critical,
			qt.QMessageBox.Yes,
			qt.QMessageBox.No | qt.QMessageBox.Default | qt.QMessageBox.Escape,
			qt.QMessageBox.NoButton).exec_loop() == qt.QMessageBox.Yes)
	def	__MkSQL(self):
		'''Construct SQL string to select'''
		retvalue = data.DataBase.SQL_Select
		if (len(self.SQL_Filter) > 0):
			retvalue += (" WHERE (%s)" % self.SQL_Filter)
		if (len(self.SQL_Order) > 0):
			retvalue += (" ORDER BY %s" % self.SQL_Order)
		return retvalue

	def	ReloadData(self):
		self.DataTable.setNumRows(0)
		data.DataBase.Exec(self.__MkSQL())
		self.data = data.DataBase.GetAll()
		self.IDs = {}
		self.DataTable.setNumRows(len(self.data))
		for row in xrange(len(self.data)):
			self.IDs[self.data[row][0]] = row
			self.FillOneRow(row, self.data[row])

	def	__FillCheckColumn(self, row, col, v):
		self.DataTable.item(row, col).setChecked(bool(v))

	def	__P2S(self, n):
		'''
		Get priority char by it's no
		'''

	def	__SetNew(self, row, value):
		self.DataTable.item(row, 0).setChecked(bool(value))

	def	__GetNew(self, row):
		return self.DataTable.item(row, 0).isChecked()

	def	__SetPriority(self, row, value):
		if (value < 0):
			c = "X"
		elif (value == 0):
			c = ""
		else:
			c = str(value)
		self.DataTable.setText(row, 1, c)

	def	__GetPriority(self, row):
		c = self.DataTable.text(row, 1).ascii()
		if (c == "X"):
			p = -1
		elif (c == ""):
			p = 0
		else:
			p = int(c)
		return p


	def	FillOneRow(self, row, data):
		'''	New, Updated, Deleted, Priority, ID,
			Date, Title, EType, Employer, Sex,
			Age, Employment, Salary'''
		self.DataTable.setItem(row, 0, qttable.QCheckTableItem(self.DataTable, ""))
		self.__SetNew(row, data[19])				# New
		self.__SetPriority(row, data[20])			# Priority
		self.DataTable.setText(row, 2, str(data[0]))		# ID
		self.DataTable.setText(row, 3, str(data[1]))		# Date
		self.DataTable.setText(row, 4, self.__X(data[2]))	# Title
		self.DataTable.setText(row, 5,
			self.__X(self.Const_ET[data[3]][0]))		# EmployerType
		self.DataTable.setText(row, 6, self.__X(data[4]))	# Employer
		self.DataTable.setText(row, 7,
			self.__X(self.Const_Sex[data[6]][0]))		# Sex
		self.DataTable.setText(row, 8,
			self.__AgeAsStr(data[7], data[8]))		# Age
		self.DataTable.setText(row, 9,
			self.__X(self.Const_Edu[data[9]][0]))		# Education
		self.DataTable.setText(row, 10,
			self.__X(self.Const_Exp[data[10]][0]))		# Experience
		self.DataTable.setText(row, 11,
			self.__X(self.Const_Emp[data[11]][0]))		# Employment
		self.DataTable.setText(row, 12, str(data[12]))		# Salary

	def	FillOneSub(self, data):
		self.CityValue.setText(self.__X(data[5]))
		self.TitleValue.setText(self.__X(data[2]))
		self.EmployerValue.setText(self.__X(data[4]))
		self.ContactValue.setText(self.__X(data[16]))
		self.PhoneValue.setText(self.__X(data[17]))
		self.EmailValue.setText(self.__X(data[18]))
		self.RequirementsValue.setText(self.__X(data[13]))
		self.DutyValue.setText(self.__X(data[14]))
		self.ConditionsValue.setText(self.__X(data[15]))

	# Slots
	def	OnCurrentChanged(self, row, col):
		id = self.__GetID(row)
		if (id):
			data = self.data[self.IDs[id]]
			self.FillOneSub(data)

	def	OnUpdateClicked(self):
		Flag = False	# flag to reload
		for row in xrange(len(self.data)):
			new_new  = self.__GetNew(row)
			new_prio = self.__GetPriority(row)
			if ((new_new <> self.data[row][19]) or (new_prio <> self.data[row][20])):
				data.DataBase.UpdateNewPrio(self.data[row][0], new_new, new_prio)
				Flag = True
		if (Flag):
			self.ReloadData()

	def	OnReloadClicked(self):
		self.ReloadData()

	def	OnSortClicked(self):
		s, ok = qt.QInputDialog.getText("Sorting by", "Sort:", qt.QLineEdit.Normal, self.SQL_Order)
		if (ok):
			self.SQL_Order = s.ascii()
			self.ReloadData()

	def	OnFilterClicked(self):
		s, ok = qt.QInputDialog.getText("Sorting by", "Sort:", qt.QLineEdit.Normal, self.SQL_Filter)
		if (ok):
			self.SQL_Filter = s.ascii()
##			print "Filter:", type(self.SQL_Filter).__name__, self.SQL_Filter
			self.ReloadData()

	def	OnDBBackupClicked(self):
		data.DataBase.Backup()

	def	OnDBRestoreClicked(self):
		if (self.__Ask("DB Restore", "All current data will B replaced w/ backuped. R U sure?")):
			data.DataBase.Restore()
			self.ReloadData()

	def	OnXMLBackupClicked(self):
		backup.Backup("jobru.xml")

	def	OnXMLRestoreClicked(self):
		pass
		if (self.__Ask("XML Restore", "All current data will B replaced w/ backuped. R U sure?")):
			backup.Restore("jobru.xml")
##			self.ReloadData()

	def	OnHTMLImportClicked(self):
		retvalue = []
		filelist = qt.QFileDialog.getOpenFileNames(
			"Hypertext (*.htm *.html)", ".", self, "open files dialog",
			"Select one or more files to open" );
		for f in filelist:
			retvalue.append(str(f))
		if (len(retvalue)):
			main.ImportFromHTML(retvalue)
			self.ReloadData()

	def	OnHTMLExportClicked(self):
		pass

	def	OnKillClicked(self):
		if (self.__Ask("Droping database", "R U realy want delete all data from database?")):
			data.DataBase.KillAll()
			self.ReloadData()

	# Key Actions
	def	__OnAnyPressed(self, p):
		'''
		Common action handler.
		@param p:int - -1, 1..5 - priority to set
		'''
		row = self.DataTable.currentRow()
		if (row >= 0):
			self.__SetNew(row, False)			# New
			self.__SetPriority(row, p)			# Priority

	def	OnDelPressed(self):
		self.__OnAnyPressed(-1)
	def	OnPrio1Pressed(self):
		self.__OnAnyPressed(1)
	def	OnPrio2Pressed(self):
		self.__OnAnyPressed(2)
	def	OnPrio3Pressed(self):
		self.__OnAnyPressed(3)
	def	OnPrio4Pressed(self):
		self.__OnAnyPressed(4)
	def	OnPrio5Pressed(self):
		self.__OnAnyPressed(5)

	def	OnMailToPressed(self):
		row = self.DataTable.currentRow()
		if (row >= 0):
			rec = self.data[row]
			to = rec[18]							# EmailLabel
			subj = utility.XCode("Резюме - " + rec[2], utility.UTF8)	# Title
			ID = rec[0]
			Contact = utility.XCode(rec[16], utility.UTF8)
			body = open("template.txt").read() % (Contact, ID)
			command = "kmail --composer -s \"%s\" --body \"%s\" %s" % (subj, body, to)
			os.system(command)

def	Exec():
	a = qt.QApplication([])
##	qt.QTextCodec.setCodecForCStrings(qt.QTextCodec.codecForLocale())	# UTF8
	a.setStyle('windows')
	f = qt.QFont()
	f.setPointSize(10)
	a.setFont(f)
	qt.QObject.connect(a, qt.SIGNAL("lastWindowClosed()"), a, qt.SLOT("quit()"))
	w = MainWindow()
	a.setMainWidget(w)
	w.show()
	w.ReloadData()
	a.exec_loop()
