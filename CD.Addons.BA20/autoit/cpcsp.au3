#cs
----------------------
����������: CryptoPro CSP
������: 2...2104
�����: TI_Eugene
----------------------
#ce

Run ('\bin\Accounting\cpcsp2-0-2104.exe')

WinWaitActive ('��������� ��������� CSP', '��� ������������ ��������� InstallShield Wizard ��� ��������� CSP')
ControlClick ('��������� ��������� CSP','','Button1')

WinWaitActive ('��������� ��������� CSP', '���������� ��������� �����.')
ControlClick ('��������� ��������� CSP','','Button1')

WinWaitActive ('��������� ��������� CSP', '�������� �����')
ControlClick ('��������� ��������� CSP','','Button1')

WinWaitActive ('��������� ��������� CSP', '����� ����������:')
ControlClick ('��������� ��������� CSP','','Button1')

WinWaitActive ('��������� ��������� CSP', '��������� InstallShield Wizard ������� ����������')
ControlClick ('��������� ��������� CSP','','Button2')
ControlClick ('��������� ��������� CSP','','Button4')


WinWaitActive ('��������: ��������� CSP')
ControlClick ('��������: ��������� CSP','','Button2')

WinWaitActive ('���� ��������')
ControlSetText ('���� �������','','Edit1', 'changethis')
ControlSetText ('���� �������','','Edit2', 'changethis')
ControlClick ('���� ��������','','Button1')

WinWaitActive ('��������: ��������� CSP')
ControlClick ('��������: ��������� CSP','','Button6')
