# -*- coding: utf-8 -*-

'''
Table read module.
Read Table from xml-file and call wanted methods ofobjects to load objects attributes.
@author TI_Eugene
'''

from xml.parsers import expat	# std
import table_core as tc, dialog_core as dc

class Cfg:
	'''
	Main Cfg reader class
	'''
	def __init__(self, fname):
		'''
		Constructor.
		@param fname filename of configuration file
		'''
		self.p = expat.ParserCreate()
		self.p.returns_unicode = 0
		self.p.StartElementHandler = self.start_element
		self.p.EndElementHandler = self.end_element
		self.p.CharacterDataHandler = self.char_data
		self.fname = fname
		self.ClearAll()
	def start_element(self, name, attrs):
		'''
		start tag catcher
		@param name:str - tag name
		@param attrs:hash - dict of tag attributes
		'''
		# 1. Table
		if (name == 'tml'):
			self.ml = tc.tml()
			self.ml.LoadFromXML(attrs)
		elif (name == 'tbl'):
			self.ml.table.LoadFromXML(attrs)
		elif (name == 'fnts'):
			self.qty = attrs.get('qty')
			self.count = 0
		elif (name == 'fnt'):
			if (self.count > self.qty):
				print "Figasse fnt:", self.count
			else:
				v = tc.fnt()
				v.LoadFromXML(attrs)
				self.ml.font.append(v)
				count += 1
		elif (name == 'tblh'):
			self.ml.tableheader.LoadFromXML(attrs)
		elif (name == 'tblf'):
			self.ml.tablefooter.LoadFromXML(attrs)
		elif (name == 'cols'):
			self.qty = attrs.get('qty')
			self.count = 0
		elif (name == 'col'):
			if (self.count > self.qty):
				print "Figasse col:", self.count
			else:
				v = tc.column()
				v.LoadFromXML(attrs)
				self.ml.col.append(v)
				self.count += 1
		elif (name == 'rows'):
			self.qty = attrs.get('qty')
			self.count = 0
		elif (name == 'row'):
			if (self.count > self.qty):
				print "Figasse row:", self.count
			else:
				v = tc.row()
				v.LoadFromXML(attrs)
				self.ml.row.append(v)
				self.count += 1
		elif (name == 'cells'):
			pass
		elif (name == 'cell'):
			if (self.count > self.qty):
				print "Figasse cell:", self.count
			else:
				v = tc.cell()
				v.LoadFromXML(attrs)
				self.ml.cell.append(v)
				self.count += 1
		elif (name == 'objs'):
			self.qty = attrs.get('qty')
			self.count = 0
		elif (	(name == 'objl') or
			(name == 'objr') or
			(name == 'objt') or
			(name == 'objo') or
			(name == 'objp')
			):
			if (self.count > self.qty):
				print "Figasse obj:", self.count
			else:
				if (name == 'objl'):
					v = tc.objl()
				elif (name == 'objr'):
					v = tc.objr()
				elif (name == 'objt'):
					v = tc.objt()
				elif (name == 'objo'):
					v = tc.objo()
				else:	# objp
					v = tc.objp()
				v.LoadFromXML(attrs)
				self.ml.obj.append(v)
				self.count += 1
		elif (name == 'joins'):
			self.qty = attrs.get('qty')
			self.count = 0
		elif (name == 'join'):
			if (self.count > self.qty):
				print "Figasse join:", self.count
			else:
				v = tc.join()
				v.LoadFromXML(attrs)
				self.ml.join.append(v)
				self.count += 1
		elif (name == 'vsecs'):
			self.qty = attrs.get('qty')
			self.count = 0
			self.dir = True
		elif (name == 'hsecs'):
			self.qty = attrs.get('qty')
			self.count = 0
			self.dir = False
		elif (name == 'sec'):
			if (self.count > self.qty):
				print "Figasse sec:", self.count
			else:
				v = tc.section()
				v.LoadFromXML(self.dir, attrs)
				self.ml.sec.append(v)
				self.count += 1
		elif (name == 'vffs'):
			self.qty = attrs.get('qty')
			self.count = 0
			self.dir = True
		elif (name == 'hffs'):
			self.qty = attrs.get('qty')
			self.count = 0
			self.dir = False
		elif (name == 'ff'):
			if (self.count > self.qty):
				print "Figasse ff:", self.count
			else:
				v = tc.formfeed()
				v.LoadFromXML(self.dir, attrs)
				self.ml.ff.append(v)
				self.count += 1
		elif (name == 'names'):
			self.qty = attrs.get('qty')
			self.count = 0
		elif (name == 'name'):
			if (self.count > self.qty):
				print "Figasse name:", self.count
			else:
				v = tc.name()
				v.LoadFromXML(attrs)
				self.ml.name.append(v)
				self.count += 1
		# 2. Dialog
		elif (name == 'dml'):
			self.ml = dc.dml()
		elif (name == 'Frame'):
			self.ml.Frame.LoadFromXML(attrs)
		elif (name == 'lr'):
			v = dc.Layer()
			v.LoadFromXML(attrs)
			self.ml.Layer.append(v)
		elif (name == 'DiaDummy'):
			pass
		elif (name == 'Browser'):
			self.ml.Browser.LoadFromXML(attrs)
		elif (name == 'mcols'):
			pass
		elif (name == 'c_browse'):
			self.ml.MultiLine.LoadFromXML(attrs)
		elif (name == 'fcols'):
			pass
		elif (name == 'f_1CEDIT'):
			v = dc.f_Edit()
			v.LoadFromXML(attrs)
			self.ml.Column.append(v)
		elif (name == 'f_BMASKED'):
			v = dc.f_BMasked()
			v.LoadFromXML(attrs)
			self.ml.Column.append(v)
		elif (name == 'f_STATIC'):
			v = dc.f_Label()
			v.LoadFromXML(attrs)
			self.ml.Column.append(v)
		elif (name == 'Controls'):
			pass
		elif (name == 'c_1CEDIT'):
			v = dc.c_Edit()
			v.LoadFromXML(attrs)
			self.ml.Control.append(v)
		elif (name == 'c_1CGROUPBOX'):
			v = dc.c_GroupBox()
			v.LoadFromXML(attrs)
			self.ml.Control.append(v)
		elif (name == 'c_BMASKED'):
			v = dc.c_BMasked()
			v.LoadFromXML(attrs)
			self.ml.Control.append(v)
		elif (name == 'c_BUTTON'):
			v = dc.c_Button()
			v.LoadFromXML(attrs)
			self.ml.Control.append(v)
		elif (name == 'c_CHECKBOX'):
			v = dc.c_CheckBox()
			v.LoadFromXML(attrs)
			self.ml.Control.append(v)
		elif (name == 'c_COMBOBOX'):
			v = dc.c_ComboBox()
			v.LoadFromXML(attrs)
			self.ml.Control.append(v)
		elif (name == 'c_LISTBOX'):
			v = dc.c_ListBox()
			v.LoadFromXML(attrs)
			self.ml.Control.append(v)
		elif (name == 'c_RADIO'):
			v = dc.c_Radio()
			v.LoadFromXML(attrs)
			self.ml.Control.append(v)
		elif (name == 'c_STATIC'):
			v = dc.c_Label()
			v.LoadFromXML(attrs)
			self.ml.Control.append(v)
		elif (name == 'c_TABLE'):
			v = dc.c_Table()
			v.LoadFromXML(attrs)
			self.ml.Control.append(v)
		elif (name == 'c_Picture'):
			v = dc.c_Picture()
			v.LoadFromXML(attrs)
			self.ml.Control.append(v)
		elif (name == 'c_SysTreeView32'):
			v = dc.c_TreeView()
			v.LoadFromXML(attrs)
			self.ml.Control.append(v)
		elif (name == 'Cnt_Ver'):
			pass
		else:
			print "Unknown entity:", name
	def end_element(self, name):
		'''
		end tag catcher
		@param name tag name
		'''
		pass
	def char_data(self, data):
		'''
		character data catcher
		@param data data themselves - one (!) line per call
		'''
		pass
	def ClearAll(self):
		'''
		Init all private data (B4 parsing).
		'''
		self.err = None
	def Load(self):
		'''
		Load and parse cfg file.
		@return None (if error occurs)
		'''
		self.ClearAll()
		self.f = open(self.fname)
		self.p.ParseFile(self.f)
		self.f.close()
		if self.err:
			return None
		else:
			return self.ml
