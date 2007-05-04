"""
QEN:		Qt eGroupWare Notifier
Designed by Eugene A. Pivnev

File:		Settings.py
Purpose:	Settings handler
"""


### Imports

# QEN 1
import	Import

# Python
try :
	import	commands, os, platform, sys
except :
	Import.slException( "Python" )

# PyQt4
try :
	from	PyQt4	import QtCore
except :
	Import.slException( "PyQt4" )

# QEN 2
import	Help, Main, Network


### Variables

# Application
Application			= QtCore.QObject()
Application.sName		= "QEN"
Application.sVersion	= "0.1"
Application.sDomain	= "qen.sourceforge.net"
QtCore.QCoreApplication.setApplicationName( Application.sName )

# Author
Author				= QtCore.QObject()
Author.sName			= "Eugene A. Pivnev"
Author.Email			= QtCore.QObject()
Author.Email.sUser	= "ti.eugene"
Author.Email.sDomain	= "@Gmail.com"
QtCore.QCoreApplication.setOrganizationName( Author.sName )
QtCore.QCoreApplication.setOrganizationDomain( Application.sDomain )

# Operating system
sOS				= platform.system()

# Path
Path				= QtCore.QObject()
Path.sKDE		= os.getenv( 'KDEDIR' )
Path.sUser		= os.getenv( 'HOME' )
Path.sQEN		= ""
Path.sSep		= QtCore.QString( QtCore.QDir.separator() )

# Init
Init				= QtCore.QObject()
Init.bHide		= False
Init.bConnect		= True
Init.bDemo		= False
Init.bVerbose		= False
Init.bInvisible	= False

# Status
Status				= QtCore.QObject()
Status.bLaunched		= False
Status.bConnected		= False
Status.oSession		= None
Status.lFreshData		= []		# hot data

# Timer
Timer					= QtCore.QObject()
Timer.Update				= QtCore.QObject()
Timer.Update.iFreq		= 60000
Timer.Update.iPause		= 2000
Timer.Control				= QtCore.QObject()
Timer.Control.iRestart		= 5000
Timer.Control.iLaunched	= 5000
Timer.Process				= QtCore.QObject()
Timer.Process.iPause		= 500
Timer.Process.iWaitMax		= 50

# Display
Display							= QtCore.QObject()
Display.bHideOfflinePeers			= True
Display.bAlternatingRowColours		= True

# Commands
Command					= QtCore.QObject()

# Icons
Icon						= QtCore.QObject()
Icon.Location				= QtCore.QObject()
Icon.Location.sApps		= ":/apps/Images/apps/"
Icon.Location.sActions		= ":/actions/Images/actions/"
Icon.Action				= QtCore.QObject()
Icon.Action.sOnline		= "led-green"
Icon.Action.sOffline		= "led-red"
##Icon.Tree				= QtCore.QObject()
##Icon.Tree.sOnline			= "pill-seagreen"
##Icon.Tree.sDodgy			= "pill-yellow"
##Icon.Tree.sOffline		= "pill-purple"

# File
##File						= QtCore.QObject()
##File.sDemoList			= "../Testing/DemoList.txt"

# Message
Message					= QtCore.QObject()
Message.sStarting			= "Starting ..."
Message.sStopping			= "Stopping ..."
Message.sConnecting		= "Connecting ..."
Message.sDisconnecting		= "Disconnecting ..."
Message.sUpdating			= "Updating ..."
Message.sTaskAccepting		= "Task accepting ..."

# Input
Input					= QtCore.QObject()
Input.iNumArgs			= len(sys.argv)
##Input.Network				= QtCore.QObject()
##Input.Network.sName		= QtCore.QString()
##Input.Network.sPassword	= QtCore.QString()
Input.Task				= QtCore.QObject()
Input.Task.sID			= QtCore.QString()

# Setting
sSettings				= QtCore.QSettings()
Setting					= QtCore.QObject()
Setting.Geometry			= QtCore.QObject()
Setting.Geometry.bPosition	= False
Setting.Appearance		= QtCore.QObject()
Setting.Appearance.bARC	= False
Setting.Connection		= QtCore.QObject()
Setting.Connection.Server	= QtCore.QUrl( "http://localhost/egroupware/" );
Setting.Connection.Login	= "user"
Setting.Connection.Password	= "password"
Setting.RefreshTime		= 300
Setting.DBPath			= "~/.qen/"


# Linux
if sOS == "Linux" :

	if not Path.sKDE :
		Path.sKDE	= '/usr/'

	if not Path.sUser :
		Path.sUser	= '/home/' + os.getenv( 'USER' ) + '/'

	# Installation
	if QtCore.QFile.exists( Path.sKDE + "/share/apps/qen/Source/" ) :
		Path.sQEN	= Path.sKDE + "/share/apps/qen/"
	elif QtCore.QFile.exists( Path.sUser + "/.kde/share/apps/qen/Source/" ) :
		Path.sQEN	= Path.sUser + "/.kde/share/apps/qen/"
	else :
		Path.sQEN	= os.getcwd() + "/../"

	# Commands
	#Command.sSU				= "sudo"
	Command.sSU				= "kdesu"
	Command.sHamachiInit	= "hamachi-init"
	Command.sHamachi		= "hamachi"
	Command.sKonsole		= "konsole"
	Command.sPing			= "ping"

	# TunCfg existence
##	if QtCore.QFile.exists( Command.sTunCfg ) :
##		Status.bCanLaunch	= True
##	else :
##		Status.bCanLaunch	= False

	Init.bHide		= True

	"""
	# Windows
	elif sOS == "Windows" :

		if not sHomeKDE :
			sHomeKDE	= ''

		if not sHomeUser :
			sHomeUser	= ''

		sReg		= QtCore.QSettings( "HKEY_LOCAL_MACHINE\\Software\\Archiving\\QEN" , QtCore.QSettings.NativeFormat )
		sHomeQEN	= sReg.value( "Path" ).toString()

		# Installation
		sInstQEN	= sHomeQEN

		# Commands
		sCmdSudo		= QtCore.QString( "sudo" )
		sCmdTunCfg		= QtCore.QString( "tuncfg" )
		sReg			= QtCore.QSettings( "HKEY_LOCAL_MACHINE\\Software\\Hamachi" , QtCore.QSettings.NativeFormat )
		sCmdHamachi		= sReg.value( "Path" ).toString() + "/Hamachi.exe"
	"""

# Others
else :

	print ""
	print "Unfortunately, your OS is not supported by " + Application.sName + " " + Application.sVersion + ".  Please email the author, specifying your system details."
	print ""

	sys.exit()


### Slots

# Load
def slLoad() :

	#print "slLoad"

	# Window
	sSettings.beginGroup( "Geometry" )
	#Main.mwMain.resize( sSettings.value( "Size" ).toSize() )
	if sSettings.contains( "Position" ) :
		Setting.Geometry.bPosition = True
		Main.mwMain.move( sSettings.value( "Position" ).toPoint() )
	sSettings.endGroup()

	# Appearance
	sSettings.beginGroup( Main.uiSettings.gbAppearance.title() )
	Setting.Appearance.bARC = sSettings.value( Main.uiSettings.cbARC.text() ).toBool()
	sSettings.endGroup()

	if Setting.Appearance.bARC == False :
		Main.uiSettings.cbARC.setCheckState( QtCore.Qt.Unchecked )
	else :
		Main.uiSettings.cbARC.setCheckState( QtCore.Qt.Checked )


# Save
def slSave() :

	#print "slSave"

	# Window
	sSettings.beginGroup( "Geometry" )
	#sSettings.setValue( "Size" , QtCore.QVariant(Main.mwMain.size()) )
	sSettings.setValue( "Position" , QtCore.QVariant(Main.mwMain.pos()) )
	#sSettings.remove( "Position" )
	sSettings.endGroup()


# Accept
def slAccept() :

	# Convert
	if Main.uiSettings.cbARC.checkState() == QtCore.Qt.Unchecked :
		Setting.Appearance.bARC = False
	else :
		Setting.Appearance.bARC = True

	#print "slSettingsA: " + str( Setting.Appearance.bARC )

	# Save
	# Appearance
	sSettings.beginGroup( Main.uiSettings.gbAppearance.title() )
	sSettings.setValue( Main.uiSettings.cbARC.text() , QtCore.QVariant(Setting.Appearance.bARC) )
	sSettings.endGroup()

	# Update GUI
	#Display.slUpdateGUI()
	Network.slUpdateList()


# Dialog
def slDialog() :

	# Modal
	Main.dSettings.exec_()

	# Load
	slLoad()


# Offline Peers
def slHideOfflinePeers() :

	#print "slHideOfflinePeers"

	# Offline Peers
	Network.slHideOfflinePeers()
