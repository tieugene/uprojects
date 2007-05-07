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
##Input.Network			= QtCore.QObject()
##Input.Network.sName		= QtCore.QString()
##Input.Network.sPassword	= QtCore.QString()
Input.Task				= QtCore.QObject()
Input.Task.sID			= QtCore.QString()

# Default values
Default					= QtCore.QObject()
Default.Server			= "http://server/egroupware/"
Default.Login				= "user"
Default.Password			= "password"
Default.RefreshTime		= None

# Settings key names
Key						= QtCore.QObject()
Key.Server				= "server"
Key.Login				= "login"
Key.Password				= "password"
Key.RefreshTime			= "refresh"

# Setting
sSettings				= QtCore.QSettings()
Setting					= QtCore.QObject()
Setting.Server			= "http://server/egroupware/";
Setting.Login				= "eugene"
Setting.Password			= "S41Plus"
Setting.RefreshTime		= 300


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
		sCmdTunCfg	= QtCore.QString( "tuncfg" )
		sReg			= QtCore.QSettings( "HKEY_LOCAL_MACHINE\\Software\\Hamachi" , QtCore.QSettings.NativeFormat )
		sCmdHamachi	= sReg.value( "Path" ).toString() + "/Hamachi.exe"
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

	if sSettings.contains(Key.Server) :
		Setting.Server = sSettings.value(Key.Server).toString()
	else :
		Setting.Server = Default.Server

	if sSettings.contains(Key.Login) :
		Setting.Login = sSettings.value(Key.Login).toString()
	else :
		Setting.Login = Default.Login

	if sSettings.contains(Key.Password) :
		Setting.Password = sSettings.value(Key.Password).toString()
	else :
		Setting.Password = Default.Password

	print Setting.Server
	print Setting.Login
	print Setting.Password


# Save
def slSave() :
	sSettings.setValue( Key.Server,   QtCore.QVariant(Setting.Server))
	sSettings.setValue( Key.Login,    QtCore.QVariant(Setting.Login))
	sSettings.setValue( Key.Password, QtCore.QVariant(Setting.Password))
	#sSettings.setValue( "refresh",  QtCore.QVariant(Setting.Server))


# Accept
def slAccept() :

	Setting.Server = Main.uiSettings.cbServerURL.text()
	sSettings.setValue( Key.Server , QtCore.QVariant(Setting.Server) )

	Setting.Login = Main.uiSettings.cbLogin.text()
	sSettings.setValue( Key.Login , QtCore.QVariant(Setting.Login) )

	Setting.Password = Main.uiSettings.cbPassword.text()
	sSettings.setValue( Key.Password , QtCore.QVariant(Setting.Password) )

	# Update GUI
	#Display.slUpdateGUI()
	Network.slUpdateList()


# Dialog
def slDialog() :

	# set values
	Main.uiSettings.cbServerURL.setText(Setting.Server)
	Main.uiSettings.cbLogin.setText(Setting.Login)
	Main.uiSettings.cbPassword.setText(Setting.Password)

	# Modal
	Main.dSettings.exec_()

	# Load
	slLoad()


# Offline Peers
def slHideOfflinePeers() :

	#print "slHideOfflinePeers"

	# Offline Peers
	Network.slHideOfflinePeers()
