#cs
----------------------
Приложение: Mozilla Thunderbird
На какой(их) версии(ях) тестировалось: 1.0 (en); 1.0.5 (en); 1.0.6 (en); 1.0.7 (ru/en); 1.5 Beta 2 (en); 1.5 (ru/en); 1.5.0.2 (ru/en); 1.5.0.4 (ru/en); 1.5.0.7 (ru/en); 1.5.0.8 (ru/en); 1.5.0.9 (ru/en); 1.5.0.10 (ru/en); 2.0.0.0 (ru/en); 2.0.0.4 (ru/en); 2.0.0.12 (ru/en); 2.0.0.14 (ru/en)

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
AutoItSetOption("WinTitleMatchMode", 2)
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

$file - установочный файл
$lang - язык пакета ('ru' - для русской версии; любое другое значение - для англ. версии)
$programgroup - в какую программную группу положить ярлыки программы
$delfromdesk - удалить или нет ярлык с "Рабочего стола" (1 - да, любое другое значение - нет)

Можно было бы обойтись без переменной $lang, но, поскольку перед началом инсталляции 
идет извлечение установочных файлов из 7z-sfx архива (а продолжительность этого этапа 
сильно зависит от частоты CPU и скорости HDD), то пришлось бы поставить приличный 
таймаут (с расчетом на медленные CPU/HDD) для определения языка пакета по 
первому окну установщика.
Если на Вашем исталляционном диске полно лишнего места, можете распаковать 
архив (например, для "Thunderbird Setup 1.0.7.exe" из 6 с небольшим Мб получится 23).
В этом сл. определите переменную $file='setup.exe'.

$default (варианты установки)
0 - тихая установка (по ум.)
1 - установка с клацаньем по окнам

----------------------
#ce
Global $default=0, $file='Russian\Thunderbird Setup 2.0.0.14.exe', $lang='ru', $programgroup='Сеть\Mozilla Thunderbird', $delfromdesk=1

If $default=0 Then
	RunWait ( @ScriptDir & '\' & $file & ' -ms -ira' )
Else
	AutoItSetOption("WinTitleMatchMode",2)
	Run ( @ScriptDir & '\' & $file )
	If $lang='ru' Then
		WinWaitActive ( 'Mozilla Thunderbird', 'Установка Mozilla Thunderbird' )
		Sleep ( 100 )
		Send ( '{ENTER}' )
		WinWaitActive ( 'Лицензионное соглашение' )
		;Я принимаю условия Лицензионного соглашения
		ControlClick ( 'Лицензионное соглашение', '', 'Button2' )
		Send ( '{ENTER}' )
		WinWaitActive ( 'Тип установки' )
		;Обычная
		Send ( '{ENTER}' )
		WinWaitActive ( 'Выбор компонентов' )
		;$InstPath = ControlGetText ( 'Select Components', '', 'Static6')
		Send ( '{ENTER}' )
		WinWaitActive ( 'авершен' )
		;снять галку "Запустить Mozilla Thunderbird"
		ControlClick ( 'авершен', '', 'Button1' )
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

;перенос и удаление ярлыков
If $delfromdesk=1 Then FileDelete ( @DesktopCommonDir & '\Mozilla Thunderbird.lnk' )

If $programgroup<>'Mozilla Thunderbird' Then
	DirCopy ( @ProgramsCommonDir & '\Mozilla Thunderbird', @ProgramsCommonDir & '\' & $programgroup, 1 )
	DirRemove ( @ProgramsCommonDir & '\Mozilla Thunderbird', 1 )
EndIf

;BlockInput ( 0 )
