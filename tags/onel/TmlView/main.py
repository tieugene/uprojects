#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Main module.
@author TI_Eugene
'''

import sys, qt
import parser, table_ui, dialog_ui

def	Run(argv):
	'''
	Main app starter.
	@param argv command line arguments (filename)
	'''
	# 1. open and parse input file
	cfg = parser.Cfg(argv[1])
	ml = cfg.Load()
	if (ml):
	# 2. prepare output
		a = qt.QApplication(argv)
		a.connect(a, qt.SIGNAL('lastWindowClosed()'), a, qt.SLOT('quit()'))
		if (ml.Type == 1):
			mw = table_ui.Table()	# was ui.MainForm()
		else:
			mw = dialog_ui.Dialog()
	# fillout Table/Dialog
		ml.FillOutUI(mw)	# was mw.MainTable
	# 3. show
		mw.show()
		a.exec_loop()

if (__name__ == '__main__'):
	Run(sys.argv)
