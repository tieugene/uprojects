#cs
----------------------
Приложение: Avira
Версия: 9.0.0.10
Автор: TI_Eugene
----------------------
#ce

Run ('\bin\The_KMPlayer_1435.exe')

WinWaitActive ('Installer Language')
ControlClick ('Installer Language','','Button1')

WinWaitActive ('The KMPlayer 2.9.4.1435 Setup', 'Welcome to the The KMPlayer Setup Wizard')
ControlClick ('The KMPlayer 2.9.4.1435 Setup','','Button2')

WinWaitActive ('The KMPlayer 2.9.4.1435 Setup', 'License Agreement')
ControlClick ('The KMPlayer 2.9.4.1435 Setup','','Button2')

WinWaitActive ('The KMPlayer 2.9.4.1435 Setup', 'Choose Components')
ControlClick ('The KMPlayer 2.9.4.1435 Setup','','Button2')

WinWaitActive ('The KMPlayer 2.9.4.1435 Setup', 'Choose Install Location')
ControlClick ('The KMPlayer 2.9.4.1435 Setup','','Button2')

WinWait ('The KMPlayer 2.9.4.1435 Setup', 'Please wait while The KMPlayer is being installed.')

WinWaitActive ('The KMPlayer 2.9.4.1435 Setup', 'Install the PandoraTV Ask Toolbar')
ControlClick ('The KMPlayer 2.9.4.1435 Setup','','Button5')
ControlClick ('The KMPlayer 2.9.4.1435 Setup','','Button2')

WinWaitActive ('The KMPlayer 2.9.4.1435 Setup', 'Completing the The KMPlayer Setup Wizard')
ControlClick ('The KMPlayer 2.9.4.1435 Setup','','Button4')
ControlClick ('The KMPlayer 2.9.4.1435 Setup','','Button2')
