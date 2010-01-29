#cs
----------------------
����������: Remote Administrator
�� �����(��) ������(��) �������������: 2.2 (ru/en)

���� ������ �������� ��� � �������, ��� � � ���������� ������� RAdmin-�.

����� �������: Sanja Alone (http://forum.oszone.net/member.php?userid=28800)
----------------------
#ce
;�������������� ����������� �������������� ������� �������
If WinExists(@ScriptName) Then Exit
AutoItWinSetTitle(@ScriptName)
;������ � ��������� ������ ��������� AutoIt
;AutoItSetOption("TrayIconHide", 1)
;���������� ������� ������ �������� � ������� ���������� ��������� ������ � ������ �������.
AutoItSetOption("TrayIconDebug", 1)
AutoItSetOption("SendKeyDelay", 15)
If ProcessExists ( "ps.exe" )<>0 Then
     ProcessClose ( "ps.exe" )
     ProcessWaitClose ( "ps.exe" )
EndIf
;������ ����������� ��� ����������� � ������ Punto Switcher-� - �� ����� �������� ���������
;��������� ���� � �����
;If @OSType="WIN32_NT" Then BlockInput ( 1 )
#cs
----------------------
���������� ����������
----------------------

$Title - ��������� ���� ����������� ('Remote Administrator' � ����� ������)
$file - ������������ ����
$InstPath - � ����� ������� ���������� ���������
$programgroup - � ����� ����������� ������ �������� ������ ���������
$password - ������ ��� ��������� �������� RAdmin-� (�� ��. - mypassword; ������ ������ ����� ���-�� NT security - ����� ������� $password='' )

$serial - �������� � ������������ ���� (���� ������� �������� � ��������) ��� �������� ��������� "Data" 
����� "HKEY_LOCAL_MACHINE\SOFTWARE\RAdmin\v1.01\ViewType". ������� ���� ���� �������� ������� ��������� 
� ������� AutoIt-� (�.�. �� ����� �������, ��� � reg-�����, � ����� �������). ���� ��������� ��������� - 
������ �������� Autoit.chm (������� � ������� RegWrite). ���� ��� ����� �� ������� - �������������� ���� 
����������� ConvRegToAu3 (http://sanjaalone.h15.ru/crta.php). ���������, ���� ����-�� ������ ������ 
�����������, �� ��� ���������... ��� ������ - �������������� �����-�� �������� ��������.

���� ������������ ������������ �� ���� ��������� ������ ����� ������������� ����� ('ru' - ���., 'en' - ����.)

----------------------
#ce
Global $Title='Remote Administrator', $file='radmin22ru.exe', $InstPath=@ProgramFilesDir & '\Radmin', $programgroup='����\Remote Administrator', $password='mypassword', $serial=''

;����������� ����� ������������
$lang=StringLower ( StringLeft ( StringRight ( $file, 6 ), 2 ) )

Run ( @ScriptDir&'\'&$file )

If $lang='ru' Then
	WinWait ( $Title, '����� ����������' )
	WinActivate ( $Title, '����� ����������' )
	WinWaitActive ( $Title, '����� ����������' )
	Send ( '{ENTER}' )
	WinWaitActive ( $Title, '� �������� ��� ����������' )
	;������� ����� "� �������� ��� ����������"
	ControlClick ( $Title, '� �������� ��� ����������', 'Button1' )
	Send ( '{ENTER}' )
	WinWaitActive ( $Title, '��������!' )
	Send ( '{ENTER}' )
	WinWaitActive ( $Title, '�������� ���������' )
	Send ( '{ENTER}' )
	WinWaitActive ( $Title, '���������� ���������' )
	;�� ��. C:\Program Files\Radmin
	If $InstPath<>@ProgramFilesDir & '\Radmin' Then ControlSetText ( $Title, '���������� ���������', 'Edit1', $InstPath )
	Send ( '{ENTER}' )
	WinWait ( $Title, 'FolderView' )
	WinClose ( $Title, 'FolderView' )
	WinWait ( '�����������', '������' )
	WinActivate ( '�����������', '������' )
	WinWaitActive ( '�����������', '������' )
	;�������� �� ������ �������������
	If ControlCommand ( '�����������', '������', 'Button4', 'IsEnabled', '' )=1 Then ControlClick ( '�����������', '������', 'Button3' )
	;����� �������� 2 ��������
	If $password<>'' Then
		;������ ������
		ControlSetText ( '�����������', '������', "Edit1", $password )
		ControlSetText ( '�����������', '������', "Edit2", $password )
	Else
		;�������� NT security [��������� ����� ������������� ����� ����� ������� ����� ���������, �������� "��������� Remote Administrator server" (r_server.exe /setup) -> "�����������..." -> "�����"]
		ControlClick ( '�����������', '������', 'Button3' )
	EndIf
	Send ( '{ENTER}' )
	WinWaitActive ( '�������������' )
	ControlClick ( '�������������', '', 'Button2' )
Else
	WinWait ( $Title, 'Welcome' )
	WinActivate ( $Title, 'Welcome' )
	WinWaitActive ( $Title, 'Welcome' )
	Send ( '{ENTER}' )
	WinWaitActive ( $Title, 'To proceed with the installation' )
	;������� ����� "� �������� ��� ����������"
	ControlClick ( $Title, 'To proceed with the installation', 'Button1' )
	Send ( '{ENTER}' )
	WinWaitActive ( $Title, 'Important notes' )
	Send ( '{ENTER}' )
	WinWaitActive ( $Title, 'Installation options' )
	Send ( '{ENTER}' )
	WinWaitActive ( $Title, 'Destination Directory' )
	;�� ��. C:\Program Files\Radmin
	If $InstPath<>@ProgramFilesDir & '\Radmin' Then ControlSetText ( $Title, 'Destination Directory', 'Edit1', $InstPath )
	Send ( '{ENTER}' )
	WinWait ( $Title, 'FolderView' )
	WinClose ( $Title, 'FolderView' )
	WinWait ( 'Password', 'Password' )
	WinActivate ( 'Password', 'Password' )
	WinWaitActive ( 'Password', 'Password' )
	;�������� �� ������ �������������
	If ControlCommand ( 'Password', 'Password', 'Button4', 'IsEnabled', '' )=1 Then ControlClick ( 'Password', 'Password', 'Button3' )
	;����� �������� 2 ��������
	If $password<>'' Then
		;������ ������
		ControlSetText ( 'Password', 'Password', "Edit1", $password )
		ControlSetText ( 'Password', 'Password', "Edit2", $password )
	Else
		;�������� NT security [��������� ����� ������������� ����� ����� ������� ����� ���������, �������� "Settings for Remote Administrator server" (r_server.exe /setup) -> "Set password..." -> "Permissions"]
		ControlClick ( 'Password', 'Password', 'Button3' )
	EndIf
	Send ( '{ENTER}' )
	WinWaitActive ( 'Confirmation' )
	ControlClick ( 'Confirmation', '', 'Button2' )
EndIf

;��������� ������� ���� ������� ������ Remote Administrator Service (�� ��. "����")
RegWrite('HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\r_server','Start',"REG_DWORD",0x00000003)

;������� �������
If StringLower($programgroup)<>'remote administrator v2.2' Then
DirCopy ( @ProgramsCommonDir & '\Remote Administrator v2.2', @ProgramsCommonDir & '\' & $programgroup, 1 )
DirRemove ( @ProgramsCommonDir & '\Remote Administrator v2.2', 1 )
EndIf

;�� ���������� �������� ��� ������ ���������
RegWrite("HKEY_CURRENT_USER\Software\RAdmin\v2.0\Parameters","showbw","REG_BINARY","00000000")

; ����������� (������������ ������ � ��. ���������� ������� � �������)
If Not StringIsXDigit ( RegRead("HKEY_LOCAL_MACHINE\SOFTWARE\RAdmin\v1.01\ViewType","Data") ) Then
	If StringIsXDigit ( $serial ) Then
	RegWrite("HKEY_LOCAL_MACHINE\SOFTWARE\RAdmin\v1.01\ViewType","Data","REG_BINARY",$serial)
	ElseIf $serial<>'' Then
		Run ( $InstPath & '\radmin.exe' )
		If $lang='ru' Then
			$win1text='������� ���'
			$win2titl='�����������'
		Else
			$win1text='Enter code'
			$win2titl='Enter License'
		EndIf
		WinWait ( '', $win1text )
		ControlClick ( '' ,$win1text, 'Button2' )
		WinWait ( $win2titl )
		ControlSetText ( $win2titl, '', 'Edit1', $serial )
		ControlClick ( $win2titl, '', 'Button1' )
		WinWaitClose ( $win2titl )
		ControlClick ( '' ,$win1text, 'Button1' )
		ProcessClose ( 'radmin.exe' )
		ProcessWaitClose ( 'radmin.exe' )
	EndIf
EndIf

;��������� ������ � ����
RegWrite('HKEY_LOCAL_MACHINE\System\RAdmin\v2.0\Server\Parameters','DisableTrayIcon',"REG_BINARY","01000000")

;������� ���� ������ � ���. �����: ��������� OLD � IP=192.168.0.3
RegWrite("HKEY_CURRENT_USER\Software\RAdmin\v2.0\Clients","2","REG_BINARY","e09304000c0c005000000500000064000000000000000100000000000000010000000100000001000000010000000100000001000000000000000000000000000000000000003139322e3136382e302e3300c8a1a400e2f4d3775100010100f0fd7f00000000f8fbfd7f000000002cc00000acc81200a4bad3772cc000002cc00000c0c8120046bad377a89a53002cc0000000000000d8c812005500d577a89a53002cc00000000000004f4c44000000000003000400c8a1a400e2f4d3775100010100f0fd7f00000000f8fbfd7f000000002cc00000acc81200a4bad3772cc000002cc00000c0c8120046bad377a89a53002cc0000000000000d8c812005500d577a89a53002cc00000000000000000000000000000000023130000000000000200000000000000")

;BlockInput ( 0 )
