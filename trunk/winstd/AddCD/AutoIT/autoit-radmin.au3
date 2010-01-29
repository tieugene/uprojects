#cs
----------------------
Приложение: Remote Administrator
На какой(их) версии(ях) тестировалось: 2.2 (ru/en)

Этот скрипт работает как с русской, так и с английской версией RAdmin-а.

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
AutoItSetOption("SendKeyDelay", 15)
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

$Title - заголовок окна установщика ('Remote Administrator' у обеих версий)
$file - установочный файл
$InstPath - в какой каталог установить программу
$programgroup - в какую программную группу положить ярлыки программы
$password - пароль для изменения настроек RAdmin-а (по ум. - mypassword; вместо пароля можно исп-ть NT security - тогда задайте $password='' )

$serial - серийник в оригинальном виде (если неохота возиться с реестром) ИЛИ значение параметра "Data" 
ветки "HKEY_LOCAL_MACHINE\SOFTWARE\RAdmin\v1.01\ViewType". Введите сюда свое значение данного параметра 
в формате AutoIt-а (т.е. не через запятую, как в reg-файле, а одной строкой). Если последнее непонятно - 
можете почитать Autoit.chm (ремарки к функции RegWrite). Если все равно не понятно - воспользуйтесь моим 
конвертером ConvRegToAu3 (http://sanjaalone.h15.ru/crta.php). Извиняюсь, если кого-то обидел такими 
уточнениями, но был прецедент... Эта запись - закодированный каким-то способом серийник.

язык дистрибутива определяется по двум последним буквам имени установочного файла ('ru' - рус., 'en' - англ.)

----------------------
#ce
Global $Title='Remote Administrator', $file='radmin22ru.exe', $InstPath=@ProgramFilesDir & '\Radmin', $programgroup='Сеть\Remote Administrator', $password='mypassword', $serial=''

;определение языка дистрибутива
$lang=StringLower ( StringLeft ( StringRight ( $file, 6 ), 2 ) )

Run ( @ScriptDir&'\'&$file )

If $lang='ru' Then
	WinWait ( $Title, 'Добро пожаловать' )
	WinActivate ( $Title, 'Добро пожаловать' )
	WinWaitActive ( $Title, 'Добро пожаловать' )
	Send ( '{ENTER}' )
	WinWaitActive ( $Title, 'Я принимаю это соглашение' )
	;выбрать пункт "Я принимаю это соглашение"
	ControlClick ( $Title, 'Я принимаю это соглашение', 'Button1' )
	Send ( '{ENTER}' )
	WinWaitActive ( $Title, 'Внимание!' )
	Send ( '{ENTER}' )
	WinWaitActive ( $Title, 'Варианты установки' )
	Send ( '{ENTER}' )
	WinWaitActive ( $Title, 'Директория установки' )
	;по ум. C:\Program Files\Radmin
	If $InstPath<>@ProgramFilesDir & '\Radmin' Then ControlSetText ( $Title, 'Директория установки', 'Edit1', $InstPath )
	Send ( '{ENTER}' )
	WinWait ( $Title, 'FolderView' )
	WinClose ( $Title, 'FolderView' )
	WinWait ( 'Авторизация', 'Пароль' )
	WinActivate ( 'Авторизация', 'Пароль' )
	WinWaitActive ( 'Авторизация', 'Пароль' )
	;проверка на случай переустановки
	If ControlCommand ( 'Авторизация', 'Пароль', 'Button4', 'IsEnabled', '' )=1 Then ControlClick ( 'Авторизация', 'Пароль', 'Button3' )
	;здесь возможны 2 варианта
	If $password<>'' Then
		;Ввести пароль
		ControlSetText ( 'Авторизация', 'Пароль', "Edit1", $password )
		ControlSetText ( 'Авторизация', 'Пароль', "Edit2", $password )
	Else
		;Включить NT security [назначить права пользователям можно будет вручную после установки, запустив "Настройка Remote Administrator server" (r_server.exe /setup) -> "Авторизация..." -> "Права"]
		ControlClick ( 'Авторизация', 'Пароль', 'Button3' )
	EndIf
	Send ( '{ENTER}' )
	WinWaitActive ( 'Подтверждение' )
	ControlClick ( 'Подтверждение', '', 'Button2' )
Else
	WinWait ( $Title, 'Welcome' )
	WinActivate ( $Title, 'Welcome' )
	WinWaitActive ( $Title, 'Welcome' )
	Send ( '{ENTER}' )
	WinWaitActive ( $Title, 'To proceed with the installation' )
	;выбрать пункт "Я принимаю это соглашение"
	ControlClick ( $Title, 'To proceed with the installation', 'Button1' )
	Send ( '{ENTER}' )
	WinWaitActive ( $Title, 'Important notes' )
	Send ( '{ENTER}' )
	WinWaitActive ( $Title, 'Installation options' )
	Send ( '{ENTER}' )
	WinWaitActive ( $Title, 'Destination Directory' )
	;по ум. C:\Program Files\Radmin
	If $InstPath<>@ProgramFilesDir & '\Radmin' Then ControlSetText ( $Title, 'Destination Directory', 'Edit1', $InstPath )
	Send ( '{ENTER}' )
	WinWait ( $Title, 'FolderView' )
	WinClose ( $Title, 'FolderView' )
	WinWait ( 'Password', 'Password' )
	WinActivate ( 'Password', 'Password' )
	WinWaitActive ( 'Password', 'Password' )
	;проверка на случай переустановки
	If ControlCommand ( 'Password', 'Password', 'Button4', 'IsEnabled', '' )=1 Then ControlClick ( 'Password', 'Password', 'Button3' )
	;здесь возможны 2 варианта
	If $password<>'' Then
		;Ввести пароль
		ControlSetText ( 'Password', 'Password', "Edit1", $password )
		ControlSetText ( 'Password', 'Password', "Edit2", $password )
	Else
		;Включить NT security [назначить права пользователям можно будет вручную после установки, запустив "Settings for Remote Administrator server" (r_server.exe /setup) -> "Set password..." -> "Permissions"]
		ControlClick ( 'Password', 'Password', 'Button3' )
	EndIf
	Send ( '{ENTER}' )
	WinWaitActive ( 'Confirmation' )
	ControlClick ( 'Confirmation', '', 'Button2' )
EndIf

;установка ручного типа запуска службы Remote Administrator Service (по ум. "Авто")
RegWrite('HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\r_server','Start',"REG_DWORD",0x00000003)

;перенос ярлыков
If StringLower($programgroup)<>'remote administrator v2.2' Then
DirCopy ( @ProgramsCommonDir & '\Remote Administrator v2.2', @ProgramsCommonDir & '\' & $programgroup, 1 )
DirRemove ( @ProgramsCommonDir & '\Remote Administrator v2.2', 1 )
EndIf

;не показывать заставку при старте программы
RegWrite("HKEY_CURRENT_USER\Software\RAdmin\v2.0\Parameters","showbw","REG_BINARY","00000000")

; регистрация (производится только в сл. отсутствия таковой в реестре)
If Not StringIsXDigit ( RegRead("HKEY_LOCAL_MACHINE\SOFTWARE\RAdmin\v1.01\ViewType","Data") ) Then
	If StringIsXDigit ( $serial ) Then
	RegWrite("HKEY_LOCAL_MACHINE\SOFTWARE\RAdmin\v1.01\ViewType","Data","REG_BINARY",$serial)
	ElseIf $serial<>'' Then
		Run ( $InstPath & '\radmin.exe' )
		If $lang='ru' Then
			$win1text='Введите код'
			$win2titl='Регистрация'
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

;отключить иконку в трэе
RegWrite('HKEY_LOCAL_MACHINE\System\RAdmin\v2.0\Server\Parameters','DisableTrayIcon',"REG_BINARY","01000000")

;создать одну запись в адр. книге: компьютер OLD с IP=192.168.0.3
RegWrite("HKEY_CURRENT_USER\Software\RAdmin\v2.0\Clients","2","REG_BINARY","e09304000c0c005000000500000064000000000000000100000000000000010000000100000001000000010000000100000001000000000000000000000000000000000000003139322e3136382e302e3300c8a1a400e2f4d3775100010100f0fd7f00000000f8fbfd7f000000002cc00000acc81200a4bad3772cc000002cc00000c0c8120046bad377a89a53002cc0000000000000d8c812005500d577a89a53002cc00000000000004f4c44000000000003000400c8a1a400e2f4d3775100010100f0fd7f00000000f8fbfd7f000000002cc00000acc81200a4bad3772cc000002cc00000c0c8120046bad377a89a53002cc0000000000000d8c812005500d577a89a53002cc00000000000000000000000000000000023130000000000000200000000000000")

;BlockInput ( 0 )
