#cs
----------------------
Приложение: VNC
Версия: 4.1.3
Автор: TI_Eugene
----------------------
#ce

Run (@ScriptDir & '\vnc-4_1_3-x86_win32.exe')

WinWaitActive ('Setup - VNC')
ControlClick ('Setup - VNC','','TNewButton1')

WinWaitActive ('Setup - VNC', 'License Agreement')
ControlClick ('Setup - VNC','','TNewRadioButton1')
ControlClick ('Setup - VNC','','TNewButton2')

Select Destination Location
WinWaitActive ('Setup - VNC', 'Select Destination Location')
ControlClick ('Setup - VNC','','TNewButton1')