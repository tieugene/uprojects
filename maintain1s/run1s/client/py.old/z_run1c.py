# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/eugene/Projects/Run1C/z_run1c.ui'
#
# Created: Пнд Июн 5 00:03:12 2006
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


        FormLayout = QGridLayout(self,1,1,6,6,"FormLayout")

        self.pushButton2 = QPushButton(self,"pushButton2")

        FormLayout.addWidget(self.pushButton2,2,1)

        self.listView1 = QListView(self,"listView1")
        self.listView1.addColumn(self.__tr("Column 1"))

        FormLayout.addMultiCellWidget(self.listView1,1,1,0,1)

        self.pushButton1 = QPushButton(self,"pushButton1")

        FormLayout.addWidget(self.pushButton1,2,0)

        self.ModeBox = QGroupBox(self,"ModeBox")
        self.ModeBox.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.ModeBox.sizePolicy().hasHeightForWidth()))

        self.radioButton2 = QRadioButton(self.ModeBox,"radioButton2")
        self.radioButton2.setGeometry(QRect(10,40,150,21))

        self.radioButton3 = QRadioButton(self.ModeBox,"radioButton3")
        self.radioButton3.setGeometry(QRect(10,60,150,21))

        self.radioButton1 = QRadioButton(self.ModeBox,"radioButton1")
        self.radioButton1.setGeometry(QRect(10,20,150,21))

        self.radioButton4 = QRadioButton(self.ModeBox,"radioButton4")
        self.radioButton4.setGeometry(QRect(10,80,150,21))

        FormLayout.addMultiCellWidget(self.ModeBox,0,0,0,1)

        self.languageChange()

        self.resize(QSize(191,256).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Form"))
        self.pushButton2.setText(self.__tr("Cancel"))
        self.listView1.header().setLabel(0,self.__tr("Column 1"))
        self.listView1.clear()
        item = QListViewItem(self.listView1,None)
        item.setText(0,self.__tr("New Item"))

        self.pushButton1.setText(self.__tr("OK"))
        self.ModeBox.setTitle(self.__tr("1C mode"))
        self.radioButton2.setText(self.__tr("Enterprise (singleuser)"))
        self.radioButton3.setText(self.__tr("Designer"))
        self.radioButton1.setText(self.__tr("Enterprise"))
        self.radioButton4.setText(self.__tr("Monitor"))


    def __tr(self,s,c = None):
        return qApp.translate("Form",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = Form()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
