#cs
----------------------
����������: Acrobat Reader
������: 9.3
�����: TI_Eugene
----------------------
#ce

Run (@ScriptDir & '\AdbeRdr930_ru_RU.exe')

WinWaitNotActive ('Adobe Reader 9.3 - Russian - Setup')

WinWait ('Windows Installer')

WinWaitActive ('Adobe Reader 9.3 - ��������� ���������', '�������� &����� ����������...')
ControlClick ('Adobe Reader 9.3 - ��������� ���������','','Button1')

WinWaitActive ('Adobe Reader 9.3 - ��������� ���������', '������� "����������", ����� ������ ���������.')
ControlClick ('Adobe Reader 9.3 - ��������� ���������','','Button1')

WinWait ('Adobe Reader 9.3 - ��������� ���������', '��������� Adobe Reader 9.3')

WinWaitActive ('Adobe Reader 9.3 - ��������� ���������', '��������� ���������.')
ControlClick ('Adobe Reader 9.3 - ��������� ���������','','Button1')
