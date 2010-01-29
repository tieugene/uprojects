#cs
----------------------
����������: Mozilla Thunderbird
�� �����(��) ������(��) �������������: 1.0 (en); 1.0.5 (en); 1.0.6 (en); 1.0.7 (ru/en); 1.5 Beta 2 (en); 1.5 (ru/en); 1.5.0.2 (ru/en); 1.5.0.4 (ru/en); 1.5.0.7 (ru/en); 1.5.0.8 (ru/en); 1.5.0.9 (ru/en); 1.5.0.10 (ru/en); 2.0.0.0 (ru/en); 2.0.0.4 (ru/en); 2.0.0.12 (ru/en); 2.0.0.14 (ru/en)

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
AutoItSetOption("WinTitleMatchMode", 2)
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

$file - ������������ ����
$lang - ���� ������ ('ru' - ��� ������� ������; ����� ������ �������� - ��� ����. ������)
$programgroup - � ����� ����������� ������ �������� ������ ���������
$delfromdesk - ������� ��� ��� ����� � "�������� �����" (1 - ��, ����� ������ �������� - ���)

����� ���� �� �������� ��� ���������� $lang, ��, ��������� ����� ������� ����������� 
���� ���������� ������������ ������ �� 7z-sfx ������ (� ����������������� ����� ����� 
������ ������� �� ������� CPU � �������� HDD), �� �������� �� ��������� ��������� 
������� (� �������� �� ��������� CPU/HDD) ��� ����������� ����� ������ �� 
������� ���� �����������.
���� �� ����� �������������� ����� ����� ������� �����, ������ ����������� 
����� (��������, ��� "Thunderbird Setup 1.0.7.exe" �� 6 � ��������� �� ��������� 23).
� ���� ��. ���������� ���������� $file='setup.exe'.

$default (�������� ���������)
0 - ����� ��������� (�� ��.)
1 - ��������� � ��������� �� �����

----------------------
#ce
Global $default=0, $file='Russian\Thunderbird Setup 2.0.0.14.exe', $lang='ru', $programgroup='����\Mozilla Thunderbird', $delfromdesk=1

If $default=0 Then
	RunWait ( @ScriptDir & '\' & $file & ' -ms -ira' )
Else
	AutoItSetOption("WinTitleMatchMode",2)
	Run ( @ScriptDir & '\' & $file )
	If $lang='ru' Then
		WinWaitActive ( 'Mozilla Thunderbird', '��������� Mozilla Thunderbird' )
		Sleep ( 100 )
		Send ( '{ENTER}' )
		WinWaitActive ( '������������ ����������' )
		;� �������� ������� ������������� ����������
		ControlClick ( '������������ ����������', '', 'Button2' )
		Send ( '{ENTER}' )
		WinWaitActive ( '��� ���������' )
		;�������
		Send ( '{ENTER}' )
		WinWaitActive ( '����� �����������' )
		;$InstPath = ControlGetText ( 'Select Components', '', 'Static6')
		Send ( '{ENTER}' )
		WinWaitActive ( '�������' )
		;����� ����� "��������� Mozilla Thunderbird"
		ControlClick ( '�������', '', 'Button1' )
	Else
		WinWaitActive ( 'Mozilla Thunderbird Setup' )
		Sleep ( 100 )
		Send ( '{ENTER}' )
		WinWaitActive ( 'Software License Agreement' )
		;I Accept the terms of the License Agreement
		ControlClick ( 'Software License Agreement', '', 'Button2' )
		Send ( '{ENTER}' )
		WinWaitActive ( 'Setup Type' )
		;Standard
		Send ( '{ENTER}' )
		WinWaitActive ( 'Select Components' )
		Send ( '{ENTER}' )
		WinWaitActive ( 'Install Complete' )
		ControlClick ( 'Install Complete', '', 'Button1' )
	EndIf
	Send ( '{ENTER}' )
	Sleep ( 50 )
EndIf

;������� � �������� �������
If $delfromdesk=1 Then FileDelete ( @DesktopCommonDir & '\Mozilla Thunderbird.lnk' )

If $programgroup<>'Mozilla Thunderbird' Then
	DirCopy ( @ProgramsCommonDir & '\Mozilla Thunderbird', @ProgramsCommonDir & '\' & $programgroup, 1 )
	DirRemove ( @ProgramsCommonDir & '\Mozilla Thunderbird', 1 )
EndIf

;BlockInput ( 0 )
