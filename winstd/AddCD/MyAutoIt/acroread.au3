#cs
----------------------
Приложение: Acrobat Reader
Версия: 9.3
Автор: TI_Eugene
----------------------
#ce

Run (@ScriptDir & '\AdbeRdr930_ru_RU.exe')

WinWaitNotActive ('Adobe Reader 9.3 - Russian - Setup')

WinWait ('Windows Installer')

WinWaitActive ('Adobe Reader 9.3 - Программа установки', 'Изменить &папку назначения...')
ControlClick ('Adobe Reader 9.3 - Программа установки','','Button1')

WinWaitActive ('Adobe Reader 9.3 - Программа установки', 'Нажмите "Установить", чтобы начать установку.')
ControlClick ('Adobe Reader 9.3 - Программа установки','','Button1')

WinWait ('Adobe Reader 9.3 - Программа установки', 'Установка Adobe Reader 9.3')

WinWaitActive ('Adobe Reader 9.3 - Программа установки', 'Установка завершена.')
ControlClick ('Adobe Reader 9.3 - Программа установки','','Button1')
