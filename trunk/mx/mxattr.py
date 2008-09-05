# -*- coding: utf-8 -*-
'''
mxattr.py - Classes to load, handle and save mx-orianted xattrs.
'''

import	datetime, time, xattr

class	MxList():
	'''
	Container for mx-atts
	'''
	def	__init__(self):
		self.data	= {}

	def	loadCfg(self, cp):
		'''
		Load metadata of xattrs from cfg-file
		@param cp:ConfigParser object
		'''
		for sect in cp.sections():
			st, sn = sect.split(".")
			if (st == "b"):
				fld = MxBool(sect)
			elif (st == "se"):
				fld = MxEnum(sect)
			elif (st == "st"):
				fld = MxTree(sect)
			elif (st == "sl"):
				fld = MxString(sect)
			elif (st == "sh"):
				fld = MxHtml(sect)
			elif (st == "sp"):
				fld = MxPlain(sect)
			elif (st.startswith("i") or st.startswith("u")):
				fld = MxInt(sect)
			elif (st == "f"):
				fld = MxFixed(sect)
			elif (st == "d"):
				fld = MxDate(sect)
			elif (st == "t"):
				fld = MxTime(sect)
			elif (st == "dt"):
				fld = MxDateTime(sect)
			elif (st == "g"):
				fld = MxImage(sect)
			elif (st == "x"):
				fld = MxUrl(sect)
			else:
				fld = None
				print "Unknown type: %s" % st
			if (fld):
				fld.loadCfg(sect, cp)
				self.data[fld.Name] = fld
		return self.data

	def	loadData(self, file):
		'''
		Load field from file's xattr.
		@param file:str
		'''
		for a in xattr.listxattr(file):
			aname = a[5:]
			st, sn = aname.split('.')
			if self.data.has_key(sn):
				self.data[sn].loadData(xattr.getxattr(file, a))

	def	askExtra(self, file):
		'''
		Check undefined xattrs of file.
		@param file:str
		@return tuple of xattr names or None
		'''
		retvalue = []
		for i in xattr.listxattr(file):
			if i not in slef.data:
				retvalue.append(i)
		return retvalue

	def	saveData(self, file, delextra = False):
		'''
		Save field to file's xattr.
		@param file:str
		'''
		# 1. get old list
		oldlist = xattr.listxattr(file)
		oldict = {}
		for i in oldlist:
			oldict[i[5:]] = True
		# 2. save need
		for d in self.data.keys():
			fld = self.data[d]
			a = fld.saveData()
			if (a != None):
				xattr.setxattr(file, "user." + fld.ID, a)
				if oldict.has_key(fld.ID):
					del oldict[fld.ID]
		# 3. delete unneeded
		for i in oldict.keys():
			xattr.removexattr(file, i)

class	_Mx():
	'''
	Parent.
	'''
	def	__init__(self, id):
		self.ID		= id
		self.Label		= None
		self.ToolTip	= None
		self.StatusTip	= None
		self.WhatsTip	= None
		self.Mandatory	= False
		self.Mult		= False
		self.Default	= None
		self.data		= None
		self.loaded	= False
		self.Type, self.Name = self.ID.split(".")

	def	_loadOpt(self, cp, sect, name, default = None):
		return cp.get(sect, name) if cp.has_option(sect, name) else default

	def	loadCfg(self, sect, cp):
		'''
		Load metadata from cfg-file.
		@param sect:str section of cfg-file
		@param cp:ConfigParser - subj.
		@return None
		'''
		self.Label		= self._loadOpt(cp, sect, "Label")
		self.ToolTip	= self._loadOpt(cp, sect, "ToolTip")
		self.StatusTip	= self._loadOpt(cp, sect, "StatusTip")
		self.WhatsTip	= self._loadOpt(cp, sect, "WhatsTip")
		self.Mandatory	= cp.getboolean(sect, "Mandatory")	if cp.has_option(sect, "Mandatory")	else False
		self.Mult		= cp.getboolean(sect, "Mult")		if cp.has_option(sect, "Mult")		else False
		self.Default	= self._loadOpt(cp, sect, "Default")

	def	loadData(self, data):
		'''
		@param data:any
		'''
		self.data		= data
		self.loaded	= True

	def	saveData(self):
		return self.data

class	MxBool(_Mx):
	'''
	Boolean.
	'''
	def	loadData(self, data):
		self.data		= bool(data)
		self.loaded	= True

	def	saveData(self):
		return 1 if self.data else 0

class	MxEnum(_Mx):
	'''
	Enum string.
	'''
	def	__init__(self, id):
		_Mx.__init__(self, id)
		self.Values = None

	def	loadCfg(self, sect, cp):
		_Mx.loadCfg(self, sect, cp)
		self.Values	= eval(cp.get(sect, "Values"))		if cp.has_option(sect, "Values")	else None

class	MxTree(_Mx):
	'''
	Tree-like enum.
	'''
	def	__init__(self, id):
		_Mx.__init__(self, id)
		self.Values = None

	def	loadCfg(self, sect, cp):
		_Mx.loadCfg(self, sect, cp)
		self.Values	= eval(cp.get(sect, "Values"))		if cp.has_option(sect, "Values")	else None

class	MxString(_Mx):
	'''
	One-line string.
	'''
	def	__init__(self, id):
		_Mx.__init__(self, id)
		self.Mask	= None

	def	loadCfg(self, sect, cp):
		_Mx.loadCfg(self, sect, cp)
		self.Mask		= self._loadOpt(cp, sect, "Mask")

class	MxHtml(_Mx):
	'''
	Rich (html) text.
	'''

class	MxPlain(_Mx):
	'''
	Plain text.
	'''

class	MxInt(_Mx):
	'''
	Integer.
	'''
	def	__init__(self, id):
		_Mx.__init__(self, id)
		self.Len	= int(self.Type[1:])
		if (self.Type.startswith('i')):
			self.Signed = True
		else:
			self.Signed = False
		self.Type	= 'i'
		self.Min		= None
		self.Max		= None

	def	loadCfg(self, sect, cp):
		_Mx.loadCfg(self, sect, cp)
		self.Min		= self._loadOpt(cp, sect, "Min")
		self.Max		= self._loadOpt(cp, sect, "Max")

	def	loadData(self, data):
		self.data		= int(data) if (self.Len <= 4) else long(data)

	def	saveData(self):
		return str(self.data)

class	MxFixed(_Mx):
	'''
	Fixed decimal.
	'''
	def	__init__(self, id):
		_Mx.__init__(self, id)
		self.Min		= None
		self.Max		= None

	def	loadCfg(self, sect, cp):
		_Mx.loadCfg(self, sect, cp)
		self.Min		= self._loadOpt(cp, sect, "Min")
		self.Max		= self._loadOpt(cp, sect, "Max")

	def	loadData(self, data):
		self.data		= float(data)		# FIXME: double
		self.loaded	= True

	def	saveData(self):
		return str(self.data)

class	MxDate(_Mx):
	'''
	Date.
	'''
	def	__init__(self, id):
		_Mx.__init__(self, id)
		self.Min		= None
		self.Max		= None

	def	loadCfg(self, sect, cp):
		_Mx.loadCfg(self, sect, cp)
		self.Min		= self._loadOpt(cp, sect, "Min")	# FIXME: date
		self.Max		= self._loadOpt(cp, sect, "Max")	# FIXME: date

	def	loadData(self, data):
		self.data		= datetime.date(*time.strptime(data, "%Y-%m-%d")[0:3])
		self.loaded	= True

	def	saveData(self):
		return str(self.data)

class	MxTime(_Mx):
	'''
	Time.
	'''
	def	loadData(self, data):
		self.data		= datetime.time(*time.strptime(data, "%H:%M:%S")[3:6])
		self.loaded	= True

	def	saveData(self):
		return str(self.data)

class	MxDateTime(_Mx):
	'''
	DateTime.
	'''
	def	loadData(self, data):
		self.data		= datetime.datetime(*time.strptime(data, "%Y-%m-%dT%H:%M:%S")[3:6])
		self.loaded	= True

	def	saveData(self):
		return str(self.data)

class	MxImage(_Mx):
	'''
	Image.
	'''

class	MxUrl(_Mx):
	'''
	URL.
	'''
