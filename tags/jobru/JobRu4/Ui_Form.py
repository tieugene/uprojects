# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'unknown'
#
# Created: Mon Aug  7 23:20:09 2006
#      by: PyQt4 UI code generator 4.0beta1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,453,544).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.Label_Conditions = QtGui.QLabel(self.centralwidget)
        self.Label_Conditions.setObjectName("Label_Conditions")
        self.vboxlayout.addWidget(self.Label_Conditions)

        self.TextBrowser_Conditions = QtGui.QTextBrowser(self.centralwidget)
        self.TextBrowser_Conditions.setObjectName("TextBrowser_Conditions")
        self.vboxlayout.addWidget(self.TextBrowser_Conditions)
        self.gridlayout.addLayout(self.vboxlayout,2,1,1,1)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.Label_Duty = QtGui.QLabel(self.centralwidget)
        self.Label_Duty.setObjectName("Label_Duty")
        self.vboxlayout1.addWidget(self.Label_Duty)

        self.TextBrowser_Duty = QtGui.QTextBrowser(self.centralwidget)
        self.TextBrowser_Duty.setObjectName("TextBrowser_Duty")
        self.vboxlayout1.addWidget(self.TextBrowser_Duty)
        self.gridlayout.addLayout(self.vboxlayout1,2,0,1,1)

        self.TableView_Main = QtGui.QTableView(self.centralwidget)
        self.TableView_Main.setObjectName("TableView_Main")
        self.gridlayout.addWidget(self.TableView_Main,0,0,1,2)

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.Label_Phone = QtGui.QLabel(self.centralwidget)
        self.Label_Phone.setObjectName("Label_Phone")
        self.gridlayout1.addWidget(self.Label_Phone,4,0,1,1)

        self.lineEdit_5 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridlayout1.addWidget(self.lineEdit_5,4,1,1,1)

        self.lineEdit_4 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridlayout1.addWidget(self.lineEdit_4,3,1,1,1)

        self.LineEdit_City = QtGui.QLineEdit(self.centralwidget)
        self.LineEdit_City.setObjectName("LineEdit_City")
        self.gridlayout1.addWidget(self.LineEdit_City,0,1,1,1)

        self.LineEdit_Experience = QtGui.QLineEdit(self.centralwidget)
        self.LineEdit_Experience.setObjectName("LineEdit_Experience")
        self.gridlayout1.addWidget(self.LineEdit_Experience,2,1,1,1)

        self.Label_City = QtGui.QLabel(self.centralwidget)
        self.Label_City.setObjectName("Label_City")
        self.gridlayout1.addWidget(self.Label_City,0,0,1,1)

        self.Label_Education = QtGui.QLabel(self.centralwidget)
        self.Label_Education.setObjectName("Label_Education")
        self.gridlayout1.addWidget(self.Label_Education,1,0,1,1)

        self.Label_Experience = QtGui.QLabel(self.centralwidget)
        self.Label_Experience.setObjectName("Label_Experience")
        self.gridlayout1.addWidget(self.Label_Experience,2,0,1,1)

        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.gridlayout1.addWidget(self.label_6,5,0,1,1)

        self.LineEdit_Education = QtGui.QLineEdit(self.centralwidget)
        self.LineEdit_Education.setObjectName("LineEdit_Education")
        self.gridlayout1.addWidget(self.LineEdit_Education,1,1,1,1)

        self.Label_Contact = QtGui.QLabel(self.centralwidget)
        self.Label_Contact.setObjectName("Label_Contact")
        self.gridlayout1.addWidget(self.Label_Contact,3,0,1,1)

        self.lineEdit_6 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.gridlayout1.addWidget(self.lineEdit_6,5,1,1,1)
        self.gridlayout.addLayout(self.gridlayout1,1,0,1,1)

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setMargin(0)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.Label_Requirements = QtGui.QLabel(self.centralwidget)
        self.Label_Requirements.setObjectName("Label_Requirements")
        self.vboxlayout2.addWidget(self.Label_Requirements)

        self.TextBrowser_Requirement = QtGui.QTextBrowser(self.centralwidget)
        self.TextBrowser_Requirement.setObjectName("TextBrowser_Requirement")
        self.vboxlayout2.addWidget(self.TextBrowser_Requirement)
        self.gridlayout.addLayout(self.vboxlayout2,1,1,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,453,29))
        self.menubar.setObjectName("menubar")

        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")

        self.menuData = QtGui.QMenu(self.menubar)
        self.menuData.setObjectName("menuData")

        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionImport_from_HTML = QtGui.QAction(MainWindow)
        self.actionImport_from_HTML.setObjectName("actionImport_from_HTML")

        self.actionExport_to_HTML = QtGui.QAction(MainWindow)
        self.actionExport_to_HTML.setObjectName("actionExport_to_HTML")

        self.actionImport_from_XML = QtGui.QAction(MainWindow)
        self.actionImport_from_XML.setObjectName("actionImport_from_XML")

        self.actionBackup_ti_XML = QtGui.QAction(MainWindow)
        self.actionBackup_ti_XML.setObjectName("actionBackup_ti_XML")

        self.actionBackup_DB = QtGui.QAction(MainWindow)
        self.actionBackup_DB.setObjectName("actionBackup_DB")

        self.actionRestore_DB = QtGui.QAction(MainWindow)
        self.actionRestore_DB.setObjectName("actionRestore_DB")

        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")

        self.actionFilter = QtGui.QAction(MainWindow)
        self.actionFilter.setObjectName("actionFilter")

        self.actionSort = QtGui.QAction(MainWindow)
        self.actionSort.setObjectName("actionSort")
        self.menuData.addAction(self.actionFilter)
        self.menuData.addAction(self.actionSort)
        self.menuFile.addAction(self.actionImport_from_HTML)
        self.menuFile.addAction(self.actionExport_to_HTML)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionImport_from_XML)
        self.menuFile.addAction(self.actionBackup_ti_XML)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionBackup_DB)
        self.menuFile.addAction(self.actionRestore_DB)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuData.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def tr(self, string):
        return QtGui.QApplication.translate("MainWindow", string, None, QtGui.QApplication.UnicodeUTF8)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(self.tr("MainWindow"))
        self.Label_Conditions.setText(self.tr("Conditions"))
        self.Label_Duty.setText(self.tr("Duty"))
        self.Label_Phone.setText(self.tr("Phone"))
        self.Label_City.setText(self.tr("City"))
        self.Label_Education.setText(self.tr("Title"))
        self.Label_Experience.setText(self.tr("Employer"))
        self.label_6.setText(self.tr("E-Mail"))
        self.Label_Contact.setText(self.tr("Contact"))
        self.Label_Requirements.setText(self.tr("Requirements"))
        self.menuEdit.setTitle(self.tr("Edit"))
        self.menuData.setTitle(self.tr("Data"))
        self.menuFile.setTitle(self.tr("File"))
        self.actionImport_from_HTML.setText(self.tr("Import from HTML"))
        self.actionExport_to_HTML.setText(self.tr("Export to HTML"))
        self.actionImport_from_XML.setText(self.tr("Backup to XML"))
        self.actionBackup_ti_XML.setText(self.tr("Restore from XML"))
        self.actionBackup_DB.setText(self.tr("Backup DB"))
        self.actionRestore_DB.setText(self.tr("Restore DB"))
        self.actionExit.setText(self.tr("Exit"))
        self.actionFilter.setText(self.tr("Filter"))
        self.actionSort.setText(self.tr("Sort"))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
