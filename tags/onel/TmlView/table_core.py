# -*- coding: utf-8 -*-

'''
Table core classes.
@author TI_Eugene
'''

import	qt
import	onec, table_ui as ui

class	params:
	'''
	Common parent for others.
	'''
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML
		@param xmlattr dict w/ xml attributes and their values.
		'''
		self.Flags	= eval('0x' + xmlattrs['flg'] + 'L')		# hex
		self.__SetFlags(self.Flags)
		self.Height		= float(xmlattrs['h'])
		self.Width		= float(xmlattrs['w'])
		self.BGColor		= int(xmlattrs['bgc'])
		self.FontNo		= int(xmlattrs['fnm'])
		self.FontSize		= int(xmlattrs['fsz'])
		self.FontBold		= int(xmlattrs['fb'])
		self.FontItalic		= bool(int(xmlattrs['fi']))
		self.FontUnderline	= bool(int(xmlattrs['fu']))
		self.FontColor		= int(xmlattrs['fc'])
		self.HAlign		= int(xmlattrs['ha'])
		self.VAlign		= int(xmlattrs['va'])
		self.PatternType	= int(xmlattrs['pt'])
		self.PatternColor	= int(xmlattrs['pc'])
		self.FrameLeft		= int(xmlattrs['frl'])
		self.FrameTop		= int(xmlattrs['frt'])
		self.FrameRight		= int(xmlattrs['frr'])
		self.FrameBottom	= int(xmlattrs['frb'])
		self.FrameColor		= int(xmlattrs['frc'])
		self.TextControl	= int(xmlattrs['tc'])
		self.TextType		= int(xmlattrs['tt'])
		self.TextProtection	= bool(int(xmlattrs.get('tp')))	# implied
		self.Unknown0		= int(xmlattrs.get('u0'))			# implied
		self.Angle		= xmlattrs.get('ang')				# ! implied
	def	__SetFlags(self, flag):
		'''
		Set proper flas due to 4-byte flag.
		@param flag 4-byte flag
		'''
		self.FlagFontName	= bool(self.Flags & 0x00000001L)
		self.FlagFontSize	= bool(self.Flags & 0x00000002L)
		self.FlagFontBold	= bool(self.Flags & 0x00000004L)
		self.FlagFontItalic	= bool(self.Flags & 0x00000008L)
		self.FlagFontUnderLine	= bool(self.Flags & 0x00000010L)
		self.FlagBorderLeft	= bool(self.Flags & 0x00000020L)
		self.FlagBorderTop	= bool(self.Flags & 0x00000040L)
		self.FlagBorderRight	= bool(self.Flags & 0x00000080L)
		self.FlagBorderBottom	= bool(self.Flags & 0x00000100L)
		self.FlagBorderColor	= bool(self.Flags & 0x00000200L)
		self.Flag0x0400		= bool(self.Flags & 0x00000400L)
		self.Flag0x0800		= bool(self.Flags & 0x00000800L)
		self.FlagHAlign		= bool(self.Flags & 0x00001000L)
		self.FlagVAlign		= bool(self.Flags & 0x00002000L)
		self.FlagFontColor	= bool(self.Flags & 0x00004000L)
		self.FlagBGColor	= bool(self.Flags & 0x00008000L)
		self.FlagPattern	= bool(self.Flags & 0x00010000L)
		self.FlagPatternColor	= bool(self.Flags & 0x00020000L)
		self.FlagControl	= bool(self.Flags & 0x00040000L)
		self.FlagType		= bool(self.Flags & 0x00080000L)
		self.FlagProtection	= bool(self.Flags & 0x00100000L)
		self.FlagDescription	= bool(self.Flags & 0x40000000L)
		self.FlagText		= bool(self.Flags & 0x80000000L)
	def	FillOutUI(self, uiitem):
		'''
		Fill UI Table object due to loaded data.
		@param uiitem QTable, QTableItem object.
		'''
		if (self.FlagControl):
			if (self.TextControl == 3):		# wrap
				uiitem.setWordWrap(True)
		if (self.FlagHAlign):
			if ((self.HAlign & 0x0F) == 0):	# left
				uiitem.setAlignment(qt.Qt.AlignLeft)
			if ((self.HAlign & 0x0F) == 2):	# right
				uiitem.setAlignment(qt.Qt.AlignRight)
			if ((self.HAlign & 0x0F) == 4):	# width
				uiitem.setAlignment(qt.Qt.AlignJustify)
			if ((self.HAlign & 0x0F) == 6):	# center
				uiitem.setAlignment(qt.Qt.AlignHCenter)
		#if (self.FlagPattern):
			#uitbl...setPixmap(...)
		if (self.FlagBGColor):
			c = onec.Color[self.BGColor]
			uiitem.setPaletteBackgroundColor(qt.QColor(c[0], c[1], c[2]))
		if (self.FlagFontColor):
			c = onec.Color[self.FontColor]
			uiitem.setPaletteForegroundColor(qt.QColor(c[0], c[1], c[2]))
		# <font>
		fontchanged = False
		font = uiitem.font()
		if ((self.FlagFontSize) and (self.FontSize)):
			font.setPointSize(self.FontSize)
			fontchanged = True
		if (self.FlagFontBold and self.FontBold):
			font.setBold(bool(self.FontBold == 7))
			fontchanged = True
		if (self.FlagFontItalic):
			font.setItalic(bool(self.FontItalic))
			fontchanged = True
		if (self.FlagFontUnderLine):
			font.setItalic(bool(self.FontUnderline))
			fontchanged = True
		if (fontchanged):
			uiitem.setFont(font)
		# </font>
		if (self.FlagPattern):
			uiitem.setPaletteBackgroundPixmap(qt.QPixmap(onec.Pattern[self.PatternType]))
class	extparams(params):
	'''
	Extended parent for others.
	'''
	def	LoadFromXML(self, xmlattrs):
		params.LoadFromXML(self, xmlattrs)
		self.text = xmlattrs.get('txt')
		self.desc = xmlattrs.get('dsc')
	def	FillOutUI(self, uiitem):
		'''
		Fill UI Table object due to loaded data.
		@param uiitem QTable, QTableItem object.
		'''
		params.FillOutUI(self, uiitem)
		if (self.text and self.FlagText):
			uiitem.setText(qt.QString().fromUtf8(self.text))
#====
class	tml:
	'''
	Table ownself.
	'''
	def	__init__(self):
		self.Type = 1	# it's Table
		self.font = []
		self.table = table()
		self.tableheader = theader()
		self.tablefooter = tfooter()
		self.col = []
		self.row = []
		self.cell = []
		self.obj = []
		self.join = []
		self.sec = []
		self.ff = []
		self.name = []
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML attrs as attributes dict.
		@param xmlattrs dict of attrname:attrvalue
		'''
		#self.u0	= xmlattrs['u0']		# 00 00 00 00 00 - fixed
		#self.version	= int(xmlattrs['ver'])
		self.colqty	= int(xmlattrs['cqty'])
		self.rowqty	= int(xmlattrs['rqty'])
		self.objqty	= int(xmlattrs['oqty'])
		self.u1		= xmlattrs.get('u1')	# implied
	def	FillOutUI(self, uitbl):
		'''
		Fill UI Table object due to loaded data.
		@param uitbl QTable object.
		@note Don't set Table, Column and Row properties. Instead we set Cell properties in that order: by Table, Column, Row and Cell ownself.
		'''
		uitbl.setNumCols(self.colqty)
		uitbl.setNumRows(self.rowqty)
		# set header and left side
		#for i in xrange(self.colqty):
			#uitbl.horizontalHeader().setLabel(i, str(i+1))
		#self.table.FillOutUI(uitbl);
		for i in self.col:
			i.FillOutUI(uitbl)
		for i in self.row:
			i.FillOutUI(uitbl)
		for i in self.cell:
			i.FillOutUI(uitbl)
		for i in self.join:
			i.FillOutUI(uitbl)
		# misc experiences
		self.left = uitbl.verticalHeader()
		#print "VHeader: count =", self.left.count()
		#self.left.removeLabel(2)
		#self.left.resizeSection(2, 50) - like row.height
		#l = qt.QLabel(qt.QString("tratata"), self.left)

class	font:
	'''
	Font description.
	'''
	def	LoadFromXML(self, xmlattrs):
		self.no			= int(xmlattrs['n'])
		self.Height		= int(xmlattrs['h'])
		self.Width		= int(xmlattrs['w'])
		self.Escapement		= int(xmlattrs['esc'])
		#self.Direction		= int(xmlattrs['dir'])	# 0 - fixed
		self.Weight		= int(xmlattrs['b'])
		self.Italic		= int(xmlattrs['i'])
		self.Underline		= int(xmlattrs['u'])
		self.StrikeOut		= int(xmlattrs['so'])
		self.CodePage		= int(xmlattrs['cp'])
		self.OutPrecision	= int(xmlattrs['opr'])
		self.ClipPrecision	= int(xmlattrs['cpr'])
		self.PitchAndFamily	= int(xmlattrs['pf'])
		self.FontName		= xmlattrs['fnm']
		self.Trash		= xmlattrs['tsh']

class	table(params):
	'''
	Common table parameters.
	'''
	def	LoadFromXML(self, xmlattrs):
		params.LoadFromXML(self, xmlattrs);
	def	FillOutUI(self, uitbl):
		'''
		Fill UI Table object due to loaded data.
		@param uitbl QTable object.
		'''
		#params.FillOutUI(self, uitbl)
class	theader(extparams):
	'''
	Table header properties.
	'''
	def	LoadFromXML(self, xmlattrs):
		extparams.LoadFromXML(self, xmlattrs);
	def	FillOutUI(self, uitbl):
		'''
		Fill UI Table object due to loaded data.
		@param uitbl QTable object.
		'''
		extparams.FillOutUI(self, uitbl)
class	tfooter(extparams):
	'''
	Table footer properties.
	'''
	def	LoadFromXML(self, xmlattrs):
		extparams.LoadFromXML(self, xmlattrs);
	def	FillOutUI(self, uitbl):
		'''
		Fill UI Table object due to loaded data.
		@param uitbl QTable object.
		'''
		extparams.FillOutUI(self, uitbl)
class	column(extparams):
	'''
	Column properties.
	'''
	def	LoadFromXML(self, xmlattrs):
		extparams.LoadFromXML(self, xmlattrs);
		self.col	= int(xmlattrs['n'])
	def	FillOutUI(self, uitbl):
		'''
		Fill UI Table object due to loaded data.
		@param uitbl QTable object.
		'''
		#extparams.FillOutUI(self, uitbl)
		if (self.Width):
			uitbl.setColumnWidth(self.col, self.Width * 7)
class	row(params):
	'''
	Row properties.
	'''
	def	LoadFromXML(self, xmlattrs):
		params.LoadFromXML(self, xmlattrs);
		self.row	= int(xmlattrs['n'])
	def	FillOutUI(self, uitbl):
		'''
		Fill UI Table object due to loaded data.
		@param uitbl QTable object.
		'''
		#params.FillOutUI(self, uitbl)
		if (self.Height):
			uitbl.setRowHeight(self.row, self.Height * 4.0/3.0)	# 11.25 == 15 px
class	cell(extparams):
	'''
	Cell properties.
	'''
	def	LoadFromXML(self, xmlattrs):
		extparams.LoadFromXML(self, xmlattrs);
		self.row	= int(xmlattrs['r'])
		self.col	= int(xmlattrs['c'])
	def	FillOutUI(self, uitbl):
		'''
		Fill UI Table object due to loaded data.
		@param uitbl QTable object.
		'''
		tmp = ui.TableItem(uitbl, self)
		uitbl.setItem(self.row, self.col, tmp)	# for Span
		self.uiitem = ui.LineEdit(uitbl)
		self.uiitem.setFrame(False)
		uitbl.setCellWidget(self.row, self.col, self.uiitem)
		# TODO: B4 this check props of Table, Column and Row
		extparams.FillOutUI(self, self.uiitem)
class	Object(params):
	'''
	Object parent class
	'''
	def	LoadFromXML(self, xmlattrs):
		self.type	= int(xmlattrs['typ'])
		#params.FillOutUI(self, self.uiitem)
		self.col0	= int(xmlattrs['c0'])
		self.row0	= int(xmlattrs['r0'])
		self.x0		= int(xmlattrs['x0'])
		self.y0		= int(xmlattrs['y0'])
		self.col1	= int(xmlattrs['c1'])
		self.row1	= int(xmlattrs['r1'])
		self.x1		= int(xmlattrs['x1'])
		self.y1		= int(xmlattrs['y1'])
		self.level	= int(xmlattrs['lvl'])
class	ObjectL(Object):
	'''
	Object 'Line' properties.
	'''
	def	LoadFromXML(self, xmlattrs):
		Object.LoadFromXML(self, xmlattrs)
class	ObjectR(Object):
	'''
	Object 'Rectangle' properties.
	'''
	def	LoadFromXML(self, xmlattrs):
		Object.LoadFromXML(self, xmlattrs)
class	ObjectT(Object):
	'''
	Object 'Text Frame' properties.
	'''
	def	LoadFromXML(self, xmlattrs):
		Object.LoadFromXML(self, xmlattrs)
class	ObjectO(Object):
	'''
	Object 'OLE|Diagram' properties.
	'''
	def	LoadFromXML(self, xmlattrs):
		Object.LoadFromXML(self, xmlattrs)
class	ObjectP(Object):
	'''
	Object 'Picture' properties.
	'''
	def	LoadFromXML(self, xmlattrs):
		Object.LoadFromXML(self, xmlattrs)
class	join(params):
	'''
	Multicell join properties.
	'''
	def	LoadFromXML(self, xmlattrs):
		self.col0	= int(xmlattrs['c0'])
		self.row0	= int(xmlattrs['r0'])
		self.col1	= int(xmlattrs['c1'])
		self.row1	= int(xmlattrs['r1'])
	def	FillOutUI(self, uitbl):
		'''
		Fill UI Table object due to loaded data.
		@param uitbl QTable object.
		'''
		uitbl.item(self.row0, self.col0).setSpan(self.row1 - self.row0 + 1, self.col1 - self.col0 + 1)
class	section(params):
	'''
	Section properties.
	'''
	def	LoadFromXML(self, dir, xmlattrs):
		'''
		@param dir bool True == vertical, false = horisontal
		'''
		self.direction		= dir
		self.begin		= int(xmlattrs['b'])
		self.end		= int(xmlattrs['e'])
		self.parent		= int(xmlattrs['p'])
		self.unknown0		= int(xmlattrs['u0'])
		self.name		= xmlattrs['nm']
class	formfeed(params):
	'''
	FormFeed properties.
	'''
	def	LoadFromXML(self, dir, xmlattrs):
		'''
		@param dir bool True == vertical, false = horisontal
		'''
		self.direction	= dir
		self.n		= int(xmlattrs['n'])
class	name(params):
	'''
	Named region properties.
	'''
	def	LoadFromXML(self, xmlattrs):
		self.name		= xmlattrs['nm']
		self.unknow0		= int(xmlattrs['u0'])
		self.unknow1		= xmlattrs['u1']
		self.unknow2		= int(xmlattrs['u2'])
		self.col0		= int(xmlattrs['c0'])
		self.row0		= int(xmlattrs['r0'])
		self.col1		= int(xmlattrs['c1'])
		self.row1		= int(xmlattrs['r1'])
