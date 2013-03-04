# -*- coding: utf-8 -*-

'''
Property dialog.
'''

import sys
from qt import *

class	PropDialog(QDialog):
	def __init__(self, name):
		QDialog.__init__(self, None, name, 0, 0)
		self.setSizeGripEnabled(1)
		MyDialogLayout = QGridLayout(self,1,1,1,1,"MyDialogLayout")
		self.MainListView = QListView(self,"MainListView")
		self.MainListView.addColumn("Name")
		self.MainListView.addColumn("Value")
		MyDialogLayout.addWidget(self.MainListView,0,0)
		self.setCaption(name)
		self.MainListView.setSorting(-1)
		self.resize(QSize(300, 500).expandedTo(self.minimumSizeHint()))
		self.clearWState(Qt.WState_Polished)
