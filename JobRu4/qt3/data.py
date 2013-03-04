# -*- coding: cp1251 -*-
'''
data module.
'''

import db, parser

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

EmptyBuffer	= [None, None, "", 0, "", "", 0, 0, 0, 0, 0, 0, 0, "", "", "", "", "", "", 0, 0]

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
