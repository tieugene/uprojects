# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/eugene/src/Python/TmlView/z_cellprop_t.ui'
#
# Created: Сбт Дек 31 20:05:43 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.15.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class MyDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("MyDialog")

        self.setSizeGripEnabled(1)

        MyDialogLayout = QGridLayout(self,1,1,6,6,"MyDialogLayout")

        layout5 = QVBoxLayout(None,0,6,"layout5")

        self.MainListView = QListView(self,"MainListView")
        self.MainListView.addColumn(self.__tr("Name"))
        self.MainListView.addColumn(self.__tr("Value"))
        layout5.addWidget(self.MainListView)

        layout2 = QHBoxLayout(None,0,6,"layout2")

        self.buttonHelp = QPushButton(self,"buttonHelp")
        self.buttonHelp.setAutoDefault(1)
        layout2.addWidget(self.buttonHelp)
        Horizontal_Spacing2 = QSpacerItem(220,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout2.addItem(Horizontal_Spacing2)

        self.buttonApply = QPushButton(self,"buttonApply")
        self.buttonApply.setAutoDefault(1)
        self.buttonApply.setDefault(1)
        layout2.addWidget(self.buttonApply)

        self.buttonOk = QPushButton(self,"buttonOk")
        self.buttonOk.setAutoDefault(1)
        self.buttonOk.setDefault(1)
        layout2.addWidget(self.buttonOk)

        self.buttonCancel = QPushButton(self,"buttonCancel")
        self.buttonCancel.setAutoDefault(1)
        layout2.addWidget(self.buttonCancel)
        layout5.addLayout(layout2)

        MyDialogLayout.addLayout(layout5,0,0)

        self.languageChange()

        self.resize(QSize(582,290).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.buttonOk,SIGNAL("clicked()"),self.accept)
        self.connect(self.buttonCancel,SIGNAL("clicked()"),self.reject)


    def languageChange(self):
        self.setCaption(self.__tr("MyDialog"))
        self.MainListView.header().setLabel(0,self.__tr("Name"))
        self.MainListView.header().setLabel(1,self.__tr("Value"))
        self.MainListView.clear()
        item_2 = QListViewItem(self.MainListView,None)
        item_2.setOpen(1)
        item = QListViewItem(item_2,None)
        item.setText(0,self.__tr("Type"))
        item_2.setOpen(1)
        item = QListViewItem(item_2,item)
        item.setText(0,self.__tr("Control"))
        item_2.setOpen(1)
        item = QListViewItem(item_2,item)
        item.setText(0,self.__tr("Contents"))
        item_2.setOpen(1)
        item = QListViewItem(item_2,item)
        item.setText(0,self.__tr("Description"))
        item_2.setOpen(1)
        item = QListViewItem(item_2,item)
        item.setText(0,self.__tr("Protection"))
        item_2.setText(0,self.__tr("Text"))

        item_3 = QListViewItem(self.MainListView,item_2)
        item_3.setOpen(1)
        item = QListViewItem(item_3,item_2)
        item.setText(0,self.__tr("Horisontal"))
        item_3.setOpen(1)
        item = QListViewItem(item_3,item)
        item.setText(0,self.__tr("Vertical"))
        item_3.setOpen(1)
        item = QListViewItem(item_3,item)
        item.setText(0,self.__tr("Angle"))
        item_3.setOpen(1)
        item = QListViewItem(item_3,item)
        item.setText(0,self.__tr("On selected columns"))
        item_3.setText(0,self.__tr("Align"))

        item_4 = QListViewItem(self.MainListView,item_3)
        item_4.setOpen(1)
        item = QListViewItem(item_4,item_3)
        item.setText(0,self.__tr("Name"))
        item_4.setOpen(1)
        item = QListViewItem(item_4,item)
        item.setText(0,self.__tr("Size"))
        item_4.setOpen(1)
        item = QListViewItem(item_4,item)
        item.setText(0,self.__tr("Bold"))
        item_4.setOpen(1)
        item = QListViewItem(item_4,item)
        item.setText(0,self.__tr("Italic"))
        item_4.setOpen(1)
        item = QListViewItem(item_4,item)
        item.setText(0,self.__tr("Underline"))
        item_4.setOpen(1)
        item = QListViewItem(item_4,item)
        item.setText(0,self.__tr("Color"))
        item_4.setText(0,self.__tr("Font"))

        item_5 = QListViewItem(self.MainListView,item_4)
        item_5.setOpen(1)
        item = QListViewItem(item_5,item_4)
        item.setText(0,self.__tr("Left"))
        item_5.setOpen(1)
        item = QListViewItem(item_5,item)
        item.setText(0,self.__tr("Top"))
        item_5.setOpen(1)
        item = QListViewItem(item_5,item)
        item.setText(0,self.__tr("Right"))
        item_5.setOpen(1)
        item = QListViewItem(item_5,item)
        item.setText(0,self.__tr("Bottom"))
        item_5.setOpen(1)
        item = QListViewItem(item_5,item)
        item.setText(0,self.__tr("All"))
        item_5.setOpen(1)
        item = QListViewItem(item_5,item)
        item.setText(0,self.__tr("Color"))
        item_5.setText(0,self.__tr("Border"))

        item_6 = QListViewItem(self.MainListView,item_5)
        item_6.setOpen(1)
        item = QListViewItem(item_6,item_5)
        item.setText(0,self.__tr("Background color"))
        item_6.setOpen(1)
        item = QListViewItem(item_6,item)
        item.setText(0,self.__tr("Foreground color"))
        item_6.setOpen(1)
        item = QListViewItem(item_6,item)
        item.setText(0,self.__tr("Style"))
        item_6.setText(0,self.__tr("Pattern"))

        self.buttonHelp.setText(self.__tr("&Help"))
        self.buttonHelp.setAccel(self.__tr("F1"))
        self.buttonApply.setText(self.__tr("&Apply"))
        self.buttonApply.setAccel(self.__tr("Alt+A"))
        self.buttonOk.setText(self.__tr("&OK"))
        self.buttonOk.setAccel(QString.null)
        self.buttonCancel.setText(self.__tr("&Cancel"))
        self.buttonCancel.setAccel(QString.null)


    def __tr(self,s,c = None):
        return qApp.translate("MyDialog",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = MyDialog()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
