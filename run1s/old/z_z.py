# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/shares/home/eugene/Projects/Run1C/z_z.ui'
#
# Created: Пнд Июн 5 18:18:32 2006
#      by: The PyQt User Interface Compiler (pyuic) 3.16
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class Form(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("Form")



        self.buttonGroup1 = QButtonGroup(self,"buttonGroup1")
        self.buttonGroup1.setGeometry(QRect(100,70,111,171))

        self.radioButton1 = QRadioButton(self.buttonGroup1,"radioButton1")
        self.radioButton1.setGeometry(QRect(20,30,81,21))

        self.radioButton2 = QRadioButton(self.buttonGroup1,"radioButton2")
        self.radioButton2.setGeometry(QRect(20,60,71,21))

        self.languageChange()

        self.resize(QSize(600,480).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Form"))
        self.buttonGroup1.setTitle(self.__tr("buttonGroup1"))
        self.radioButton1.setText(self.__tr("radioButton1"))
        self.radioButton2.setText(self.__tr("radioButton2"))


    def __tr(self,s,c = None):
        return qApp.translate("Form",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = Form()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
