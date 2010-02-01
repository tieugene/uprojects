#cs
----------------------
Приложение: FastStone Image Viewer / FastStone Screen Capture / FastStone Photo Resizer
На какой(их) версии(ях) тестировалось: 2.22; 2.26 beta 2; 2.28; 2.29 / 1.6 / 2.0

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
;
#cs
----------------------
объявление переменных
----------------------

$Title - заголовок окна установщика "FastStone Image Viewer"
$file - установочный файл
$programgroup - в какую программную группу положить ярлыки программы
$targetfolder - в какой каталог установить программу
$rus - русификатор для "FastStone Image Viewer" (если есть)
$fscapt - установщик "FastStone Screen Capture" (если есть)
$fsresz - установщик "FastStone Photo Resizer" (если есть)

$default (варианты установки)
0 - тихая установка (по ум.)
любое другое значение - клацанье по окнам

----------------------
#ce
Global $default=0, $Title='FastStone', $file='FSViewerSetup.exe', $rus='FastStone Image Viewer 2.29 Rus.exe', $fscapt='FSCaptureSetup.exe', $fsresz='FSResizerSetup.exe', $programgroup='Мультимедиа\FastStone Image Viewer', $targetfolder=@ProgramFilesDir & '\FastStone Image Viewer'
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
;снять галку с пункта "Run FastStone Image Viewer"
Send("{SPACE}")
Send("{ENTER}")
EndIf

;установка русификатора для "FastStone Image Viewer"
If FileExists ( @ScriptDir & '\' & $rus ) Then
Run ( @ScriptDir & '\' & $rus )
WinWaitActive ( 'Установка русификатора', 'Вас приветствует мастер' )
ControlClick ( 'Установка русификатора', 'Вас приветствует мастер', '&Далее >' )
WinWaitActive ( 'Установка русификатора', 'Информация' )
ControlClick ( 'Установка русификатора', 'Информация', '&Далее >' )
WinWaitActive ( 'Установка русификатора', 'Лицензионнное соглашение' )
ControlClick ( 'Установка русификатора', 'Лицензионнное соглашение', 'Button4' )
ControlClick ( 'Установка русификатора', 'Лицензионнное соглашение', '&Далее >' )
WinWaitActive ( 'Установка русификатора', 'Папка назначения' )
ControlClick ( 'Установка русификатора', 'Папка назначения', '&Далее >' )
WinWaitActive ( 'Установка русификатора', 'Подтверждение' )
ControlClick ( 'Установка русификатора', 'Подтверждение', '&Старт' )
WinWaitActive ( 'Установка русификатора', 'Готово' )
ControlClick ( 'Установка русификатора', 'Готово', 'Button5' )
ControlClick ( 'Установка русификатора', 'Готово', '&Выход' )
EndIf

If FileExists ( @ProgramsDir & '\FastStone Image Viewer\' ) Then
;удаление ярлыка с рабочего стола
FileDelete ( @DesktopDir & '\FastStone Image Viewer.lnk' )
;перемещение ярлыков
DirCopy ( @ProgramsDir & '\FastStone Image Viewer', @ProgramsCommonDir & '\' & $programgroup, 1 )
DirRemove ( @ProgramsDir & '\FastStone Image Viewer', 1 )
EndIf
If FileExists ( @ProgramsCommonDir & '\FastStone Image Viewer\' ) Then
FileDelete ( @DesktopCommonDir & '\FastStone Image Viewer.lnk' )
DirCopy ( @ProgramsCommonDir & '\FastStone Image Viewer', @ProgramsCommonDir & '\' & $programgroup, 1 )
DirRemove ( @ProgramsCommonDir & '\FastStone Image Viewer', 1 )
EndIf

;тихая установка "FastStone Photo Resizer"
If FileExists ( @ScriptDir & '\' & $fsresz ) Then
RunWait ( @ScriptDir&'\'&$fsresz &' /S' )
Sleep ( 70 )
FileDelete ( @DesktopCommonDir & '\FastStone Photo Resizer.lnk' )
DirCopy ( @ProgramsCommonDir & '\FastStone Photo Resizer', @ProgramsCommonDir & '\Мультимедиа\FastStone Photo Resizer', 1 )
DirRemove ( @ProgramsCommonDir & '\FastStone Photo Resizer', 1 )
EndIf

;тихая установка "FastStone Screen Capture"
If FileExists ( @ScriptDir & '\' & $fscapt ) Then
RunWait ( @ScriptDir&'\'&$fscapt &' /S' )
;после установки открывается страница http://www.faststone.org/ в браузере по умолчанию - закрываем процесс браузера
$defaultbrowser = RegRead ('HKEY_LOCAL_MACHINE\SOFTWARE\Clients\StartMenuInternet','')
ProcessWait ( $defaultbrowser, 2 )
ProcessClose ( $defaultbrowser )
ProcessWaitClose ( $defaultbrowser )
FileDelete ( @DesktopDir & '\FastStone Capture.lnk' )
DirCopy ( @ProgramsDir & '\FastStone Screen Capture', @ProgramsCommonDir & '\Мультимедиа\FastStone Screen Capture', 1 )
DirRemove ( @ProgramsDir & '\FastStone Screen Capture', 1 )
EndIf

;BlockInput ( 0 )