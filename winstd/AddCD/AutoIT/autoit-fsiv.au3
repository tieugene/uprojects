#cs
----------------------
����������: FastStone Image Viewer / FastStone Screen Capture / FastStone Photo Resizer
�� �����(��) ������(��) �������������: 2.22; 2.26 beta 2; 2.28; 2.29 / 1.6 / 2.0

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
AutoItSetOption("SendKeyDelay", 10)
If ProcessExists ( "ps.exe" )<>0 Then
     ProcessClose ( "ps.exe" )
     ProcessWaitClose ( "ps.exe" )
EndIf
;������ ����������� ��� ����������� � ������ Punto Switcher-� - �� ����� �������� ���������
;��������� ���� � �����
;If @OSType="WIN32_NT" Then BlockInput ( 1 )
;
#cs
----------------------
���������� ����������
----------------------

$Title - ��������� ���� ����������� "FastStone Image Viewer"
$file - ������������ ����
$programgroup - � ����� ����������� ������ �������� ������ ���������
$targetfolder - � ����� ������� ���������� ���������
$rus - ����������� ��� "FastStone Image Viewer" (���� ����)
$fscapt - ���������� "FastStone Screen Capture" (���� ����)
$fsresz - ���������� "FastStone Photo Resizer" (���� ����)

$default (�������� ���������)
0 - ����� ��������� (�� ��.)
����� ������ �������� - �������� �� �����

----------------------
#ce
Global $default=0, $Title='FastStone', $file='FSViewerSetup.exe', $rus='FastStone Image Viewer 2.29 Rus.exe', $fscapt='FSCaptureSetup.exe', $fsresz='FSResizerSetup.exe', $programgroup='�����������\FastStone Image Viewer', $targetfolder=@ProgramFilesDir & '\FastStone Image Viewer'
If $default=0 Then
RunWait(@ScriptDir&'\'&$file &' /S /D=' & $targetfolder)
Else
Run(@ScriptDir&'\'&$file &' /D=' & $targetfolder)
WinWait($Title,"This wizard")
If Not WinActive($Title,"This wizard") Then WinActivate($Title,"This wizard")
WinWaitActive($Title,"This wizard")
Send("{ENTER}")
WinWait($Title,"License Agreement")
If Not WinActive($Title,"License Agreement") Then WinActivate($Title,"License Agreement")
WinWaitActive($Title,"License Agreement")
Send("{ENTER}")
WinWait($Title,"Choose Install Location")
If Not WinActive($Title,"Choose Install Location") Then WinActivate($Title,"Choose Install Location")
WinWaitActive($Title,"Choose Install Location")
Send("{ENTER}")
WinWait($Title,"Completing")
If Not WinActive($Title,"Completing") Then WinActivate($Title,"Completing")
WinWaitActive($Title,"Completing")
;����� ����� � ������ "Run FastStone Image Viewer"
Send("{SPACE}")
Send("{ENTER}")
EndIf

;��������� ������������ ��� "FastStone Image Viewer"
If FileExists ( @ScriptDir & '\' & $rus ) Then
Run ( @ScriptDir & '\' & $rus )
WinWaitActive ( '��������� ������������', '��� ������������ ������' )
ControlClick ( '��������� ������������', '��� ������������ ������', '&����� >' )
WinWaitActive ( '��������� ������������', '����������' )
ControlClick ( '��������� ������������', '����������', '&����� >' )
WinWaitActive ( '��������� ������������', '������������� ����������' )
ControlClick ( '��������� ������������', '������������� ����������', 'Button4' )
ControlClick ( '��������� ������������', '������������� ����������', '&����� >' )
WinWaitActive ( '��������� ������������', '����� ����������' )
ControlClick ( '��������� ������������', '����� ����������', '&����� >' )
WinWaitActive ( '��������� ������������', '�������������' )
ControlClick ( '��������� ������������', '�������������', '&�����' )
WinWaitActive ( '��������� ������������', '������' )
ControlClick ( '��������� ������������', '������', 'Button5' )
ControlClick ( '��������� ������������', '������', '&�����' )
EndIf

If FileExists ( @ProgramsDir & '\FastStone Image Viewer\' ) Then
;�������� ������ � �������� �����
FileDelete ( @DesktopDir & '\FastStone Image Viewer.lnk' )
;����������� �������
DirCopy ( @ProgramsDir & '\FastStone Image Viewer', @ProgramsCommonDir & '\' & $programgroup, 1 )
DirRemove ( @ProgramsDir & '\FastStone Image Viewer', 1 )
EndIf
If FileExists ( @ProgramsCommonDir & '\FastStone Image Viewer\' ) Then
FileDelete ( @DesktopCommonDir & '\FastStone Image Viewer.lnk' )
DirCopy ( @ProgramsCommonDir & '\FastStone Image Viewer', @ProgramsCommonDir & '\' & $programgroup, 1 )
DirRemove ( @ProgramsCommonDir & '\FastStone Image Viewer', 1 )
EndIf

;����� ��������� "FastStone Photo Resizer"
If FileExists ( @ScriptDir & '\' & $fsresz ) Then
RunWait ( @ScriptDir&'\'&$fsresz &' /S' )
Sleep ( 70 )
FileDelete ( @DesktopCommonDir & '\FastStone Photo Resizer.lnk' )
DirCopy ( @ProgramsCommonDir & '\FastStone Photo Resizer', @ProgramsCommonDir & '\�����������\FastStone Photo Resizer', 1 )
DirRemove ( @ProgramsCommonDir & '\FastStone Photo Resizer', 1 )
EndIf

;����� ��������� "FastStone Screen Capture"
If FileExists ( @ScriptDir & '\' & $fscapt ) Then
RunWait ( @ScriptDir&'\'&$fscapt &' /S' )
;����� ��������� ����������� �������� http://www.faststone.org/ � �������� �� ��������� - ��������� ������� ��������
$defaultbrowser = RegRead ('HKEY_LOCAL_MACHINE\SOFTWARE\Clients\StartMenuInternet','')
ProcessWait ( $defaultbrowser, 2 )
ProcessClose ( $defaultbrowser )
ProcessWaitClose ( $defaultbrowser )
FileDelete ( @DesktopDir & '\FastStone Capture.lnk' )
DirCopy ( @ProgramsDir & '\FastStone Screen Capture', @ProgramsCommonDir & '\�����������\FastStone Screen Capture', 1 )
DirRemove ( @ProgramsDir & '\FastStone Screen Capture', 1 )
EndIf

;BlockInput ( 0 )