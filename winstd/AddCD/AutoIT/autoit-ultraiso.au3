#cs
----------------------
Приложение: UltraISO
На какой(их) версии(ях) тестировалось: 7.6.1.1125; 7.6.2.1180; 7.6.5.1225; 7.6.5.1269; 8.0.0.1392; 8.1.2.1625; 8.2.0.1669; 8.5.1.1860; 8.6.0.1936; 8.6.1.1985; 8.6.3.2052; 9.1.2.2465; 9.2.0.2536

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
;нельзя блокировать (и нормально ввести серийник) при находящемся в памяти Punto Switcher-е - не будет работать установка
;блокируем мышь и клаву
;If @OSType="WIN32_NT" Then BlockInput ( 1 )
#cs
----------------------
объявление переменных
----------------------

$file - установочный файл
$programgroup - в какую программную группу положить ярлыки программы

Введите свои имя и серийник соответственно в переменные $regname и $serial.

Если у Вас версия UltraISO < 7.62 измените значение переменной $ver 
на что-нибудь отличное от 'new'.

При отсутствии рабочего серийника (переменная $serial='') производится проверка на 
наличие крякнутого экзэшника, и, в сл. положительного рез-та, файл копируется в 
директорию UltraISO (переменная $crackedexe).

----------------------
#ce
Global $ver='new', $file='uiso9_pe.exe', $regname='', $serial='', $programgroup='CD и DVD утилиты\UltraISO', $crackedexe='UltraISO.exe'

;запуск установки в тихом режиме
RunWait ( @ScriptDir&'\'&$file & ' /VERYSILENT /SP- /GROUP="' & $programgroup & '"' )
Select
    Case $serial<>''
		;запуск проги для появления диалога регистрации
		Run ( @ProgramFilesDir & '\UltraISO\UltraISO.exe' )
		WinWait ( 'Добро пожаловать' )
		WinActivate ( 'Добро пожаловать' )
		WinWaitActive ( 'Добро пожаловать' )
		ControlClick ( 'Добро пожаловать', '', 'TButton4' )
		WinWait ( 'Регистрация' )
		WinActivate ( 'Регистрация' )
		WinWaitActive ( 'Регистрация' )
		;ввод рег. данных
		;Начиная с версии 7.62 серийник при регистрации вводится сплошной строкой 
		;(для более ранних версий требуется его разделение)
		If $ver <> 'new' Then
			$ssplit = StringSplit ( $serial, "-" )
			ControlSetText ( 'Регистрация', '', 'TEdit4', $regname )
			ControlSetText ( 'Регистрация', '', 'TEdit5', $ssplit[1] )
			ControlSetText ( 'Регистрация', '', 'TEdit3', $ssplit[2] )
			ControlSetText ( 'Регистрация', '', 'TEdit2', $ssplit[3] )
			ControlSetText ( 'Регистрация', '', 'TEdit1', $ssplit[4] )
		Else
			ControlSetText ( 'Регистрация', '', 'TEdit1', $regname )
			ControlSetText ( 'Регистрация', '', 'TEdit2', $serial )
		EndIf
		ControlClick ( 'Регистрация', '', 'TButton2' )
		WinWait ( 'Подсказка' )
		WinActivate ( 'Подсказка' )
		WinWaitActive ( 'Подсказка' )
		Send ( '{ENTER}' )
		WinWaitClose ( 'Подсказка' )
    Case Else
		If FileExists ( @ScriptDir&'\'&$crackedexe ) Then
			FileCopy ( @ProgramFilesDir & '\UltraISO\UltraISO.exe', @ProgramFilesDir & '\UltraISO\UltraISO.exe.bak', 1 )
			FileCopy ( @ScriptDir & '\' & $crackedexe, @ProgramFilesDir & '\UltraISO\', 1 )
		EndIf
EndSelect
Sleep ( 30 )

;удаление ярлыка с рабочего стола
FileDelete ( @DesktopDir & '\UltraISO.lnk' )

;копирование ярлыка на панель быстрого запуска
;If Not FileExists (@AppDataCommonDir & '\Microsoft\Internet Explorer\Quick Launch\') Then DirCreate (@AppDataCommonDir & '\Microsoft\Internet Explorer\Quick Launch\')
FileCopy ( @ProgramsCommonDir & '\' & $programgroup & '\UltraISO.lnk', @AppDataDir & '\Microsoft\Internet Explorer\Quick Launch\', 1 )

;русский язык интерфейса
RegWrite('HKEY_CURRENT_USER\Software\EasyBoot Systems\UltraISO\5.0',"Language","REG_SZ",'1049')

;снимаем блокировку мыши и клавы
;BlockInput ( 0 )
