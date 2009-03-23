# -*- coding: utf-8 -*-
'''
Common functions
'''

class	ref:
	'''
	Common parent for siple references: id, name, comments
	'''
	def	__init__(self, dbname, mainlistname):
		self.dbname = dbname
		self.mainlistname = mainlistname
		self.listform = var.render.ref_list
		self.editform = var.render.ref_edit
	def	GET(self, view, id = None):
		if (view == 'list'):
			items = var.mydb.select(self.dbname)
			return self.listform(var.root, items, self.dbname, GetMsg())
		elif (view == 'del'):
			t = var.mydb.transaction()
			try:
				n = var.mydb.delete(self.dbname, where='id=%s' % id)
			except:
				t.rollback()
				var.message = 'Error deleting %s' % self.dbname
			else:
				t.commit()
				var.message = '%d %s deleted ok' % (n, self.dbname)
			raise web.seeother(self.mainlistname)
		elif (view == 'edit'):
			item = var.mydb.select(self.dbname, where='id=%s' % id)[0]
			return self.editform(var.root, item, self.dbname, GetMsg())
		else:
			var.message = 'Unknown action'
			raise web.seeother(self.mainlistname)
	def	POST(self, view, id = None):	# list, None | edit, 2
		i = web.input()			# name, comments
		if (view == 'list'):
			if CheckUniq(self.dbname, 'name="%s"' % i.name):
				var.message = "%s w/ same name already exists." % self.dbname
			else:
				t = var.mydb.transaction()
				try:
					n = var.mydb.insert(self.dbname, name=i.name, comments=i.comments)
				except:
					t.rollback()
					var.message = 'Error inserting %s' % self.dbname
				else:
					t.commit()
					var.message = '%d %s added ok' % (n, self.dbname)
		elif (view == 'edit'):
			t = var.mydb.transaction()
			try:
				var.mydb.update(self.dbname, where="id=%s" % id, name=i.name, comments=i.comments)
			except:
				t.rollback()
				var.message = 'Error updating %s' % self.dbname
			else:
				t.commit()
		raise web.seeother(self.mainlistname)

