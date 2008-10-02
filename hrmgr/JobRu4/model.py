# -*- coding: utf-8 -*-
'''
model.py - data model.
'''

from PyQt4 import QtCore, QtSql, QtGui
import data

class	CustomDelegate(QtGui.QItemDelegate):
	def __init__(self, parent=None):
		QtGui.QItemDelegate.__init__(self, parent)
		self.__IconSex = (
			QtGui.QPixmap("icons/any.png"),
			QtGui.QPixmap("icons/male.png"),
			QtGui.QPixmap("icons/female.png"))
		self.__IconET = (
			QtGui.QPixmap("icons/any.png"),
			QtGui.QPixmap("icons/half.png"),
			QtGui.QPixmap("icons/female.png"))
	def	paint(self, painter, option, index):
		if index.column() == 6:
			i = index.model().data(index).toInt()[0]
			if (i):
				painter.drawPixmap(option.rect.topLeft(), self.__IconSex[i])
		elif index.column() == 11:
			i = index.model().data(index).toInt()[0]
			if (i):
				painter.drawPixmap(option.rect.topLeft(), self.__IconET[i])
		else:
			QtGui.QItemDelegate.paint(self, painter, option, index)

class	CustomModel(QtSql.QSqlTableModel):
	def __init__(self, parent = None, db = QtSql.QSqlDatabase()):
		QtSql.QSqlTableModel.__init__(self, parent, db)
		self.__value_exp = ("", "1", "2", "3", "4", "5", "5+")
	def data(self, index, role = QtCore.Qt.DisplayRole):
		value = QtSql.QSqlTableModel.data(self, index, role)
		if (value.isValid()):
			if (role == QtCore.Qt.DisplayRole):
				col = index.column()
				if (col == 10):
					value = QtCore.QVariant(self.__value_exp[value.toInt()[0]])
##				elif (col == 2):
##					value = QtCore.QVariant(value.toDateTime())	# value.toDateTime().toString("yy/MM hh:mm")
				elif (	# drop "0"s
					(col == 7) or
					(col == 8) or
					(col == 9) or
					(col == 12) or
					(col == 19)):
					if (not value.toInt()[0]):
						value = QtCore.QVariant()
##			elif (role == QtCore.Qt.TextColorRole):
##				if index.column() == 1:
##					value = QtCore.QVariant(QtGui.QColor(QtCore.Qt.blue))
##			if (role == QtCore.Qt.DecorationRole):
##				if index.column() == 6:
##					print "role:", role
##					#value = QtCore.QVariant(self.__IconFemale)
		return value

def	CreateModel():
	model = CustomModel()
	model.setTable("main")
	model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
	model.select()
	hs = (None, None, None, "ET", None, None, "S", "AF", "AT", "Edu", "Exp", "Emp", "Sal", None, None, None, None, None, None, None, "Pri")
	for i, h in enumerate(hs):
		if h:
			model.setHeaderData(i, QtCore.Qt.Horizontal, QtCore.QVariant(QtCore.QObject.tr(model, h)))
	#model.setHeaderData(1, QtCore.Qt.Horizontal, QtCore.QVariant(QtCore.QObject.tr(model, "First name")))
	return model

def	BeginMassAdd(mod):
	'''
	Begin massive record add.
	@param mod:QAbstractModel - model.
	'''
	pass
	#mod.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)

def	CommitMassAdd(mod):
	'''
	Commit massive record add.
	@param mod:QAbstractModel - model.
	'''
	return mod.submitAll()
	#mod.setEditStrategy(QtSql.QSqlTableModel.OnRowChange)

def	RollbackMassAdd(mod):
	'''
	Rollback massive record add.
	@param mod:QAbstractModel - model.
	'''
	return mod.revertAll()
	#mod.setEditStrategy(QtSql.QSqlTableModel.OnRowChange)

def	DeleteAll(mod):
	'''
	Delete all records from DB.
	@param mod:QAbstractModel - model.
	'''
	mod.removeRows(0, mod.rowCount(QtCore.QModelIndex()), QtCore.QModelIndex())
	mod.submitAll()

def	AddRecord(mod, rec, mode = False):
	'''
	Add new record into DB.
	If mode == True - check exist. If not - add, if yes - replace (if newer) or not.
	@param mod:QAbstractModel - model.
	@param rec:list - one record as list.
	@param mode:bool - mode of addition; False - add, True - check and add or replace
	'''
	# search
	recs = mod.match(mod.index(0, 0), QtCore.Qt.DisplayRole, QtCore.QVariant(rec[0]), 1, QtCore.Qt.MatchExactly)
	if (len(recs) > 0):		# found => QModelIndex[]
		row = recs[0].row()
		if (rec[1] <= mod.data(mod.index(row, 1)).toDateTime()):	# found, but duplicated
			return True
	else:
		row = -1
	qsr = mod.record()
	for i, r in enumerate(rec):
		qsr.setValue(i, QtCore.QVariant(r))
	if not mod.insertRecord(row, qsr):
		print mod.lastError().text()
		retvalue = False
	else:
		retvalue = True
	return retvalue
