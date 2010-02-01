#cs
----------------------
Приложение: CryptoPro CSP
Версия: 2...2104
Автор: TI_Eugene
----------------------
#ce

Run ('\bin\Accounting\cpcsp2-0-2104.exe')

WinWaitActive ('Установка КриптоПро CSP', 'Вас приветствует программа InstallShield Wizard для КриптоПро CSP')
ControlClick ('Установка КриптоПро CSP','','Button1')

WinWaitActive ('Установка КриптоПро CSP', 'Прочитайте следующий текст.')
ControlClick ('Установка КриптоПро CSP','','Button1')

WinWaitActive ('Установка КриптоПро CSP', 'Конечная папка')
ControlClick ('Установка КриптоПро CSP','','Button1')

WinWaitActive ('Установка КриптоПро CSP', 'Папка назначения:')
ControlClick ('Установка КриптоПро CSP','','Button1')

WinWaitActive ('Установка КриптоПро CSP', 'Программа InstallShield Wizard успешно установила')
ControlClick ('Установка КриптоПро CSP','','Button2')
ControlClick ('Установка КриптоПро CSP','','Button4')


WinWaitActive ('Свойства: КриптоПро CSP')
ControlClick ('Свойства: КриптоПро CSP','','Button2')

WinWaitActive ('Ввод лицензии')
ControlSetText ('Ввод лицензи','','Edit1', 'changethis')
ControlSetText ('Ввод лицензи','','Edit2', 'changethis')
ControlClick ('Ввод лицензии','','Button1')

WinWaitActive ('Свойства: КриптоПро CSP')
ControlClick ('Свойства: КриптоПро CSP','','Button6')
