#cs
----------------------
����������: Avira
������: 9.0.0.10
�����: TI_Eugene
----------------------
#ce

Run ('\bin\avira_antivir_personal_ru.9.0.0.13.exe')

WinWaitActive ('Avira AntiVir Personal - Free Antivirus')
ControlClick ('Avira AntiVir Personal - Free Antivirus','','Button1')

WinWait ('��������� Avira AntiVir Personal - Free Antivirus')

WinWaitActive ('Avira AntiVir Personal - Free Antivirus')
ControlClick ('Avira AntiVir Personal - Free Antivirus','','Button2')

WinWaitActive ('Avira AntiVir Personal - Free Antivirus', '������ ���� �����')
ControlClick ('Avira AntiVir Personal - Free Antivirus','','Button2')

WinWaitActive ('Avira AntiVir Personal - Free Antivirus', '������������ ���������� ��� ��������� ������������ ���������� ������������ ��������� Avira AntiVir Personal - Free Antivirus')
ControlClick ('Avira AntiVir Personal - Free Antivirus','','Button1')
ControlClick ('Avira AntiVir Personal - Free Antivirus','','Button3')

WinWaitActive ('Avira AntiVir Personal - Free Antivirus', '����������, ����������� ���� ��������� ������������ Avira AntiVir Personal - Free Antivirus ������ ������� ������� � �� ������������ ������� � ������������ �����.')
ControlClick ('Avira AntiVir Personal - Free Antivirus','','Button2')
ControlClick ('Avira AntiVir Personal - Free Antivirus','','Button5')

WinWaitActive ('Avira AntiVir Personal - Free Antivirus', '�������� ��� ���������')
ControlClick ('Avira AntiVir Personal - Free Antivirus','','Button1')
ControlClick ('Avira AntiVir Personal - Free Antivirus','','Button7')

WinWaitActive ('��������� �������� Avira AntiVir Personal - Free Antivirus')
ControlClick ('��������� �������� Avira AntiVir Personal - Free Antivirus','','Button2')
ControlClick ('��������� �������� Avira AntiVir Personal - Free Antivirus','','Button5')

;WinWait('Avira AntiVir Personal - Free Antivirus', '���������� Avira AntiVir Personal - Free Antivirus ��������� ����������� ��������.')

WinWaitActive ('Avira AntiVir Personal - Free Antivirus', '��������� ���������')
ControlClick ('Avira AntiVir Personal - Free Antivirus','','Button1')
ControlClick ('Avira AntiVir Personal - Free Antivirus','','Button12')


WinWaitActive ('��������� ��������', '��������� Avira AntiVir Personal - Free Antivirus ���������')
ControlClick ('��������� ��������','','Button2')

WinWaitActive ('��������� ��������', 'CfgWizard::���������')
ControlClick ('��������� ��������','','Button6')

WinWaitActive ('��������� ��������', 'CfgWizard::Unwanted')
ControlClick ('��������� ��������','','Button8')

WinWaitActive ('��������� ��������', 'CfgWizard::StartMode')
ControlClick ('��������� ��������','','Button10')

WinWaitActive ('��������� ��������', '�����::Email')
ControlClick ('��������� ��������','','Button1')
ControlClick ('��������� ��������','','Button11')

WinWaitActive ('��������� ��������', 'CfgWizard::Finish')
ControlClick ('��������� ��������','','Button12')


WinWaitActive ('��������� ����������')
ControlClick ('��������� ����������','','Button1')
ControlClick ('��������� ����������','','Button1')
