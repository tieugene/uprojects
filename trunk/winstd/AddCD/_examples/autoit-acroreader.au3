#cs
----------------------
����������: Acrobat Reader
�� �����(��) ������(��) �������������: 6.0 Pro

����� �������: DenchikK (http://forum.oszone.net/member.php?u=29156)
----------------------
#ce

If WinExists(@ScriptName) Then Exit
AutoItWinSetTitle(@ScriptName)
AutoItSetOption("TrayIconDebug", 1)
AutoItSetOption("SendKeyDelay", 60)
AutoItSetOption("MouseCoordMode", 0)

If FileExists ( @ProgramFilesDir & "\Adobe\Acrobat 6.0\Acrobat\Acrobat.exe" ) Then
	MsgBox (64,'����������','��������� Acrobat ��� ����� �� ����� ����������. ������� � � ���������� �����.',7)
      Exit
EndIf

Global $Serial

Run (@ScriptDir & '\keygen.exe')

WinWaitActive ('Keygen for Adobe Acrobat')
$Serial = ControlGetText ( "Keygen for Adobe Acrobat", "", "Edit2" )
ControlClick ('Keygen for Adobe Acrobat','','Button2')

ProcessWaitClose("keygen.exe", 10)

Run (@ScriptDir & '\setup.exe')

WinWaitActive ('Adobe Acrobat 6.0 Professional -  Wizard')
ControlClick ('Adobe Acrobat 6.0 Professional -  Wizard','','&Next >')

WinWaitActive ('Adobe Acrobat 6.0 Professional - Setup','WARNING: This program is protected by copyright law and international treaties.')
ControlClick ('Adobe Acrobat 6.0 Professional - Setup','WARNING: This program is protected by copyright law and international treaties.','&Next >')

WinWaitActive ('Adobe Acrobat 6.0 Professional - Setup','Select EULA Language')
ControlClick ('Adobe Acrobat 6.0 Professional - Setup','Select EULA Language','&Next >')

WinWaitActive ('Adobe Acrobat 6.0 Professional - Setup','End User License Agreement')
ControlClick ('Adobe Acrobat 6.0 Professional - Setup','End User License Agreement','&Accept >')

; �� ������� �� ��������������
WinWaitActive ('Adobe Acrobat 6.0 Professional - Setup','Customer Information')
Send('{Tab 2}')
Send ($Serial)
ControlClick ('Adobe Acrobat 6.0 Professional - Setup','Customer Information','&Next >')

WinWaitActive ('Adobe Acrobat 6.0 Professional - Setup','Setup Type')
ControlClick ('Adobe Acrobat 6.0 Professional - Setup','Setup Type','&Next >')

WinWaitActive ('Adobe Acrobat 6.0 Professional - Setup','Destination Folder')
ControlClick ('Adobe Acrobat 6.0 Professional - Setup','Destination Folder','&Next >')

WinWaitActive ('Adobe Acrobat 6.0 Professional - Setup','Ready to Install the Program')
ControlClick ('Adobe Acrobat 6.0 Professional - Setup','Ready to Install the Program','&Update')

WinWaitActive ('Adobe Acrobat 6.0 Professional - Setup','Setup Completed')
ControlClick ('Adobe Acrobat 6.0 Professional - Setup','Setup Completed','&Finish')

ProcessWaitClose("setup.exe", 10)

Run (@ScriptDir & '\update.exe')

WinWaitActive ('���������� Adobe Acrobat 6.0: ������� ���������')
ControlClick ('���������� Adobe Acrobat 6.0: ������� ���������','','����������')

WinWaitActive ('���������� Adobe Acrobat 6.0: ������')
ControlClick ('���������� Adobe Acrobat 6.0: ������','','�������')

ProcessWaitClose("update.exe", 10)

Run (@ScriptDir & '\rusfonts.exe')

WinWaitActive ('��������� ���������� ������� ��������')
ControlClick ('��������� ���������� ������� ��������','','��')

WinWaitActive ('��������� ���������� ������� ��������')
ControlClick ('��������� ���������� ������� ��������','','��')

Exit
