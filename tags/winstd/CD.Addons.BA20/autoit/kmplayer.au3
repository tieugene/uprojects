#cs
----------------------
Приложение: KMplayer
Версия: 3.0.0.1439
Автор: TI_Eugene
----------------------
#ce

Run ('\bin\kmp.3.0.0.1439.exe')

WinWaitActive ('Installer Language')
ControlClick ('Installer Language','','Button1')

WinWaitActive ('The KMPlayer Setup', 'Welcome to the The KMPlayer Setup Wizard')
ControlClick ('The KMPlayer Setup','','Button2')

WinWaitActive ('The KMPlayer Setup', 'License Agreement')
ControlClick ('The KMPlayer Setup','','Button2')

WinWaitActive ('The KMPlayer Setup', 'Choose Components')
ControlClick ('The KMPlayer Setup','','Button2')

WinWaitActive ('The KMPlayer Setup', 'Choose Install Location')
ControlClick ('The KMPlayer Setup','','Button2')

WinWait ('The KMPlayer 3.0.0.1438 Setup', 'Please wait while The KMPlayer is being installed.')

WinWaitActive ('The KMPlayer Setup', 'Install the PandoraTV Ask Toolbar')
ControlClick ('The KMPlayer Setup','','Button5')
ControlClick ('The KMPlayer Setup','','Button2')

WinWaitActive ('The KMPlayer Setup', 'Completing the The KMPlayer Setup Wizard')
ControlClick ('The KMPlayer Setup','','Button4')
ControlClick ('The KMPlayer Setup','','Button2')
