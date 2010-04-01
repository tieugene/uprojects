# -*- coding: utf-8 -*-

'''
Table UI.
@author TI_Eugene
'''

import	qt, qttable
import propdialog as cp, propitem as pi, onec

class	Table(qttable.QTable):
	'''
	QTable replacement.
	'''
	def	__init__(self):
		qttable.QTable.__init__(self, 0, 0, None, "Table")
		self.__prepareCM()
		self.connect(self, qt.SIGNAL("contextMenuRequested(int,int,const QPoint&)"), self.__ContextMenuProcessor)
	def	__ContextMenuProcessor(self, row, col, point):
		self.__cmRow = row	# row context menu called where
		self.__cmCol = col	# col context menu called where
		self.ContextMenu.popup(point)
	def	__prepareCM(self):
		tmp = (
			("Cut",			self.__cmCut),
			("Copy",		self.__cmCopy),
			("Paste",		self.__cmPaste),
			("Special paste ...",	self.__cmSPaste),
			("Clear",		self.__cmClear),
			None,
			("Insert",		self.__cmInsert),
			("Del",			self.__cmDelete),
			("Clear text",		self.__cmClearText),
			None,
			("Row &height",		self.__cmHeight),
			("Column &width",	self.__cmWidth),
			None,
			("Properties ...",	self.__cmProperties)
		)
		self.ContextMenu = qt.QPopupMenu()
		for i in (tmp):
			if i:
				self.ContextMenu.insertItem(i[0], i[1])
			else:
				self.ContextMenu.insertSeparator()
	def	__cmCut(self):
		pass
	def	__cmCopy(self):
		pass
	def	__cmPaste(self):
		pass
	def	__cmSPaste(self):
		pass
	def	__cmClear(self):
		pass
	def	__cmInsert(self):
		pass
	def	__cmDelete(self):
		pass
	def	__cmClearText(self):
		pass
	def	__cmHeight(self):
		pass
	def	__cmWidth(self):
		pass
	def	__cmProperties(self):
		if ((self.__cmRow < 0) or (self.__cmCol < 0) or (not self.item(self.__cmRow, self.__cmCol))):
			return
		ci = self.item(self.__cmRow, self.__cmCol).coreitem
		cpd = cp.PropDialog("Cell properties")
		self.cp	= cpd.MainListView
		# 1. prepare tmps
		tmp1 = ("Text", "Expression", "Template", "Fixed template")
		tmp2 = ("Auto", "Cut", "Backspace (?)", "Wrap", "Red", "Backspace (?) + Red")
		tmp3 = ("Left", "Right", "Justify", "Center")
		tmp4 = {0:"Top", 0x08:"Bottom", 0x18:"Center"}
		# 2. fill values
		TextItem = pi.PropertyItem(self.cp, None, "Text")
		TextItem.setOpen(True)
		self.after = None
		self.__setItemText(ci.FlagType, TextItem, "Type", tmp1[ci.TextType])
		self.__setItemText(ci.FlagControl, TextItem, "Control", tmp2[ci.TextControl])
		self.__setItemText(ci.FlagText, TextItem, "Contents", qt.QString().fromUtf8(ci.text))
		self.__setItemText(ci.FlagDescription, TextItem, "Description", qt.QString().fromUtf8(ci.desc))
		self.__setItemBool(ci.FlagProtection, TextItem, "Protection", ci.TextProtection)

		AlignItem = pi.PropertyItem(self.cp, TextItem, "Align")
		AlignItem.setOpen(True)
		self.after = None
		self.__setItemText(ci.FlagHAlign, AlignItem, "Horisontal", tmp3[(ci.HAlign & 0x1F)/2])
		self.__setItemText(ci.FlagVAlign, AlignItem, "Vertical", tmp4[ci.VAlign])
		self.__setItemText(ci.Angle, AlignItem, "Angle", str(ci.Angle))
		self.__setItemText(ci.FlagHAlign, AlignItem, "On selected columns", ci.HAlign & 0x20)
	
		FontItem = pi.PropertyItem(self.cp, AlignItem, "Font")
		FontItem.setOpen(True)
		self.after = None
		#pi.PropertyItemText(FontItem, "Name")
		self.__setItemText(ci.FlagFontSize, FontItem, "Size", str(ci.FontSize))
		self.__setItemBool(ci.FlagFontBold, FontItem, "Bold", ci.FontBold == 7)
		self.__setItemBool(ci.FlagFontItalic, FontItem, "Italic", ci.FontItalic)
		self.__setItemBool(ci.FlagFontUnderLine, FontItem, "Underline", ci.FontUnderline)
		self.__setItemColor(ci.FlagFontColor, FontItem, "Color", onec.Color[ci.FontColor])
	
		BorderItem = pi.PropertyItem(self.cp, FontItem, "Border")
		BorderItem.setOpen(True)
		self.after = None
		self.__setItemFrame(ci.FlagBorderLeft, BorderItem, "Left", onec.Frame[ci.FrameLeft])
		self.__setItemFrame(ci.FlagBorderTop, BorderItem, "Top", onec.Frame[ci.FrameTop])
		self.__setItemFrame(ci.FlagBorderRight, BorderItem, "Right", onec.Frame[ci.FrameRight])
		self.__setItemFrame(ci.FlagBorderBottom, BorderItem, "Bottom", onec.Frame[ci.FrameBottom])
		self.__setItemColor(ci.FlagBorderColor, BorderItem, "Color", onec.Color[ci.FrameColor])
	
		PatternItem = pi.PropertyItem(self.cp, BorderItem, "Pattern")
		PatternItem.setOpen(True)
		self.after = None
		self.__setItemColor(ci.FlagBGColor, PatternItem, "Background color", onec.Color[ci.BGColor])
		self.__setItemColor(ci.FlagPatternColor, PatternItem, "Foreground color", onec.Color[ci.PatternColor])
		self.__setItemPattern(ci.FlagPattern, PatternItem, "Style", onec.Pattern[ci.PatternType])
		# 3. Test
		TestItem = pi.PropertyItem(self.cp, PatternItem, "Test")
		tmp = pi.PropertyItemNone(TestItem, None, "Nothing")
		tmp = pi.PropertyItemBool(TestItem, tmp, "Bool.False", False)
		tmp = pi.PropertyItemBool(TestItem, tmp, "Bool.True", True)
		tmp = pi.PropertyItemText(TestItem, tmp, "Text", "Simply the text")
		tmp = pi.PropertyItemColor(TestItem, tmp, "Color.0", onec.Color[0])
		tmp = pi.PropertyItemColor(TestItem, tmp, "Color.1", onec.Color[1])
		tmp = pi.PropertyItemColor(TestItem, tmp, "Color.2", onec.Color[2])
		tmp = pi.PropertyItemColor(TestItem, tmp, "Color.3", onec.Color[3])
		tmp = pi.PropertyItemColor(TestItem, tmp, "Color.4", onec.Color[4])
		tmp = pi.PropertyItemPattern(TestItem, tmp, "Pattern.0", onec.Pattern[0])
		tmp = pi.PropertyItemPattern(TestItem, tmp, "Pattern.1", onec.Pattern[1])
		tmp = pi.PropertyItemPattern(TestItem, tmp, "Pattern.2", onec.Pattern[2])
		tmp = pi.PropertyItemPattern(TestItem, tmp, "Pattern.3", onec.Pattern[3])
		tmp = pi.PropertyItemPattern(TestItem, tmp, "Pattern.4", onec.Pattern[4])
		tmp = pi.PropertyItemFrame(TestItem, tmp, "Frame.0", onec.Frame[0])
		tmp = pi.PropertyItemFrame(TestItem, tmp, "Frame.1", onec.Frame[1])
		tmp = pi.PropertyItemFrame(TestItem, tmp, "Frame.2", onec.Frame[2])
		tmp = pi.PropertyItemFrame(TestItem, tmp, "Frame.3", onec.Frame[3])
		tmp = pi.PropertyItemFrame(TestItem, tmp, "Frame.4", onec.Frame[4])
		tmp = pi.PropertyItemFrame(TestItem, tmp, "Frame.5", onec.Frame[5])
		tmp = pi.PropertyItemFrame(TestItem, tmp, "Frame.6", onec.Frame[6])
		tmp = pi.PropertyItemFrame(TestItem, tmp, "Frame.7", onec.Frame[7])
		tmp = pi.PropertyItemFrame(TestItem, tmp, "Frame.8", onec.Frame[8])
		tmp = pi.PropertyItemFrame(TestItem, tmp, "Frame.9", onec.Frame[9])
		# 4. show
		cpd.exec_loop()
	def	__setItem(self, classtype, flag, parent, name, val):
		if (flag):
			self.after = classtype(parent, self.after, name, val)
		else:
			self.after = pi.PropertyItemNone(parent, self.after, name)
	def	__setItemBool(self, flag, parent, name, val):
		self.__setItem(pi.PropertyItemBool, flag, parent, name, val)
	def	__setItemText(self, flag, parent, name, val):
		self.__setItem(pi.PropertyItemText, flag, parent, name, val)
	def	__setItemColor(self, flag, parent, name, val):
		self.__setItem(pi.PropertyItemColor, flag, parent, name, val)
	def	__setItemPattern(self, flag, parent, name, val):
		self.__setItem(pi.PropertyItemPattern, flag, parent, name, val)
	def	__setItemFrame(self, flag, parent, name, val):
		self.__setItem(pi.PropertyItemFrame, flag, parent, name, val)

class	TableItem(qttable.QTableItem):
	'''
	QTableItem replacement.
	'''
	def	__init__(self, table, coreitem):
		'''
		@param table - Table object, concluding self
		@param coreitem - core object
		'''
		qttable.QTableItem.__init__(self, table, qttable.QTableItem.OnTyping)
		self.coreitem = coreitem

class	LineEdit(qt.QLineEdit):
	'''
	QLioneEdit replacement.
	'''
	def	__init__(self, parent):
		qt.QLineEdit.__init__(self, parent)
	def	contextMenuEvent(self, e):
		e.ignore()
