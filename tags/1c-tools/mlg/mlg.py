#!/bin/env python
'''
MLG format: ";"-separated:
* date:date (yyyymmdd)
* time:time (hh:mm:ss)
* [user:str]
* component (E/C/...)
* eventtype;event/cat:	# нас интересует Sys
	Accs – счета;
	Archive – сохранение/восстановление;
	CJ – журнал расчетов;
	Const – константы;
		ConstWrite
		ConstDel
	CorrProv – корректные проводки;
	Distr – распределенная ИБ;
	Docs – документы;
	Grbgs – общие события;
	Refs – справочники;
	Restruct – конфигурация;
	Sys – сеанс:
		OpenSession (Подключение);0;[НОВЫЙ СЕАНС : ]Компьютер <hostname>[(m)];;
		CloseSession (Отключение);0;;;
	TmplOpers – типовые операции;
	UpDown – выгрузка/загрузка данных;
	Users – другие события;
	UsrDef – пользователи;
* event:str
* category:int
* comments:
* object:
* objimg:

20070110;12:10:55;;E;Sys;OpenSession;0;НОВЫЙ СЕАНС : Компьютер aquarius3(m);;

date	20070110
time	12:10:55
user	
component	E
evttype	Sys
evt	OpenSession
category	0
;НОВЫЙ СЕАНС : Компьютер aquarius3(m);;
'''



def	main(argv):
	f = open(argv[0])
	if (f):
		pass

if	(__name__ == '__main__'):
	main(sys.argv[1:])
