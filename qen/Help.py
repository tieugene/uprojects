"""
QEN:		Qt eGroupWare Notifier
Designed by Eugene A. Pivnev

File:	Help.py
Purpose:	Help menu handler
"""


### Imports

# QEN 1
import	Import

# PyQt4
try :
	from	PyQt4	import QtCore, QtGui
except :
	Import.slException( "PyQt4" )

# QEN 2
import	Main, Settings


### Slots

# About Qt4
def slAboutQt4() :
	QtGui.QApplication.aboutQt()


# About QEN
def slAboutQEN() :
	QtGui.QMessageBox.about( Main.uiMain.cwMain, "About " + Settings.Application.sName,
		"<b>" + Settings.Application.sName + "</b> " + Settings.Application.sVersion +
		"<br>Designed by " + Settings.Author.sName + "<br>"
		"<br>" + Settings.Application.sName + " is a eGroupWare's InfoLog Notifier.<br>" )


# Open URL
def slUOpen( uURL ) :

	Main.uiMain.sbMain.showMessage( "Launching external application ..." )

	QtGui.QDesktopServices.openUrl( uURL )


# URL: QEN
def slUQEN() :

	# Set URL
	uURL = QtCore.QUrl( "http://uprojects.googlecode.com/svn/trunk/qen" )

	slUOpen( uURL )


# URL: Qt4
def slUQt4() :

	# Set URL
	uURL = QtCore.QUrl( "http://www.trolltech.com/products/qt" )

	slUOpen( uURL )

# URL: PyQt4
def slUPyQt4() :

	# Set URL
	uURL = QtCore.QUrl( "http://www.riverbankcomputing.co.uk/pyqt/" )

	slUOpen( uURL )

# URL: Python
def slUPython() :

	# Set URL
	uURL = QtCore.QUrl( "http://www.python.org/" )

	slUOpen( uURL )


# Doc: Authors
def slDocAuthors() :

	# Set URL
	uURL = QtCore.QUrl( "file:" + Settings.Path.sQEN + Settings.Path.sSep + "Doc" + Settings.Path.sSep + "AUTHORS.txt" )

	slUOpen( uURL )

# Doc: Changes
def slDocChanges() :

	# Set URL
	uURL = QtCore.QUrl( "file:" + Settings.Path.sQEN + Settings.Path.sSep + "Doc" + Settings.Path.sSep + "ChangeLog.txt" )

	slUOpen( uURL )

# Doc: Copying
def slDocCopying() :

	# Set URL
	uURL = QtCore.QUrl( "file:" + Settings.Path.sQEN + Settings.Path.sSep + "Doc" + Settings.Path.sSep + "COPYING.txt" )

	slUOpen( uURL )

# Doc: Install
def slDocInstall() :

	# Set URL
	uURL = QtCore.QUrl( "file:" + Settings.Path.sQEN + Settings.Path.sSep + "Doc" + Settings.Path.sSep + "INSTALL.txt" )

	slUOpen( uURL )

# Doc: Issues
def slDocIssues() :

	# Set URL
	uURL = QtCore.QUrl( "file:" + Settings.Path.sQEN + Settings.Path.sSep + "Doc" + Settings.Path.sSep + "ISSUES.txt" )

	slUOpen( uURL )

# Doc: Licence
def slDocLicence() :

	# Set URL
	uURL = QtCore.QUrl( "file:" + Settings.Path.sQEN + Settings.Path.sSep + "Doc" + Settings.Path.sSep + "LICENCE.txt" )

	slUOpen( uURL )

# Doc: News
def slDocNews() :

	# Set URL
	uURL = QtCore.QUrl( "file:" + Settings.Path.sQEN + Settings.Path.sSep + "Doc" + Settings.Path.sSep + "NEWS.txt" )

	slUOpen( uURL )

# Doc: Introduction
def slDocIntroduction() :

	# Set URL
	uURL = QtCore.QUrl( "file:" + Settings.Path.sQEN + Settings.Path.sSep + "Doc" + Settings.Path.sSep + "README.txt" )

	slUOpen( uURL )

# Doc: Requests
def slDocRequests() :

	# Set URL
	uURL = QtCore.QUrl( "file:" + Settings.Path.sQEN + Settings.Path.sSep + "Doc" + Settings.Path.sSep + "TODO.txt" )

	slUOpen( uURL )

# Doc: Requests
def slGoTask() :
	id = Settings.Input.Task.sID = Main.uiMain.twTasks.item(Main.uiMain.twTasks.currentRow(), 0).text()	#.toInt()[0]
	uURL = QtCore.QUrl(Settings.Setting.Connection.Server + "index.php?menuaction=infolog.uiinfolog.edit&info_id=" + id)
	slUOpen( uURL )
