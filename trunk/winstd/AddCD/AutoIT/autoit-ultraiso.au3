#cs
----------------------
����������: UltraISO
�� �����(��) ������(��) �������������: 7.6.1.1125; 7.6.2.1180; 7.6.5.1225; 7.6.5.1269; 8.0.0.1392; 8.1.2.1625; 8.2.0.1669; 8.5.1.1860; 8.6.0.1936; 8.6.1.1985; 8.6.3.2052; 9.1.2.2465; 9.2.0.2536

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
If ProcessExists ( "ps.exe" )<>0 Then
    ProcessClose ( "ps.exe" )
    ProcessWaitClose ( "ps.exe" )
EndIf
;������ ����������� (� ��������� ������ ��������) ��� ����������� � ������ Punto Switcher-� - �� ����� �������� ���������
;��������� ���� � �����
;If @OSType="WIN32_NT" Then BlockInput ( 1 )
#cs
----------------------
���������� ����������
----------------------

$file - ������������ ����
$programgroup - � ����� ����������� ������ �������� ������ ���������

������� ���� ��� � �������� �������������� � ���������� $regname � $serial.

���� � ��� ������ UltraISO < 7.62 �������� �������� ���������� $ver 
�� ���-������ �������� �� 'new'.

��� ���������� �������� ��������� (���������� $serial='') ������������ �������� �� 
������� ���������� ���������, �, � ��. �������������� ���-��, ���� ���������� � 
���������� UltraISO (���������� $crackedexe).

----------------------
#ce
Global $ver='new', $file='uiso9_pe.exe', $regname='', $serial='', $programgroup='CD � DVD �������\UltraISO', $crackedexe='UltraISO.exe'

;������ ��������� � ����� ������
RunWait ( @ScriptDir&'\'&$file & ' /VERYSILENT /SP- /GROUP="' & $programgroup & '"' )
Select
    Case $serial<>''
		;������ ����� ��� ��������� ������� �����������
		Run ( @ProgramFilesDir & '\UltraISO\UltraISO.exe' )
		WinWait ( '����� ����������' )
		WinActivate ( '����� ����������' )
		WinWaitActive ( '����� ����������' )
		ControlClick ( '����� ����������', '', 'TButton4' )
		WinWait ( '�����������' )
		WinActivate ( '�����������' )
		WinWaitActive ( '�����������' )
		;���� ���. ������
		;������� � ������ 7.62 �������� ��� ����������� �������� �������� ������� 
		;(��� ����� ������ ������ ��������� ��� ����������)
		If $ver <> 'new' Then
			$ssplit = StringSplit ( $serial, "-" )
			ControlSetText ( '�����������', '', 'TEdit4', $regname )
			ControlSetText ( '�����������', '', 'TEdit5', $ssplit[1] )
			ControlSetText ( '�����������', '', 'TEdit3', $ssplit[2] )
			ControlSetText ( '�����������', '', 'TEdit2', $ssplit[3] )
			ControlSetText ( '�����������', '', 'TEdit1', $ssplit[4] )
		Else
			ControlSetText ( '�����������', '', 'TEdit1', $regname )
			ControlSetText ( '�����������', '', 'TEdit2', $serial )
		EndIf
		ControlClick ( '�����������', '', 'TButton2' )
		WinWait ( '���������' )
		WinActivate ( '���������' )
		WinWaitActive ( '���������' )
		Send ( '{ENTER}' )
		WinWaitClose ( '���������' )
    Case Else
		If FileExists ( @ScriptDir&'\'&$crackedexe ) Then
			FileCopy ( @ProgramFilesDir & '\UltraISO\UltraISO.exe', @ProgramFilesDir & '\UltraISO\UltraISO.exe.bak', 1 )
			FileCopy ( @ScriptDir & '\' & $crackedexe, @ProgramFilesDir & '\UltraISO\', 1 )
		EndIf
EndSelect
Sleep ( 30 )

;�������� ������ � �������� �����
FileDelete ( @DesktopDir & '\UltraISO.lnk' )

;����������� ������ �� ������ �������� �������
;If Not FileExists (@AppDataCommonDir & '\Microsoft\Internet Explorer\Quick Launch\') Then DirCreate (@AppDataCommonDir & '\Microsoft\Internet Explorer\Quick Launch\')
FileCopy ( @ProgramsCommonDir & '\' & $programgroup & '\UltraISO.lnk', @AppDataDir & '\Microsoft\Internet Explorer\Quick Launch\', 1 )

;������� ���� ����������
RegWrite('HKEY_CURRENT_USER\Software\EasyBoot Systems\UltraISO\5.0',"Language","REG_SZ",'1049')

;������� ���������� ���� � �����
;BlockInput ( 0 )
