#cs
----------------------
Приложение: VNC
Версия: 4.1.3
Автор: TI_Eugene
----------------------
#ce

Run ('C:\Program Files\RealVNC\VNC4\vncconfig.exe')

WinWaitActive ('VNC Server Properties (User-Mode)')
ControlClick ('VNC Server Properties (User-Mode)','','Button3')

WinWaitActive ('VNC Server Password')
ControlSetText ('VNC Server Password','','Edit1', 'tratata')
ControlSetText ('VNC Server Password','','Edit2', 'tratata')
ControlClick ('VNC Server Password','','Button1')

WinWaitActive ('VNC Server Properties (User-Mode)')
ControlClick ('VNC Server Properties (User-Mode)','','Button9')
