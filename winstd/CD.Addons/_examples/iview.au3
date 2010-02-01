#cs
----------------------
Приложение: IrfanView
Версия: 4.25
Автор: TI_Eugene
----------------------
#ce

Run ('\bin\iview425_setup.exe')

WinWaitActive ('IrfanView Setup', 'Welcome')
ControlClick ('IrfanView Setup','','Button2')
ControlClick ('IrfanView Setup','','Button3')
ControlClick ('IrfanView Setup','','Button6')
ControlClick ('IrfanView Setup','','Button11')

WinWaitActive ('IrfanView Setup', "What's new")
ControlClick ('IrfanView Setup','','Button11')

WinWaitActive ('IrfanView Setup', 'Do you want to associate')
ControlClick ('IrfanView Setup','','Button1')
ControlClick ('IrfanView Setup','','Button5')
ControlClick ('IrfanView Setup','','Button16')

WinWaitActive ('IrfanView Setup', 'Google Toolbar')
ControlClick ('IrfanView Setup','','Button1')
ControlClick ('IrfanView Setup','','Button17')

WinWaitActive ('IrfanView Setup', 'Ready to install')
ControlClick ('IrfanView Setup','','Button2')
ControlClick ('IrfanView Setup','','Button22')

WinWaitActive ('IrfanView Setup', 'You want to change')
ControlClick ('IrfanView Setup','','Button1')

WinWaitActive ('IrfanView Setup', 'Installation successfull')
ControlClick ('IrfanView Setup','','Button2')
ControlClick ('IrfanView Setup','','Button26')

Run (@ScriptDir & '\irfanview_lang_russian.exe')

WinWaitActive ('IrfanView Language Installer', 'Welcome to')
ControlClick ('IrfanView Language Installer','','Button1')

WinWaitActive ('IrfanView Language Installer', 'Installation successfull')
ControlClick ('IrfanView Language Installer','','Button1')
