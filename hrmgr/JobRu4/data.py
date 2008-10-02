# -*- coding: cp1251 -*-
'''
data.py - Data module.
Global constants and variables
'''

DebugLevel = 1

fld = ("Date", "Title", "EmpTy", "Emplyr", "City", "Sex", "Age F", "Age T", "Educat", "Experi", "Emplym", "Salary", "Req", "Duty", "Cond", "ID", "Contac", "Phone", "E-Mail")
sex = (("Не имеет значения", 0), ("Муж", 1), ("Жен", 2))
edu = (("Не имеет значения", 0), ("Учащийся", 1), ("Среднее", 2), ("Среднее специальное", 3), ("Неполное высшее", 4), ("Высшее", 5))
exp = (("Нет", 0), ("1 год", 1), ("2 года", 2), ("3 года", 3), ("4 года", 4), ("5 лет", 5), ("Свыше 5 лет", 6))
emp = (("Любая", 0), ("Полная", 1), ("По совместительству", 2))
sex2i = {}
i2sex = {}
edu2i = {}
i2edu = {}
exp2i = {}
i2exp = {}
ext2i = {}
i2ext = {}

Parser		= None	# HTMLParser
DataBase	= None	# MySQL DB connector
data		= []	# list-of-lists of data
IDs		= {}	# dict of ID:data[#]
UI		= None	# QtApp

EmptyBuffer	= [None, None, "", 0, "", "", 0, 0, 0, 0, 0, 0, 0, "", "", "", "", "", "", 0, 0]

Create_SQL_String = '''
CREATE TABLE main (
	ID		BIGINT	UNSIGNED	NOT NULL	PRIMARY KEY,
	DateTime	DATETIME		NOT NULL,
	Title		VARCHAR(400)		NOT NULL,
	EmployerType	BOOL			NOT NULL,
	Employer	VARCHAR(200)		NULL,
	City		VARCHAR(100)		NULL,
	Sex		BOOL			NULL,
	AgeFrom		TINYINT	UNSIGNED	NULL,
	AgeTo		TINYINT	UNSIGNED	NULL,
	Education	TINYINT	UNSIGNED	NULL,
	Experience	TINYINT	UNSIGNED	NULL,
	Employment	TINYINT	UNSIGNED	NULL,
	Salary		INT	UNSIGNED	NULL,
	Requirements	VARCHAR(1600)		NULL,
	Duty		VARCHAR(1600)		NULL,
	Conditions	VARCHAR(800)		NULL,
	Contact		VARCHAR(50)		NOT NULL,
	Phone		VARCHAR(50)		NOT NULL,
	Email		VARCHAR(50)		NULL,
	New		BOOL			NOT NULL	DEFAULT 1,
	Priority	TINYINT			NOT NULL	DEFAULT 0
	) DEFAULT CHARSET = utf8;
'''

def	__T2D(t):
	'''
	Touple 2 2 x Dict converter
	'''
	d1 = {}
	d2 = {}
	for i in t:
		d1[i[0]] = i[1]	# name 2 int
		d2[i[1]] = i[0]
	return d1, d2

if (len(sex2i.keys()) == 0):
	sex2i, i2sex = __T2D(sex)
	edu2i, i2edu = __T2D(edu)
	exp2i, i2exp = __T2D(exp)
	emp2i, i2emp = __T2D(emp)
