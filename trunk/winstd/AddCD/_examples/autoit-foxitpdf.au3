#cs
----------------------
Приложение: Foxit PDF Reader
На какой(их) версии(ях) тестировалось: 1.3 (Сборка 0708); 1.3 (Сборка 0930); 1.3 (Сборка 1209); 1.3 (Сборка 1413); 1.3 (Сборка 1522); 1.3 (Сборка 1621); 2.0 beta (Сборка 0609); 2.0 (Сборка 0912); 2.0 (Сборка 0930); 2.0 (Сборка 1312); 2.0 (Сборка 1414); 2.0 (Сборка 1606); 2.1 (Сборка 2023); 2.3 (Сборка 2825)

Автор скрипта: Sanja Alone (http://forum.oszone.net/member.php?userid=28800)
----------------------
#ce
;предотвращение возможности множественного запуска скрипта
If WinExists(@ScriptName) Then Exit
AutoItWinSetTitle(@ScriptName)
;скрыть в системной панели индикатор AutoIt
;AutoItSetOption("TrayIconHide", 1)
;Отображать текущую строку сценария с помощью индикатора системной панели в режиме отладки.
AutoItSetOption("TrayIconDebug", 1)
AutoItSetOption("SendKeyDelay", 10)
If ProcessExists ( "ps.exe" )<>0 Then
    ProcessClose ( "ps.exe" )
    ProcessWaitClose ( "ps.exe" )
EndIf
;нельзя блокировать при находящемся в памяти Punto Switcher-е - не будет работать установка
;блокируем мышь и клаву
;If @OSType="WIN32_NT" Then BlockInput ( 1 )
#cs
----------------------
объявление переменных
----------------------

$Title - заголовок окна установки
$file - установочный файл
$programgroup - в какую программную группу положить ярлыки программы
$InstPath - путь установки по ум. (!! НЕ ИЗМЕНЯЙТЕ, если исп-те 0 или 1 варианты установки !!)

$default (варианты установки)
0 - тихая установка (не работает на новых версиях)
1 - если есть только exe-файл самой программы (переменная $exe), то можно провести установку по типу WinPE (копирование + внесение в реестр необходимых данных)
2 - установка с клацаньем по окнам

Для новых версий (1.3.1413 и выше):
	Если есть желание провести установку по типу WinPE, то, запустите установщик, 
	и, дождавшись появления первого окна, зайдите в свою папку TEMP (скорее всего 
	это будет или %windir%\Temp или %AppData%\Temp). Из этой папки извлеките 
	файл Foxit Reader.exe (если хотите иметь возм-ть удаления программы через 
	"Установка и удаление программ", то еще и Uninstall.exe) и положите рядом 
	с этим скриптом не забыв присвоить правильное имя файла переменной $exe.

----------------------
#ce
Global $default=1, $file='foxitreader_setup.exe', $InstPath=@ProgramFilesDir & '\Foxit Reader', $programgroup='Офис\Foxit PDF Reader', $Title='Foxit', $exe='Foxit Reader.exe'
Select
	Case $default=0 and FileExists ( @ScriptDir & '\' & $file )
		RunWait ( @ScriptDir & '\' & $file & ' /VERYSILENT /SP- /DIR="' & $InstPath & '" /GROUP="' & $programgroup & '"' )
	Case $default=1 and FileExists ( @ScriptDir & '\' & $exe )
		If Not FileExists ( $InstPath ) Then DirCreate ( $InstPath )
		If FileExists ( $InstPath & '\' & $exe ) Then FileSetAttrib ( $InstPath & '\' & $exe, "-R" )
		FileCopy ( @ScriptDir & '\' & $exe, $InstPath & '\' & $exe, 1 )
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\.pdf',"","REG_SZ",'FoxitReader.Document')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\.pdf',"Content Type","REG_SZ",'application/pdf')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\FoxitReader.Document',"","REG_SZ",'PDF Document')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\FoxitReader.Document',"BrowseInPlace","REG_SZ",'1')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\FoxitReader.Document\DefaultIcon',"","REG_SZ",FileGetShortName($InstPath&'\'&$exe)&',1')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\FoxitReader.Document\DocObject',"","REG_SZ",'0')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\FoxitReader.Document\Insertable',"","REG_SZ",'')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\FoxitReader.Document\protocol\StdFileEditing\server',"","REG_SZ",FileGetShortName($InstPath&'\'&$exe))
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\FoxitReader.Document\protocol\StdFileEditing\verb\0',"","REG_SZ",'&Edit')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\FoxitReader.Document\shell\open\command',"","REG_SZ",'"'&FileGetShortName($InstPath&'\'&$exe)&'" "%1"')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\FoxitReader.Document\shell\open\ddeexec')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\FoxitReader.Document\shell\print\command',"","REG_SZ",FileGetShortName($InstPath&'\'&$exe)&' /dde')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\FoxitReader.Document\shell\print\ddeexec',"","REG_SZ",'[print("%1")]')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\FoxitReader.Document\shell\printto\command',"","REG_SZ",FileGetShortName($InstPath&'\'&$exe)&' /dde')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\FoxitReader.Document\shell\printto\ddeexec',"","REG_SZ",'[printto("%1","%2","%3","%4")]')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\FoxitReader.Document\CLSID',"","REG_SZ",'{14E8BBD8-1D1C-4D56-A4DA-D20B75EB814E}')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{14E8BBD8-1D1C-4D56-A4DA-D20B75EB814E}',"","REG_SZ",'PDF Document')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{14E8BBD8-1D1C-4D56-A4DA-D20B75EB814E}\AuxUserType\2',"","REG_SZ",'PDF')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{14E8BBD8-1D1C-4D56-A4DA-D20B75EB814E}\AuxUserType\3',"","REG_SZ",'Foxit Reader')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{14E8BBD8-1D1C-4D56-A4DA-D20B75EB814E}\DefaultExtension',"","REG_SZ",'.pdf, PDF Files(*.pdf)')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{14E8BBD8-1D1C-4D56-A4DA-D20B75EB814E}\DefaultIcon',"","REG_SZ",FileGetShortName($InstPath&'\'&$exe)&',1')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{14E8BBD8-1D1C-4D56-A4DA-D20B75EB814E}\DocObject',"","REG_SZ",'0')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{14E8BBD8-1D1C-4D56-A4DA-D20B75EB814E}\InprocHandler32',"","REG_SZ",'ole32.dll')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{14E8BBD8-1D1C-4D56-A4DA-D20B75EB814E}\Insertable',"","REG_SZ",'')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{14E8BBD8-1D1C-4D56-A4DA-D20B75EB814E}\LocalServer32',"","REG_SZ",FileGetShortName($InstPath&'\'&$exe))
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{14E8BBD8-1D1C-4D56-A4DA-D20B75EB814E}\MiscStatus',"","REG_SZ",'32')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{14E8BBD8-1D1C-4D56-A4DA-D20B75EB814E}\Printable',"","REG_SZ",'')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{14E8BBD8-1D1C-4D56-A4DA-D20B75EB814E}\ProgID',"","REG_SZ",'FoxitReader.Document')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{14E8BBD8-1D1C-4D56-A4DA-D20B75EB814E}\Verb\0',"","REG_SZ",'&Edit,0,2')
		RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{14E8BBD8-1D1C-4D56-A4DA-D20B75EB814E}\Verb\1',"","REG_SZ",'&Open,0,2')
;		If FileExists ( @ScriptDir & '\Uninstall.exe' ) Then
;			FileCopy ( @ScriptDir & '\Uninstall.exe', $InstPath & '\', 1 )
;			RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Foxit Reader','UninstallString',"REG_SZ",$InstPath&'\Uninstall.exe')
;			RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Foxit Reader','DisplayName',"REG_SZ",'Foxit Reader')
;			RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Foxit Reader','DisplayIcon',"REG_SZ",$InstPath&'\'&$exe)
;			RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Foxit Reader','UninstallPath',"REG_SZ",$InstPath&'\Uninstall.exe')
;		EndIf
	Case $default=2 and FileExists ( @ScriptDir & '\' & $file )
		;AutoItSetOption("WinDetectHiddenText",1)
		;AutoItSetOption("WinTitleMatchMode",2)
		Run ( @ScriptDir & '\' & $file )
		;WinWait($Title,"",10)
		;WinActivate($Title)
		;WinWaitActive($Title)
		;AutoItSetOption("WinTitleMatchMode",4)
		;старый или новый инсталлятор (TWizardForm - имя класса окна старого инсталлятора)
		;$handle=WinGetHandle("classname=TWizardForm")
		;$Title=WinGetTitle("")
		;$err = @error
		;msgbox(0,'','<'&$Title&'>'&@LF&'<'&$err&'>')
		;AutoItSetOption("WinTitleMatchMode",1)
		If StringLeft($Title,9)<>"Установка" Then
			WinWait($Title,"Setup will install")
			WinActivate($Title,"Setup will install")
			WinWaitActive($Title,"Setup will install")
			Send("{ENTER}")
			WinWait($Title,"Please read")
			WinActivate($Title,"Please read")
			WinWaitActive($Title,"Please read")
			Send("{ENTER}")
			WinWait($Title,"Please select")
			WinActivate($Title,"Please select")
			WinWaitActive($Title,"Please select")
			;Custom
			ControlClick($Title,"Please select","Button2")
			WinWait($Title,"Please Choose the folder")
			WinActivate($Title,"Please Choose the folder")
			WinWaitActive($Title,"Please Choose the folder")
			If $InstPath<>@ProgramFilesDir & '\Foxit Software\Foxit Reader' Then ControlSetText($Title,"Please Choose the folder","Edit1",$InstPath)
			;по ум. C:\Program Files\Foxit Software\Foxit Reader\
			Send("{ENTER}")
			WinWait($Title,"Desktop Settings")
			WinActivate($Title,"Desktop Settings")
			WinWaitActive($Title,"Desktop Settings")
			;отключить "Add a desktop shortcut"
			ControlClick($Title,"Desktop Settings","Button3")
			;отключить "Add an icon to the Start Menu"
			ControlClick($Title,"Desktop Settings","Button4")
			;отключить "Add an icon to Windows Quick Launch Toolbar"
			ControlClick($Title,"Desktop Settings","Button7")
			Send("{ENTER}")
			WinWait($Title,"Click Install")
			WinActivate($Title,"Click Install")
			WinWaitActive($Title,"Click Install")
			Send("{ENTER}")
			WinWait($Title,"Setup has successfully")
			WinActivate($Title,"Setup has successfully")
			WinWaitActive($Title,"Setup has successfully")
			;снять галку "Run Foxit Reader"
			ControlClick($Title,"Setup has successfully","Button2")
			Send("{ENTER}")
		Else
			WinWait($Title,"Вас приветствует")
			WinActivate($Title,"Вас приветствует")
			WinWaitActive($Title,"Вас приветствует")
			Send("{ENTER}")
			WinWait($Title,"Выбор папки")
			WinActivate($Title,"Выбор папки")
			WinWaitActive($Title,"Выбор папки")
			If $InstPath<>@ProgramFilesDir&'\Foxit PDF Reader' Then
			Send($InstPath)
			;по ум. C:\Program Files\Foxit PDF Reader
			EndIf
			Send("{ENTER}")
			WinWait($Title,"Выберите папку в мен")
			WinActivate($Title,"Выберите папку в мен")
			WinWaitActive($Title,"Выберите папку в мен")
			Send($programgroup)
			Send("{ENTER}")
			WinWait($Title,"Выберите дополнитель")
			WinActivate($Title,"Выберите дополнитель")
			WinWaitActive($Title,"Выберите дополнитель")
			Send("{ENTER}")
			WinWait($Title,"Всё готово к установ")
			WinActivate($Title,"Всё готово к установ")
			WinWaitActive($Title,"Всё готово к установ")
			Send("{ENTER}")
			WinWait($Title,"Завершение Мастера у")
			WinActivate($Title,"Завершение Мастера у")
			WinWaitActive($Title,"Завершение Мастера у")
			Send("{SPACE}")
			Send("{ENTER}")
		EndIf
EndSelect

;отключить рекламу
RegWrite('HKEY_CURRENT_USER\Software\Foxit Software\Foxit Reader\MainFrame','ShowEditorAd1.3',"REG_SZ",'0')
RegWrite('HKEY_CURRENT_USER\Software\Foxit Software\Foxit Reader\MainFrame','ShowReaderAd1.3',"REG_SZ",'0')
RegWrite('HKEY_CURRENT_USER\Software\Foxit Software\Foxit Reader\MainFrame','ShowTypewriterAd1.3',"REG_SZ",'0')
RegWrite('HKEY_CURRENT_USER\Software\Foxit Software\Foxit Reader\MainFrame','ShowEditorAd_908',"REG_SZ",'0')
RegWrite('HKEY_CURRENT_USER\Software\Foxit Software\Foxit Reader\MainFrame','ShowReaderAd_908',"REG_SZ",'0')
RegWrite('HKEY_CURRENT_USER\Software\Foxit Software\Foxit Reader\MainFrame','ShowTypewriterAd_908',"REG_SZ",'0')
RegWrite('HKEY_CURRENT_USER\Software\Foxit Software\Foxit Reader\MainFrame','ShowPOAd_908',"REG_SZ",'0')
RegWrite('HKEY_CURRENT_USER\Software\Foxit Software\Foxit Reader\MainFrame','ShowSDKAd_908',"REG_SZ",'0')

;BlockInput ( 0 )
