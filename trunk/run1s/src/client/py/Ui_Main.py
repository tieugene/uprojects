# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/shares/home/eugene/Projects/uprojects/run1c/py/client/Main.ui'
#
# Created: Tue Dec 23 17:44:13 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(376, 299)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtGui.QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtGui.QTableWidget(self.centralWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 376, 31))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuOptions = QtGui.QMenu(self.menuBar)
        self.menuOptions.setObjectName("menuOptions")
        self.menuHelp = QtGui.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuAction = QtGui.QMenu(self.menuBar)
        self.menuAction.setObjectName("menuAction")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.FileToolBar = QtGui.QToolBar(MainWindow)
        self.FileToolBar.setObjectName("FileToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.FileToolBar)
        self.OptionsToolBar = QtGui.QToolBar(MainWindow)
        self.OptionsToolBar.setObjectName("OptionsToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.OptionsToolBar)
        self.ActionsToolBar = QtGui.QToolBar(MainWindow)
        self.ActionsToolBar.setObjectName("ActionsToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.ActionsToolBar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionHelp = QtGui.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtGui.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionSettings = QtGui.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionEnterprise = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/ent_16x16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEnterprise.setIcon(icon)
        self.actionEnterprise.setObjectName("actionEnterprise")
        self.actionEnterprise_singleuser = QtGui.QAction(MainWindow)
        self.actionEnterprise_singleuser.setIcon(icon)
        self.actionEnterprise_singleuser.setObjectName("actionEnterprise_singleuser")
        self.actionConfigurer = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/cfg_16x16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConfigurer.setIcon(icon1)
        self.actionConfigurer.setObjectName("actionConfigurer")
        self.actionMonitor = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/mon_16x16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMonitor.setIcon(icon2)
        self.actionMonitor.setObjectName("actionMonitor")
        self.menuFile.addAction(self.actionExit)
        self.menuOptions.addAction(self.actionSettings)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionAbout_Qt)
        self.menuAction.addAction(self.actionEnterprise)
        self.menuAction.addAction(self.actionEnterprise_singleuser)
        self.menuAction.addAction(self.actionConfigurer)
        self.menuAction.addAction(self.actionMonitor)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuAction.menuAction())
        self.menuBar.addAction(self.menuOptions.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.FileToolBar.addAction(self.actionExit)
        self.OptionsToolBar.addAction(self.actionSettings)
        self.ActionsToolBar.addAction(self.actionEnterprise)
        self.ActionsToolBar.addAction(self.actionEnterprise_singleuser)
        self.ActionsToolBar.addAction(self.actionConfigurer)
        self.ActionsToolBar.addAction(self.actionMonitor)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "run1s", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("MainWindow", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("MainWindow", "Org", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("MainWindow", "Comments", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuOptions.setTitle(QtGui.QApplication.translate("MainWindow", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAction.setTitle(QtGui.QApplication.translate("MainWindow", "Action", None, QtGui.QApplication.UnicodeUTF8))
        self.FileToolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.OptionsToolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.ActionsToolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setText(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout_Qt.setText(QtGui.QApplication.translate("MainWindow", "About Qt", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setText(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEnterprise.setText(QtGui.QApplication.translate("MainWindow", "Enterprise", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEnterprise_singleuser.setText(QtGui.QApplication.translate("MainWindow", "Enterprise (singleuser)", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConfigurer.setText(QtGui.QApplication.translate("MainWindow", "Configurer", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMonitor.setText(QtGui.QApplication.translate("MainWindow", "Monitor", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

