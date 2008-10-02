#!/bin/env python

import sys
from PyQt4 import QtCore, QtGui, QtSql

def createConnection():
	db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
	db.setDatabaseName("test.db")		# Safe: ":memory:"
	if not db.open():
		QtGui.QMessageBox.critical(0, QtGui.qApp.tr("Cannot open database"),
			QtGui.qApp.tr("Unable to establish a database connection."),
			QtGui.QMessageBox.Cancle, QtGui.QMessageBox.NoButton)
		return False
	else:
		if (db.tables().indexOf("person") == -1):		# if wanted table not exists - create them
			query = QtSql.QSqlQuery()
			query.exec_("create table person(id int primary key, firstname varchar(20), lastname varchar(20))")
			query.exec_("insert into person values(1, 'Danny', 'Young')")
			query.exec_("insert into person values(2, 'Christine', 'Holand')")
			query.exec_("insert into person values(3, 'Lars', 'Gordon')")
		return True

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	# 1. create connection
	if not createConnection():
		sys.exit(1)
	# 2. create model
	model = QtSql.QSqlTableModel()
	# 3. init model
	model.setTable("person")
#	model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
	model.select()
	model.setHeaderData(0, QtCore.Qt.Horizontal, QtCore.QVariant(QtCore.QObject.tr(model, "ID")))
	model.setHeaderData(1, QtCore.Qt.Horizontal, QtCore.QVariant(QtCore.QObject.tr(model, "First name")))
	model.setHeaderData(2, QtCore.Qt.Horizontal, QtCore.QVariant(QtCore.QObject.tr(model, "Last name")))
	# 4. create view
	view = QtGui.QTableView()
	view.setModel(model)
	view.setWindowTitle(model.tr("Table Model (View 1)"))
	# 5. lets go
	view.show()
	sys.exit(app.exec_())
