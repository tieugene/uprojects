# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/shares/home/eugene/Projects/uprojects/run1c/py/client/Settings.ui'
#
# Created: Tue Dec 23 18:33:10 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.resize(277, 194)
        self.gridLayout = QtGui.QGridLayout(SettingsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.labelServer = QtGui.QLabel(SettingsDialog)
        self.labelServer.setObjectName("labelServer")
        self.gridLayout.addWidget(self.labelServer, 0, 0, 1, 1)
        self.leServer = QtGui.QLineEdit(SettingsDialog)
        self.leServer.setObjectName("leServer")
        self.gridLayout.addWidget(self.leServer, 0, 1, 1, 2)
        self.labelLogin = QtGui.QLabel(SettingsDialog)
        self.labelLogin.setObjectName("labelLogin")
        self.gridLayout.addWidget(self.labelLogin, 1, 0, 1, 1)
        self.leLogin = QtGui.QLineEdit(SettingsDialog)
        self.leLogin.setObjectName("leLogin")
        self.gridLayout.addWidget(self.leLogin, 1, 1, 1, 2)
        self.labelPassword = QtGui.QLabel(SettingsDialog)
        self.labelPassword.setObjectName("labelPassword")
        self.gridLayout.addWidget(self.labelPassword, 2, 0, 1, 1)
        self.lePassword = QtGui.QLineEdit(SettingsDialog)
        self.lePassword.setEchoMode(QtGui.QLineEdit.Password)
        self.lePassword.setObjectName("lePassword")
        self.gridLayout.addWidget(self.lePassword, 2, 1, 1, 2)
        self.label1sPath = QtGui.QLabel(SettingsDialog)
        self.label1sPath.setObjectName("label1sPath")
        self.gridLayout.addWidget(self.label1sPath, 3, 0, 1, 1)
        self.lePath = QtGui.QLineEdit(SettingsDialog)
        self.lePath.setObjectName("lePath")
        self.gridLayout.addWidget(self.lePath, 3, 1, 1, 1)
        self.pbPath = QtGui.QPushButton(SettingsDialog)
        self.pbPath.setObjectName("pbPath")
        self.gridLayout.addWidget(self.pbPath, 3, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(SettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 3)
        self.labelServer.setBuddy(self.leServer)
        self.labelLogin.setBuddy(self.leLogin)
        self.labelPassword.setBuddy(self.lePassword)
        self.label1sPath.setBuddy(self.lePath)

        self.retranslateUi(SettingsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), SettingsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), SettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QtGui.QApplication.translate("SettingsDialog", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.labelServer.setText(QtGui.QApplication.translate("SettingsDialog", "&Server:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelLogin.setText(QtGui.QApplication.translate("SettingsDialog", "&Login:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPassword.setText(QtGui.QApplication.translate("SettingsDialog", "&Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.label1sPath.setText(QtGui.QApplication.translate("SettingsDialog", "&1C path:", None, QtGui.QApplication.UnicodeUTF8))
        self.pbPath.setText(QtGui.QApplication.translate("SettingsDialog", "...", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SettingsDialog = QtGui.QDialog()
    ui = Ui_SettingsDialog()
    ui.setupUi(SettingsDialog)
    SettingsDialog.show()
    sys.exit(app.exec_())

