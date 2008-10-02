# -*- coding: utf-8 -*-
'''
Database layer. Common.
@author TI_Eugene
'''

import sys, MySQLdb	# std
import data

class DB:
	def	__init__(self):
		self.DB = None
		self.Cursor = None
		self.FieldNames = (
			"ID", "DateTime", "Title", "EmployerType", "Employer",
			"City", "Sex", "AgeFrom", "AgeTo", "Education",
			"Experience", "Employment", "Salary", "Requirements", "Duty",
			"Conditions", "Contact", "Phone", "Email", "New", "Priority")
		self.SQL_Fields = "ID"
		self.SQL_Update = "UPDATE main SET ID = %s"
		for fn in self.FieldNames[1:]:
			self.SQL_Fields += ", %s" % fn
			self.SQL_Update += (", " + fn + " = %s")
		self.SQL_Select = "SELECT " + self.SQL_Fields + " FROM main "
		self.SQL_Insert = "INSERT INTO main (" + self.SQL_Fields + ") VALUES (%s" + 20 * ", %s" + ")"
		self.SQL_Update += " WHERE ID = "
	def Open(self, sname, dname, uname):
		'''
		Open database.
		@param sname DB-server hostname
		@param dname Database name
		@param uname Database user name
		'''
		#print gvar.UIDS_Manager
		if (self.DB == None):
			try:
				self.DB = MySQLdb.connect(host=sname, db=dname)
				self.Cursor = self.DB.cursor()
			except:
				print 'Couldn\'t connect to MySQL server!'
				sys.exit(0)
			self.Cursor.execute("SET NAMES koi8r")
##			self.Cursor.execute("SET CHARACTER SET koi8r")
			self.Cursor.execute("SET collation_connection = 'koi8r_general_ci'")

	def	Exec(self, s, t = None):
		if (t):
			self.Cursor.execute(s, t)
		else:
			self.Cursor.execute(s)

	def	GetOne(self):
		return self.Cursor.fetchone()

	def	GetAll(self):
		return self.Cursor.fetchall()


	def	InsertRecord(self, buffer):
		'''
		Insert a record
		@param buffer:tuple - a record
		'''
		self.Cursor.execute(self.SQL_Insert, buffer)

	def	UpdateRecord(self, buffer):
		'''
		Update a record
		@param buffer:tuple - a record
		UPDATE table SET col_name1=expr1 [, col_name2=expr2 ...] WHERE where_condition]
		'''
		self.Cursor.execute(self.SQL_Update + str(buffer[0]), buffer)

	def	UpdateNewPrio(self, id, n, p):
		'''
		Update a record
		@param buffer:tuple - a record
		UPDATE table SET col_name1=expr1 [, col_name2=expr2 ...] WHERE where_condition]
		'''
		self.Cursor.execute("UPDATE main SET New = %s, Priority = %s WHERE ID = %s", (n, p, id))

	def	KillAll(self):
		self.Cursor.execute("DELETE FROM main")

	def	__CopyTables(self, src, dst):
		self.Cursor.execute("DROP TABLE %s" % dst)
		self.Cursor.execute("CREATE TABLE %s LIKE %s" % (dst, src))
		self.Cursor.execute("INSERT INTO %s (%s) SELECT %s FROM %s" % (dst, self.SQL_Fields, self.SQL_Fields, src))

	def	Backup(self):
		self.__CopyTables("main", "backup")

	def	Restore(self):
		self.__CopyTables("backup", "main")

	def	Close(self):
		'''
		Close database.
		<b>DEPRICATED</b>
		'''
		self.Cursor.close()
