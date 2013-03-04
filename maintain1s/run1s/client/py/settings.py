# -*- coding: utf-8 -*-
'''
'''

import		os, platform, sys
from	PyQt4	import QtCore, QtGui
import	Ui_Settings

### Variables
dSettings	= None

# Application
Application		= QtCore.QObject()
Application.sName	= "run1s"
Application.sVersion	= "0.1"
Application.sRelease	= "0"
Application.sDomain	= "code.google.com/p/uprojects"
QtCore.QCoreApplication.setApplicationName( Application.sName )

# Author
Author			= QtCore.QObject()
Author.sName		= "TI_Eugene"
Author.Email		= QtCore.QObject()
Author.Email.sUser	= "ti.eugene"
Author.Email.sDomain	= "@gmail.com"
QtCore.QCoreApplication.setOrganizationName( Author.sName )
QtCore.QCoreApplication.setOrganizationDomain( Application.sDomain )

# Default values
Default			= QtCore.QObject()
Default.Server		= ""
Default.Login		= ""
Default.Password	= ""
Default.Path		= ""

# Settings key names
Key		= QtCore.QObject()
Key.Server	= "server"
Key.Login	= "login"
Key.Password	= "password"
Key.Path	= "path"

# Setting
sSettings		= QtCore.QSettings()
Setting			= QtCore.QObject()
Setting.Server		= None
Setting.Login		 = None
Setting.Password	= None
Setting.Path		= None

class	SettingsDialog(QtGui.QDialog, Ui_Settings.Ui_SettingsDialog):
	def	__init__(self):
		QtGui.QDialog.__init__(self)
		self.setupUi(self)
		self.__setSlots()

	def	__setSlots(self):
		self.connect( self, QtCore.SIGNAL( "accepted()" ), self.slAccept )
		self.connect( self.pbPath, QtCore.SIGNAL( "clicked()" ), self.slPath)

	def	slPath(self):
		print QtCore.QFileInfo(Setting.Path).path()
		filename = QtGui.QFileDialog().getOpenFileName(self,  "Open 1C executable",  QtCore.QFileInfo(Setting.Path).path(),  "Executable files (*.exe)")
		if filename:
			self.lePath.setText(filename)
			Setting.Path = filename
			sSettings.setValue( Key.Path,		QtCore.QVariant(Setting.Path))

	def slLoad(self) :
		'''
		Load settings from config file or set default values.
		'''
		Setting.Server	= sSettings.value(Key.Server).toString()	if sSettings.contains(Key.Server)		else Default.Server
		Setting.Login	= sSettings.value(Key.Login).toString()	if sSettings.contains(Key.Login)	else Default.Login
		Setting.Password	= sSettings.value(Key.Password).toString()	if sSettings.contains(Key.Password)	else Default.Password
		Setting.Path	= sSettings.value(Key.Path).toString()	if sSettings.contains(Key.Path)	else Default.Path

	def slSave(self) :
		'''
		'''

	def slDialog(self) :
		'''
		Call Options dialog w/ settings.
		'''
		self.leServer.setText(Setting.Server)
		self.leLogin.setText(Setting.Login)
		self.lePassword.setText(Setting.Password)
		self.lePath.setText(Setting.Path)
		self.exec_()
		self.slLoad()

	def slAccept(self) :
		'''
		Accept settings from Options dialog.
		'''
		Setting.Server		= self.leServer.text()
		Setting.Login		= self.leLogin.text()
		Setting.Password	= self.lePassword.text()
		Setting.Path		= self.lePath.text()
		sSettings.setValue( Key.Server,		QtCore.QVariant(Setting.Server))
		sSettings.setValue( Key.Login,		QtCore.QVariant(Setting.Login))
		sSettings.setValue( Key.Password,	QtCore.QVariant(Setting.Password))
		sSettings.setValue( Key.Path,		QtCore.QVariant(Setting.Path))
