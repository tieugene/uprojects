# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/eugene/src/Python/TmlView/z_example.ui'
#
# Created: Сбт Янв 28 17:40:01 2006
#      by: The PyQt User Interface Compiler (pyuic) 3.15.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *
from qttable import QTable


class MainForm(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("MainForm")



        self.MainTable = QTable(self,"MainTable")
        self.MainTable.setGeometry(QRect(6,6,500,160))
        self.MainTable.setNumRows(3)
        self.MainTable.setNumCols(3)

        self.groupBox1 = QGroupBox(self,"groupBox1")
        self.groupBox1.setGeometry(QRect(140,190,111,80))

        self.radioButton3 = QRadioButton(self.groupBox1,"radioButton3")
        self.radioButton3.setGeometry(QRect(10,20,91,21))

        self.radioButton4 = QRadioButton(self.groupBox1,"radioButton4")
        self.radioButton4.setGeometry(QRect(10,50,91,21))

        self.buttonGroup1 = QButtonGroup(self,"buttonGroup1")
        self.buttonGroup1.setGeometry(QRect(10,180,111,60))

        self.radioButton1 = QRadioButton(self.buttonGroup1,"radioButton1")
        self.radioButton1.setGeometry(QRect(10,10,100,21))

        self.radioButton2 = QRadioButton(self.buttonGroup1,"radioButton2")
        self.radioButton2.setGeometry(QRect(10,30,91,21))

        self.languageChange()

        self.resize(QSize(626,504).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Form"))
        self.groupBox1.setTitle(self.__tr("groupBox1"))
        self.radioButton3.setText(self.__tr("radioButton3"))
        self.radioButton4.setText(self.__tr("radioButton4"))
        self.buttonGroup1.setTitle(self.__tr("buttonGroup1"))
        self.radioButton1.setText(self.__tr("radioButton1"))
        self.radioButton2.setText(self.__tr("radioButton2"))


    def __tr(self,s,c = None):
        return qApp.translate("MainForm",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = MainForm()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
