# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/shares/data/eugene/Projects/JobRu/z_form.ui'
#
# Created: Сбт Май 20 20:57:55 2006
#      by: The PyQt User Interface Compiler (pyuic) 3.16
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *
from qttable import QTable


class Form(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("Form")


        FormLayout = QGridLayout(self,1,1,6,6,"FormLayout")

        self.BHSplitter = QSplitter(self,"BHSplitter")
        self.BHSplitter.setOrientation(QSplitter.Vertical)

        self.DataTable = QTable(self.BHSplitter,"DataTable")
        self.DataTable.setNumCols(self.DataTable.numCols() + 1)
        self.DataTable.horizontalHeader().setLabel(self.DataTable.numCols() - 1,self.__tr("New"))
        self.DataTable.setNumCols(self.DataTable.numCols() + 1)
        self.DataTable.horizontalHeader().setLabel(self.DataTable.numCols() - 1,self.__tr("Priority"))
        self.DataTable.setNumCols(self.DataTable.numCols() + 1)
        self.DataTable.horizontalHeader().setLabel(self.DataTable.numCols() - 1,self.__tr("ID"))
        self.DataTable.setNumCols(self.DataTable.numCols() + 1)
        self.DataTable.horizontalHeader().setLabel(self.DataTable.numCols() - 1,self.__tr("DateTime"))
        self.DataTable.setNumCols(self.DataTable.numCols() + 1)
        self.DataTable.horizontalHeader().setLabel(self.DataTable.numCols() - 1,self.__tr("Title"))
        self.DataTable.setNumCols(self.DataTable.numCols() + 1)
        self.DataTable.horizontalHeader().setLabel(self.DataTable.numCols() - 1,self.__tr("EType"))
        self.DataTable.setNumCols(self.DataTable.numCols() + 1)
        self.DataTable.horizontalHeader().setLabel(self.DataTable.numCols() - 1,self.__tr("Employer"))
        self.DataTable.setNumCols(self.DataTable.numCols() + 1)
        self.DataTable.horizontalHeader().setLabel(self.DataTable.numCols() - 1,self.__tr("Sex"))
        self.DataTable.setNumCols(self.DataTable.numCols() + 1)
        self.DataTable.horizontalHeader().setLabel(self.DataTable.numCols() - 1,self.__tr("Age"))
        self.DataTable.setNumCols(self.DataTable.numCols() + 1)
        self.DataTable.horizontalHeader().setLabel(self.DataTable.numCols() - 1,self.__tr("Employment"))
        self.DataTable.setNumCols(self.DataTable.numCols() + 1)
        self.DataTable.horizontalHeader().setLabel(self.DataTable.numCols() - 1,self.__tr("Salary"))
        self.DataTable.setNumRows(0)
        self.DataTable.setNumCols(11)

        self.BTVSplitter = QSplitter(self.BHSplitter,"BTVSplitter")
        self.BTVSplitter.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.BTVSplitter.sizePolicy().hasHeightForWidth()))
        self.BTVSplitter.setOrientation(QSplitter.Horizontal)

        LayoutWidget = QWidget(self.BTVSplitter,"BottomTLLayout")
        BottomTLLayout = QGridLayout(LayoutWidget,1,1,6,6,"BottomTLLayout")

        self.EmailValue = QLineEdit(LayoutWidget,"EmailValue")

        BottomTLLayout.addWidget(self.EmailValue,5,1)

        self.CityValue = QLineEdit(LayoutWidget,"CityValue")

        BottomTLLayout.addWidget(self.CityValue,0,1)

        self.EmailLabel = QLabel(LayoutWidget,"EmailLabel")

        BottomTLLayout.addWidget(self.EmailLabel,5,0)

        self.ContactLabel = QLabel(LayoutWidget,"ContactLabel")

        BottomTLLayout.addWidget(self.ContactLabel,3,0)

        self.EducationLabel = QLabel(LayoutWidget,"EducationLabel")

        BottomTLLayout.addWidget(self.EducationLabel,1,0)

        self.CityLabel = QLabel(LayoutWidget,"CityLabel")

        BottomTLLayout.addWidget(self.CityLabel,0,0)

        self.PhoneLabel = QLabel(LayoutWidget,"PhoneLabel")

        BottomTLLayout.addWidget(self.PhoneLabel,4,0)

        self.PhoneValue = QLineEdit(LayoutWidget,"PhoneValue")

        BottomTLLayout.addWidget(self.PhoneValue,4,1)

        self.ExperienceValue = QLineEdit(LayoutWidget,"ExperienceValue")

        BottomTLLayout.addWidget(self.ExperienceValue,2,1)

        self.ExperiaenceLabel = QLabel(LayoutWidget,"ExperiaenceLabel")

        BottomTLLayout.addWidget(self.ExperiaenceLabel,2,0)

        self.ContactValue = QLineEdit(LayoutWidget,"ContactValue")

        BottomTLLayout.addWidget(self.ContactValue,3,1)

        self.EducationValue = QLineEdit(LayoutWidget,"EducationValue")

        BottomTLLayout.addWidget(self.EducationValue,1,1)

        LayoutWidget_2 = QWidget(self.BTVSplitter,"BottomTRLayout")
        BottomTRLayout = QVBoxLayout(LayoutWidget_2,6,6,"BottomTRLayout")

        self.RequirementsLabel = QLabel(LayoutWidget_2,"RequirementsLabel")
        BottomTRLayout.addWidget(self.RequirementsLabel)

        self.RequirementsValue = QTextEdit(LayoutWidget_2,"RequirementsValue")
        BottomTRLayout.addWidget(self.RequirementsValue)

        self.BBVSplitter = QSplitter(self.BHSplitter,"BBVSplitter")
        self.BBVSplitter.setOrientation(QSplitter.Horizontal)

        LayoutWidget_3 = QWidget(self.BBVSplitter,"BottomBLLayout")
        BottomBLLayout = QVBoxLayout(LayoutWidget_3,6,6,"BottomBLLayout")

        self.DutyLabel = QLabel(LayoutWidget_3,"DutyLabel")
        BottomBLLayout.addWidget(self.DutyLabel)

        self.DutyValue = QTextEdit(LayoutWidget_3,"DutyValue")
        BottomBLLayout.addWidget(self.DutyValue)

        LayoutWidget_4 = QWidget(self.BBVSplitter,"BottomBRLayout")
        BottomBRLayout = QVBoxLayout(LayoutWidget_4,6,6,"BottomBRLayout")

        self.ConditionsLabel = QLabel(LayoutWidget_4,"ConditionsLabel")
        BottomBRLayout.addWidget(self.ConditionsLabel)

        self.ConditionsValue = QTextEdit(LayoutWidget_4,"ConditionsValue")
        BottomBRLayout.addWidget(self.ConditionsValue)

        FormLayout.addMultiCellWidget(self.BHSplitter,1,1,0,1)

        self.pushButton1 = QPushButton(self,"pushButton1")

        FormLayout.addWidget(self.pushButton1,0,0)

        self.pushButton1_2 = QPushButton(self,"pushButton1_2")

        FormLayout.addWidget(self.pushButton1_2,0,1)

        self.languageChange()

        self.resize(QSize(475,570).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.CityValue,SIGNAL("textChanged(const QString&)"),self.MySlot)


    def languageChange(self):
        self.setCaption(self.__tr("Form"))
        self.DataTable.horizontalHeader().setLabel(0,self.__tr("New"))
        self.DataTable.horizontalHeader().setLabel(1,self.__tr("Priority"))
        self.DataTable.horizontalHeader().setLabel(2,self.__tr("ID"))
        self.DataTable.horizontalHeader().setLabel(3,self.__tr("DateTime"))
        self.DataTable.horizontalHeader().setLabel(4,self.__tr("Title"))
        self.DataTable.horizontalHeader().setLabel(5,self.__tr("EType"))
        self.DataTable.horizontalHeader().setLabel(6,self.__tr("Employer"))
        self.DataTable.horizontalHeader().setLabel(7,self.__tr("Sex"))
        self.DataTable.horizontalHeader().setLabel(8,self.__tr("Age"))
        self.DataTable.horizontalHeader().setLabel(9,self.__tr("Employment"))
        self.DataTable.horizontalHeader().setLabel(10,self.__tr("Salary"))
        self.EmailLabel.setText(self.__tr("Experience"))
        self.ContactLabel.setText(self.__tr("Contact"))
        self.EducationLabel.setText(self.__tr("Education"))
        self.CityLabel.setText(self.__tr("City"))
        self.PhoneLabel.setText(self.__tr("Phone"))
        self.ExperiaenceLabel.setText(self.__tr("Experience"))
        self.RequirementsLabel.setText(self.__tr("Requirements"))
        self.DutyLabel.setText(self.__tr("Duty"))
        self.ConditionsLabel.setText(self.__tr("Conditions"))
        self.pushButton1.setText(self.__tr("pushButton1"))
        self.pushButton1_2.setText(self.__tr("pushButton1"))


    def MySlot(self):
        print "tratata"
        

    def __tr(self,s,c = None):
        return qApp.translate("Form",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = Form()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
