#cs
----------------------
Приложение: IrfanView
Версия: 4.25
Автор: TI_Eugene
----------------------
#ce

Run (@ScriptDir & '\iview425_setup.exe')

WinWaitActive ('IrfanView Setup')
ControlClick ('IrfanView Setup','','Button2')
ControlClick ('IrfanView Setup','','Button3')
ControlClick ('IrfanView Setup','','Button4')
ControlClick ('IrfanView Setup','','Button11')

WinWaitActive ('IrfanView Setup')
ControlClick ('IrfanView Setup','','Button11')

WinWaitActive ('IrfanView Setup')
ControlClick ('IrfanView Setup','','Button1')
ControlClick ('IrfanView Setup','','Button5')
ControlClick ('IrfanView Setup','','Button16')

WinWaitActive ('IrfanView Setup')
ControlClick ('IrfanView Setup','','Button1')
ControlClick ('IrfanView Setup','','Button17')

WinWaitActive ('IrfanView Setup')
ControlClick ('IrfanView Setup','','Button2')
ControlClick ('IrfanView Setup','','Button22')

WinWaitActive ('IrfanView Setup')
ControlClick ('IrfanView Setup','','Button1')

WinWaitActive ('IrfanView Setup')
ControlClick ('IrfanView Setup','','Button2')
ControlClick ('IrfanView Setup','','Button26')

Run (@ScriptDir & '\irfanview_lang_russian.exe')

WinWaitActive ('IrfanView Language Installer')
ControlClick ('IrfanView Language Installer','','Button1')

WinWaitActive ('IrfanView Language Installer')
ControlClick ('IrfanView Language Installer','','Button1')
