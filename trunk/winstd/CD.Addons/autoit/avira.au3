#cs
----------------------
Приложение: Avira
Версия: 9.0.0.10
Автор: TI_Eugene
----------------------
#ce

Run ('\bin\avira_antivir_personal_ru.9.0.0.13.exe')

WinWaitActive ('Avira AntiVir Personal - Free Antivirus')
ControlClick ('Avira AntiVir Personal - Free Antivirus','','Button1')

WinWait ('Установка Avira AntiVir Personal - Free Antivirus')

WinWaitActive ('Avira AntiVir Personal - Free Antivirus')
ControlClick ('Avira AntiVir Personal - Free Antivirus','','Button2')

WinWaitActive ('Avira AntiVir Personal - Free Antivirus', 'Другие виды угроз')
ControlClick ('Avira AntiVir Personal - Free Antivirus','','Button2')

WinWaitActive ('Avira AntiVir Personal - Free Antivirus', 'Лицензионное соглашение для конечного пользователя бесплатной антивирусной программы Avira AntiVir Personal - Free Antivirus')
ControlClick ('Avira AntiVir Personal - Free Antivirus','','Button1')
ControlClick ('Avira AntiVir Personal - Free Antivirus','','Button3')

WinWaitActive ('Avira AntiVir Personal - Free Antivirus', 'Пожалуйста, подтвердите свои намерения использовать Avira AntiVir Personal - Free Antivirus только частным образом и не использовать продукт в коммерческих целях.')
ControlClick ('Avira AntiVir Personal - Free Antivirus','','Button2')
ControlClick ('Avira AntiVir Personal - Free Antivirus','','Button5')

WinWaitActive ('Avira AntiVir Personal - Free Antivirus', 'Выберите тип установки')
ControlClick ('Avira AntiVir Personal - Free Antivirus','','Button1')
ControlClick ('Avira AntiVir Personal - Free Antivirus','','Button7')

WinWaitActive ('Ассистент лицензий Avira AntiVir Personal - Free Antivirus')
ControlClick ('Ассистент лицензий Avira AntiVir Personal - Free Antivirus','','Button2')
ControlClick ('Ассистент лицензий Avira AntiVir Personal - Free Antivirus','','Button5')

;WinWait('Avira AntiVir Personal - Free Antivirus', 'Установщик Avira AntiVir Personal - Free Antivirus выполняет запрошенные операции.')

WinWaitActive ('Avira AntiVir Personal - Free Antivirus', 'Установка завершена')
ControlClick ('Avira AntiVir Personal - Free Antivirus','','Button1')
ControlClick ('Avira AntiVir Personal - Free Antivirus','','Button12')


WinWaitActive ('Ассистент настроек', 'Установка Avira AntiVir Personal - Free Antivirus завершена')
ControlClick ('Ассистент настроек','','Button2')

WinWaitActive ('Ассистент настроек', 'CfgWizard::Эвристика')
ControlClick ('Ассистент настроек','','Button6')

WinWaitActive ('Ассистент настроек', 'CfgWizard::Unwanted')
ControlClick ('Ассистент настроек','','Button8')

WinWaitActive ('Ассистент настроек', 'CfgWizard::StartMode')
ControlClick ('Ассистент настроек','','Button10')

WinWaitActive ('Ассистент настроек', 'Общее::Email')
ControlClick ('Ассистент настроек','','Button1')
ControlClick ('Ассистент настроек','','Button11')

WinWaitActive ('Ассистент настроек', 'CfgWizard::Finish')
ControlClick ('Ассистент настроек','','Button12')


WinWaitActive ('Программа обновлений')
ControlClick ('Программа обновлений','','Button1')
ControlClick ('Программа обновлений','','Button1')
