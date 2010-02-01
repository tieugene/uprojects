#cs
----------------------
Приложение: 7-Zip
На какой(их) версии(ях) тестировалось: 4.17 - 4.49

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
If ProcessExists ( "ps.exe" )<>0 Then
    ProcessClose ( "ps.exe" )
    ProcessWaitClose ( "ps.exe" )
EndIf
;нельзя блокировать при находящемся в памяти Punto Switcher-е - не будет работать установка
;блокируем мышь и клаву
;If @OSType="WIN32_NT" Then BlockInput ( 1 )
#cs
-----------------------------------
объявление переменных
-----------------------------------

$file - установочный файл
$programgroup - в какую программную группу положить ярлыки программы

-----------------------------------
#ce
Global $file='7z449.exe', $programgroup='Архиваторы\7-Zip'

;установка в тихом режиме
RunWait ( @ScriptDir&'\'&$file & ' /S' )

;н-рые настройки
RegWrite("HKEY_CURRENT_USER\Software\7-Zip","Lang","REG_SZ","ru")
RegWrite("HKEY_CURRENT_USER\Software\7-Zip\Compression","Solid","REG_DWORD",0x00000001)
RegWrite("HKEY_CURRENT_USER\Software\7-Zip\Compression","Level","REG_DWORD",0x00000007)
RegWrite("HKEY_CURRENT_USER\Software\7-Zip\Compression","Archiver","REG_SZ","7z")
RegWrite("HKEY_CURRENT_USER\Software\7-Zip\Compression\Options\7z","Level","REG_DWORD",0x00000007)
RegWrite("HKEY_CURRENT_USER\Software\7-Zip\Compression\Options\7z","Method","REG_SZ","LZMA")
RegWrite("HKEY_CURRENT_USER\Software\7-Zip\Compression\Options\7z","Dictionary","REG_DWORD",0x01000000)
RegWrite("HKEY_CURRENT_USER\Software\7-Zip\Compression\Options\7z","Order","REG_DWORD",0x00000080)
RegWrite("HKEY_CURRENT_USER\Software\7-Zip\FM","ShowGrid","REG_DWORD",0x00000001)
RegWrite("HKEY_CURRENT_USER\Software\7-Zip\Options","CascadedMenu","REG_DWORD",0x00000001)

;перенос ярлыков
If $programgroup<>'7-Zip' Then
	DirCopy ( @ProgramsCommonDir & '\7-Zip', @ProgramsCommonDir & '\' & $programgroup, 1 )
	DirRemove ( @ProgramsCommonDir & '\7-Zip', 1 )
EndIf

;добавление пути к 7-zip в системную переменную Path
;(для удобства использования архиватора совместно с Far-ом)
$addtopath=@ProgramFilesDir&'\7-Zip'
$smcur='HKEY_LOCAL_MACHINE\SYSTEM\ControlSet' & StringFormat("%03s",RegRead("HKEY_LOCAL_MACHINE\SYSTEM\Select","Current")) & '\Control\Session Manager\Environment'
$syscurpath=RegRead($smcur,"Path")
;если путь уже был внесен в Path (например, при установке поверх более старой версии), то ничего не делаем
If Not StringInStr ($syscurpath,'%ProgramFiles%\7-Zip') and Not StringInStr ($syscurpath,$addtopath) Then
	RegWrite($smcur,"Path","REG_EXPAND_SZ",RegRead($smcur,"Path") & ";" & $addtopath)
EndIf

;BlockInput ( 0 )
