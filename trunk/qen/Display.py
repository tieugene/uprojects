"""
QEN:		Qt eGroupWare Notifier
Designed by Eugene A. Pivnev

File:		Display.py
Purpose:	Display handler
"""


### Imports

# QEN 1
import	Import

# Python
try :
	import	sys
except :
	Import.slException( "Python" )

# PyQt4
try :
	from	PyQt4	import QtCore, QtGui
except :
	Import.slException( "PyQt4" )

# QEN 2
import	Main, Network, Settings, Thread
"""
try :
	from	Main_ui			import Ui_Main
	from	Main_rc			import *
	from	Settings_ui		import Ui_Settings
	from	Settings_rc		import *
except :
	Import.slException( Settings.Application.sName )
"""

### Slots

# Display Init
def slInit() :

	# Tree Widget
##	Main.uiMain.aSep1.setSeparator( True )
##	Main.uiMain.aSep2.setSeparator( True )
##	Main.uiMain.aSep3.setSeparator( True )
##	Main.uiMain.aSep1.setText( "" )
##	Main.uiMain.aSep2.setText( "" )
##	Main.uiMain.aSep3.setText( "" )

##	Main.uiMain.lwTasks.header().setResizeMode( 0, QtGui.QHeaderView.ResizeToContents )
##	Main.uiMain.lwTasks.addAction( Main.uiMain.aPeerBrowse )
##	Main.uiMain.lwTasks.addAction( Main.uiMain.aPeerPing )
##	Main.uiMain.lwTasks.addAction( Main.uiMain.aPeerEvict )
##	Main.uiMain.lwTasks.addAction( Main.uiMain.aPeerCA )
##	Main.uiMain.lwTasks.addAction( Main.uiMain.aSep1 )
##	Main.uiMain.lwTasks.addAction( Main.uiMain.aNetLeave )
##	Main.uiMain.lwTasks.addAction( Main.uiMain.aSep2 )
##	Main.uiMain.lwTasks.addAction( Main.uiMain.aNetConnect )
##	Main.uiMain.lwTasks.addAction( Main.uiMain.aNetDisconnect )
##	Main.uiMain.lwTasks.addAction( Main.uiMain.aSep3 )
##	Main.uiMain.lwTasks.addAction( Main.uiMain.aNetDelete )
	Main.uiMain.lwTasks.addAction( Main.uiMain.aTaskAccept )

	# Main Window
	if not Settings.Setting.Geometry.bPosition :
		Main.mwMain.move( QtGui.QApplication.desktop().screen().rect().bottomRight() - Main.mwMain.rect().center() )

	# System Tray Icon
	if QtGui.QSystemTrayIcon.isSystemTrayAvailable() :

		# Context menu
		Main.stiMain.setContextMenu( Main.uiMain.mStatus )

		# Icon
		iIcon = QtGui.QIcon( Settings.Icon.Location.sApps + "infolog.png" )	# Settings.Application.sName
		Main.stiMain.setIcon( iIcon )

		# Tooltip
		Main.stiMain.setToolTip( Settings.Application.sName + " (Offline)" )

		if not Settings.Init.bInvisible :
			Main.stiMain.show()

	# Show main dialog?
	if not Settings.Init.bHide and not Settings.Init.bInvisible :
		Main.mwMain.show()


# Show GUI?
def slMainWindow( arEvent ) :

	# Show or hide the main window
	if arEvent == QtGui.QSystemTrayIcon.Trigger :
		Main.mwMain.setVisible( not Main.mwMain.isVisible() )


# Update GUI
def slUpdateGUI() :

	# Messages
	Main.uiMain.sbMain.clearMessage()

	# Buttons
	Main.uiMain.pbOnline.setEnabled( Settings.Status.bConnected )
	Main.uiMain.pbOnline.setChecked( Settings.Status.bConnected )

	# Actions
	Main.uiMain.aStaConnect.setEnabled( not Settings.Status.bConnected )
	Main.uiMain.aStaDisconnect.setEnabled( Settings.Status.bConnected )

	# Tab widget
	Main.uiMain.lwTasks.setEnabled( Settings.Status.bConnected )
	#Main.uiMain.lwTasks.setAlternatingRowColors( Settings.Setting.Appearance.bARC )

	# Menus
	#Main.uiMain.mNetwork.setEnabled( Settings.Status.bConnected )

	# Online
	if Settings.Status.bConnected :

		Main.uiMain.pbOnline.setText( "Online" )
		Main.uiMain.pbOnline.setIcon( QtGui.QIcon( Settings.Icon.Location.sActions + Settings.Icon.Action.sOnline ) )
		#Main.mwMain.setWindowTitle( Settings.Application.sName + " (Online)" )
		Main.stiMain.setToolTip( Settings.Application.sName + " (Online)" )

		# Update Timer
		#Main.tmUpdate.start( 1000 )

	# Offline
	else :

		Main.uiMain.pbOnline.setText( "Offline" )
		Main.uiMain.pbOnline.setIcon( QtGui.QIcon( Settings.Icon.Location.sActions + Settings.Icon.Action.sOffline ) )
		#Main.mwMain.setWindowTitle( Settings.Application.sName + " (Offline)" )
		Main.stiMain.setToolTip( Settings.Application.sName + " (Offline)" )

		# Update Timer
		#Main.tmUpdate.stop()


# Update List
def slUpdateList( sList ) :

	Main.uiMain.lwTasks.clear()

	for task in Settings.Status.lFreshData :
		lwiTask	= QtGui.QListWidgetItem()
		sName	= QtCore.QString(task[1])
		sTip		= QtCore.QString(task[2])
		lwiTask.setText( sName )
		lwiTask.setToolTip( sTip )
		Main.uiMain.lwTasks.addItem( lwiTask )
#		lwiTask.setIcon( 0 , iIcon )

	# Sort
	#Main.uiMain.lwTasks.sortItems( 0 , QtCore.Qt.AscendingOrder )

	# Statusbar
	#Main.uiMain.sbMain.clearMessage()


# Error Message
def slErrorMessage( sError ) :

	# Is main window visible?
	if Main.mwMain.isVisible() and sError != "" :
		QtGui.QErrorMessage.showMessage( QtGui.QErrorMessage.qtHandler() , sError )
