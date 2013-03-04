# -*- coding: utf-8 -*-

'''
Dialog core classes.
@author TI_Eugene
'''

import	qt, qttable
import	onec, dialog_ui as ui

class	gfx:
	# funcs to recalc 1C:Coordinates into px values
	def	__XCoord(self, src, a, b, c, d):
		if (src > 0):
			dst = int((src + a) * b / c + d)
		else:
			dst = 0
		return dst
	def	_XCoord_X(self, src):
		return self.__XCoord(src,  -2, 20, 13, 0)
	def	_XCoord_Y(self, src):
		#return self.__XCoord(src, -18,  5,  3)
		return self.__XCoord(src,   0,  7,  4, -20)
	def	_XCoord_W(self, src):
		return self.__XCoord(src,   0, 20, 13, 0)	# but if - > ret 1
	def	_XCoord_H(self, src):
		#return self.__XCoord(src,   0,  5,  3)		# but if - > ret 1
		return self.__XCoord(src,   0,  7,  4, 0)	# but if - > ret 1

class	ctrl(gfx):
	'''
	Common parent for controls.
	'''
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML
		@param xmlattr dict w/ xml attributes and their values.
		'''
		self.No		= int(xmlattrs['no'])
		self.Unknown00	= int(xmlattrs['u00'])
		self.X		= int(xmlattrs['x'])
		self.Y		= int(xmlattrs['y'])
		self.Width	= int(xmlattrs['w'])
		self.Height	= int(xmlattrs['h'])
		self.TabNo	= int(xmlattrs['tn'])
		self.FontName	= xmlattrs['fn']
		self.Layer	= xmlattrs['lr']
	def	FillOutUI(self):
		'''
		Fill UI Dialog object due to loaded data.
		@param uiitem QDialog object.
		'''
		self.uiitem.setGeometry(self._XCoord_X(self.X), self._XCoord_Y(self.Y), self._XCoord_W(self.Width), self._XCoord_H(self.Height))

class	col:
	'''
	Common parent for column controls.
	'''
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML
		@param xmlattr dict w/ xml attributes and their values.
		'''
		self.No			= int(xmlattrs['no'])
		self.Caption		= xmlattrs['cap']
		self.Width		= int(xmlattrs['w'])
		self.TabNo		= int(xmlattrs['tn'])
		self.Formula		= xmlattrs['fm']
		self.ID			= xmlattrs['id']
		self.RqUID		= int(xmlattrs['rid'])
		self.ValueLen		= int(xmlattrs['vln'])
		self.Unknown1		= int(xmlattrs['u1'])
		self.Unknown2		= xmlattrs['u2']
		self.Flag		= int(xmlattrs['flg'])
		self.ShortTip		= xmlattrs['stp']
		self.Type		= int(xmlattrs['typ'])
		self.ValueType		= xmlattrs['vtp']
		self.ValuePrecision	= int(xmlattrs['vpr'])
		self.FlagPT		= int(xmlattrs['pt'])
		self.HeadAlign		= int(xmlattrs['aln'])
		self.Masque		= xmlattrs['msq']
		self.Unknown3		= xmlattrs.get('u3')	# ! implied
	def	FillOutUI(self, uiitem):
		'''
		Common column settings.
		'''
		self.Column = uiitem.numCols()
		uiitem.setNumCols(self.Column + 1)
		uiitem.horizontalHeader().setLabel(self.Column, qt.QString().fromUtf8(self.Caption))
		uiitem.setColumnWidth(self.Column, self.Width)
# -----	now controls themselvs -----
class	dml:
	'''
	Dialog themself.
	XML entity: dml
	'''
	def	__init__(self):
		self.Type = 2	# it's Dialog
		self.Frame = Frame()
		self.Layer = []
		self.Browser = Browser()
		self.MultiLine = MultiLine()
		self.Column = []
		self.Control = []
	def	FillOutUI(self, uiitem):
		'''
		Fill UI Dialog object due to loaded data.
		@param uiitem QDialog object.
		'''
		self.uiitem = uiitem
		self.Frame.FillOutUI(self.uiitem)
		for i in self.Control:
			i.FillOutUI(self.uiitem)
		self.MultiLine.FillOutUI(self.uiitem)
		for i in self.Column:
			i.FillOutUI(self.MultiLine.uiitem)

class	Frame(gfx):
	'''
	XML entity: Frame
	'''
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML
		@param xmlattr dict w/ xml attributes and their values.
		'''
		self.FontSize		= int(xmlattrs['fs'])
		self.FontBold		= int(xmlattrs['fb'])
		self.FontItalic		= bool(int(xmlattrs['fi']))
		self.FontUndeline	= bool(int(xmlattrs['fu']))
		self.Unknown05		= int(xmlattrs['u05'])
		self.Unknown08		= int(xmlattrs['u08'])
		self.FontName		= xmlattrs['fn']
		self.Width		= int(xmlattrs['w'])
		self.Height		= int(xmlattrs['h'])
		self.Caption		= xmlattrs['cap']
		self.SavingMode		= int(xmlattrs['sm'])
		self.FontDefault	= bool(int(xmlattrs['fd']))
		self.AutoTab		= bool(int(xmlattrs['at']))
		self.Unknown13		= int(xmlattrs['u13'])
		self.BGColor		= int(xmlattrs['bc'])
		self.PicNo		= int(xmlattrs['pic'])
		self.SM1		= int(xmlattrs['sm1'])
		self.ActiveLayer	= int(xmlattrs['al'])
		self.IsToolBar		= bool(xmlattrs.get('stb'))	# ! implied
		self.Sizable		= bool(xmlattrs.get('szbl'))	# ! implied
	def	FillOutUI(self, uiitem):
		'''
		Fill UI Dialog object due to loaded data.
		@param uiitem QDialog object.
		'''
		uiitem.setCaption(qt.QString().fromUtf8(self.Caption))
		uiitem.resize(self._XCoord_W(self.Width), self._XCoord_H(self.Height) - 25)
class	Layer:
	'''
	XML entity: lr
	'''
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML
		@param xmlattr dict w/ xml attributes and their values.
		'''
		self.No		= int(xmlattrs['no'])
		self.ID		= xmlattrs['id']
		self.Visible	= bool(int(xmlattrs['v']))
class	Browser:
	'''
	XML entity: Browser
	'''
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML
		@param xmlattr dict w/ xml attributes and their values.
		'''
		self.Unknown0	= int(xmlattrs['u0'])
		self.Unknown1	= int(xmlattrs['u1'])
class	MultiLine(ctrl):
	'''
	Multiline part of Dialog.
	XML entity: c_browse
	'''
	def	__init__(self):
		self._defined = False	# flag of multiline part defined
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML
		@param xmlattr dict w/ xml attributes and their values.
		'''
		ctrl.LoadFromXML(self, xmlattrs)
		self.Formula		= xmlattrs['fm']
		self.ID			= xmlattrs['id']
		self.RqUID		= int(xmlattrs['rid'])
		self.ValueType		= xmlattrs['vtp']
		self.ValueLen		= int(xmlattrs['vln'])
		self.ValuePrecision	= int(xmlattrs['vpr'])
		self.TypeUID		= xmlattrs.get('uref')	# implied
		self.FlagPT		= int(xmlattrs['pt'])
		self.Flag		= int(xmlattrs['flg'])
		self.PicID		= int(xmlattrs['pid'])
		self.HotKeyMeta		= xmlattrs.get('hkm')	# implied
		self.HotKeyScanCode	= xmlattrs.get('hks')	# implied
		self._defined = True
	def	FillOutUI(self, uiitem):
		'''
		Fill UI Dialog object due to loaded data.
		@param uiitem QDialog object.
		'''
		self.uiitem = qttable.QTable(uiitem)
		self.uiitem.setLeftMargin(0)
		ctrl.FillOutUI(self)
class	f_Edit(col):
	'''
	XML entity: f_1CEDIT
	'''
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML
		@param xmlattr dict w/ xml attributes and their values.
		'''
		col.LoadFromXML(self, xmlattrs)
##	def	FillOutUI(self, uiitem):
##		'''
##		Fill UI Dialog's multiline part due to loaded data.
##		@param uiitem QTable object.
##		'''
##		col.FillOutUI(self)
class	f_BMasked(col):
	'''
	XML entity: f_BMASKED
	'''
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML
		@param xmlattr dict w/ xml attributes and their values.
		'''
		col.LoadFromXML(self, xmlattrs)
		self.TypeUID		= xmlattrs.get('uref')	# ! implied
##	def	FillOutUI(self, uiitem):
##		'''
##		Fill UI Dialog's multiline part due to loaded data.
##		@param uiitem QTable object.
##		'''
##		col.FillOutUI(self)
class	f_Label(col):
	'''
	XML entity: f_STATIC
	'''
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML
		@param xmlattr dict w/ xml attributes and their values.
		'''
		col.LoadFromXML(self, xmlattrs)
##	def	FillOutUI(self, uiitem):
##		'''
##		Fill UI Dialog's multiline part due to loaded data.
##		@param uiitem QTable object.
##		'''
##		col.FillOutUI(self)
class	c_Edit(ctrl):
	'''
	Common parent for column controls.
	'''
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML
		@param xmlattr dict w/ xml attributes and their values.
		'''
		ctrl.LoadFromXML(self, xmlattrs)
		self.Caption		= xmlattrs['cap']
		self.Linked		= bool(int(xmlattrs['rq']))
		self.Formula		= xmlattrs['fm']
		self.ID			= xmlattrs['id']
		self.RqUID		= xmlattrs['rid']
		self.ValueType		= xmlattrs['vtp']
		self.ValueLen		= int(xmlattrs['vln'])
		self.ValuePrecision	= int(xmlattrs['vpr'])
		self.TypeUID		= xmlattrs.get('uref')	# ! implied
		self.FlagPT		= int(xmlattrs['pt'])
		self.Flag		= int(xmlattrs['flg'])
		self.Masque		= xmlattrs['msq']
		self.ShortTip		= xmlattrs['stp']
		self.FontSize		= bool(int(xmlattrs['fs']))
		self.FontBold		= bool(int(xmlattrs['fb']))
##		self.FontItalic		= bool(int(xmlattrs['fi']))
##		self.FontUndeline	= bool(int(xmlattrs['fu']))
		self.Unknown08		= int(xmlattrs['u08'])
		self.Unknown09		= int(xmlattrs['u09'])
		self.Unknown10		= int(xmlattrs['u10'])
		self.Unknown11		= int(xmlattrs['u11'])
		self.Unknown12		= int(xmlattrs['u12'])
		self.FontColor		= int(xmlattrs['fc'])
##		self.PicID		= int(xmlattrs['pid'])
##		self.HotKeyMeta		= int(xmlattrs['hkm'])
##		self.HotKeyScanCode	= int(xmlattrs['hks'])
	def	FillOutUI(self, uiitem):
		'''
		Fill UI Dialog object due to loaded data.
		@param uiitem QDialog object.
		'''
		self.uiitem = qt.QLineEdit(uiitem)
		self.uiitem.setCaption(qt.QString().fromUtf8(self.Caption))
		ctrl.FillOutUI(self)
class	c_GroupBox(ctrl):
	'''
	Common parent for column controls.
	'''
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML
		@param xmlattr dict w/ xml attributes and their values.
		'''
		ctrl.LoadFromXML(self, xmlattrs)
		self.Caption		= xmlattrs['cap']
##		self.Linked		= bool(int(xmlattrs['rq']))
##		self.Formula		= xmlattrs['fm']
		self.ID			= xmlattrs['id']
		self.RqUID		= xmlattrs['rid']
##		self.ValueType		= xmlattrs['vtp']
##		self.ValueLen		= int(xmlattrs['vln'])
##		self.ValuePrecision	= int(xmlattrs['vpr'])
##		self.TypeUID		= xmlattrs.get('uref')	# ! implied
##		self.FlagPT		= int(xmlattrs['pt'])
		self.Flag		= int(xmlattrs['flg'])
##		self.Masque		= xmlattrs['msq']
##		self.ShortTip		= xmlattrs['stp']
##		self.FontSize		= bool(int(xmlattrs['fs']))
##		self.FontBold		= bool(int(xmlattrs['fb']))
##		self.FontItalic		= bool(int(xmlattrs['fi']))
##		self.FontUndeline	= bool(int(xmlattrs['fu']))
##		self.Unknown08		= int(xmlattrs['u08'])
##		self.Unknown09		= int(xmlattrs['u09'])
##		self.Unknown10		= int(xmlattrs['u10'])
##		self.Unknown11		= int(xmlattrs['u11'])
##		self.Unknown12		= int(xmlattrs['u12'])
##		self.FontColor		= int(xmlattrs['fc'])
##		self.PicID		= int(xmlattrs['pid'])
##		self.HotKeyMeta		= int(xmlattrs['hkm'])
##		self.HotKeyScanCode	= int(xmlattrs['hks'])
	def	FillOutUI(self, uiitem):
		'''
		Fill UI Dialog object due to loaded data.
		@param uiitem QDialog object.
		'''
		self.uiitem = qt.QGroupBox(uiitem)
		self.uiitem.setTitle(qt.QString().fromUtf8(self.Caption))
		ctrl.FillOutUI(self)
class	c_BMasked(ctrl):
	'''
	Common parent for column controls.
	'''
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML
		@param xmlattr dict w/ xml attributes and their values.
		'''
		ctrl.LoadFromXML(self, xmlattrs)
		self.Caption		= xmlattrs['cap']
		self.Linked		= bool(int(xmlattrs['rq']))
		self.Formula		= xmlattrs['fm']
		self.ID			= xmlattrs['id']
		self.RqUID		= xmlattrs['rid']
		self.ValueType		= xmlattrs['vtp']
		self.ValueLen		= int(xmlattrs['vln'])
		self.ValuePrecision	= int(xmlattrs['vpr'])
		self.TypeUID		= xmlattrs.get('uref')	# ! implied
		self.FlagPT		= int(xmlattrs['pt'])
		self.Flag		= int(xmlattrs['flg'])
		self.Masque		= xmlattrs['msq']
		self.ShortTip		= xmlattrs['stp']
		self.FontSize		= bool(int(xmlattrs['fs']))
		self.FontBold		= bool(int(xmlattrs['fb']))
##		self.FontItalic		= bool(int(xmlattrs['fi']))
##		self.FontUndeline	= bool(int(xmlattrs['fu']))
		self.Unknown08		= int(xmlattrs['u08'])
		self.Unknown09		= int(xmlattrs['u09'])
		self.Unknown10		= int(xmlattrs['u10'])
		self.Unknown11		= int(xmlattrs['u11'])
		self.Unknown12		= int(xmlattrs['u12'])
		self.FontColor		= int(xmlattrs['fc'])
##		self.PicID		= int(xmlattrs['pid'])
##		self.HotKeyMeta		= int(xmlattrs['hkm'])
##		self.HotKeyScanCode	= int(xmlattrs['hks'])
	def	FillOutUI(self, uiitem):
		'''
		Fill UI Dialog object due to loaded data.
		@param uiitem QDialog object.
		'''
##		self.uiitem = qt.QCheckBox(uiitem)
##		self.uiitem.setText(qt.QString().fromUtf8(self.Caption))
##		ctrl.FillOutUI(self)
class	c_Button(ctrl):
	'''
	Common parent for column controls.
	'''
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML
		@param xmlattr dict w/ xml attributes and their values.
		'''
		ctrl.LoadFromXML(self, xmlattrs)
		self.Caption		= xmlattrs['cap']
##		self.Linked		= bool(int(xmlattrs['rq']))
		self.Formula		= xmlattrs['fm']
		self.ID			= xmlattrs['id']
		self.RqUID		= xmlattrs['rid']
		self.ValueType		= xmlattrs['vtp']
##		self.ValueLen		= int(xmlattrs['vln'])
##		self.ValuePrecision	= int(xmlattrs['vpr'])
##		self.FlagPT		= int(xmlattrs['pt'])
		self.Flag		= int(xmlattrs['flg'])
##		self.Masque		= xmlattrs['msq']
		self.ShortTip		= xmlattrs['stp']
##		self.FontSize		= bool(int(xmlattrs['fs']))
##		self.FontBold		= bool(int(xmlattrs['fb']))
##		self.FontItalic		= bool(int(xmlattrs['fi']))
##		self.FontUndeline	= bool(int(xmlattrs['fu']))
##		self.Unknown08		= int(xmlattrs['u08'])
##		self.Unknown09		= int(xmlattrs['u09'])
##		self.Unknown10		= int(xmlattrs['u10'])
##		self.Unknown11		= int(xmlattrs['u11'])
##		self.Unknown12		= int(xmlattrs['u12'])
##		self.FontColor		= int(xmlattrs['fc'])
		self.PicID		= int(xmlattrs['pid'])
		self.HotKeyMeta		= xmlattrs.get('hkm')	# implied
		self.HotKeyScanCode	= xmlattrs.get('hks')	# implied
	def	FillOutUI(self, uiitem):
		'''
		Fill UI Dialog object due to loaded data.
		@param uiitem QDialog object.
		'''
		self.uiitem = qt.QPushButton(uiitem)
		self.uiitem.setText(qt.QString().fromUtf8(self.Caption))
		ctrl.FillOutUI(self)
class	c_CheckBox(ctrl):
	'''
	Common parent for column controls.
	'''
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML
		@param xmlattr dict w/ xml attributes and their values.
		'''
		ctrl.LoadFromXML(self, xmlattrs)
		self.Caption		= xmlattrs['cap']
		self.Linked		= bool(int(xmlattrs['rq']))
		self.Formula		= xmlattrs['fm']
		self.ID			= xmlattrs['id']
		self.RqUID		= xmlattrs['rid']
		self.ValueType		= xmlattrs['vtp']
		self.ValueLen		= int(xmlattrs['vln'])
##		self.ValuePrecision	= int(xmlattrs['vpr'])
		self.FlagPT		= int(xmlattrs['pt'])
		self.Flag		= int(xmlattrs['flg'])
##		self.Masque		= xmlattrs['msq']
		self.ShortTip		= xmlattrs['stp']
##		self.FontSize		= bool(int(xmlattrs['fs']))
##		self.FontBold		= bool(int(xmlattrs['fb']))
##		self.FontItalic		= bool(int(xmlattrs['fi']))
##		self.FontUndeline	= bool(int(xmlattrs['fu']))
##		self.Unknown08		= int(xmlattrs['u08'])
##		self.Unknown09		= int(xmlattrs['u09'])
##		self.Unknown10		= int(xmlattrs['u10'])
##		self.Unknown11		= int(xmlattrs['u11'])
##		self.Unknown12		= int(xmlattrs['u12'])
##		self.FontColor		= int(xmlattrs['fc'])
##		self.PicID		= int(xmlattrs['pid'])
##		self.HotKeyMeta		= int(xmlattrs['hkm'])
##		self.HotKeyScanCode	= int(xmlattrs['hks'])
	def	FillOutUI(self, uiitem):
		'''
		Fill UI Dialog object due to loaded data.
		@param uiitem QDialog object.
		'''
		self.uiitem = qt.QCheckBox(uiitem)
		self.uiitem.setText(qt.QString().fromUtf8(self.Caption))
		ctrl.FillOutUI(self)
class	c_ComboBox(ctrl):
	'''
	Common parent for column controls.
	'''
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML
		@param xmlattr dict w/ xml attributes and their values.
		'''
		ctrl.LoadFromXML(self, xmlattrs)
		self.Caption		= xmlattrs['cap']
##		self.Linked		= bool(int(xmlattrs['rq']))
		self.Formula		= xmlattrs['fm']
		self.ID			= xmlattrs['id']
		self.RqUID		= xmlattrs['rid']
		self.ValueType		= xmlattrs['vtp']
##		self.ValueLen		= int(xmlattrs['vln'])
##		self.ValuePrecision	= int(xmlattrs['vpr'])
##		self.FlagPT		= int(xmlattrs['pt'])
		self.Flag		= int(xmlattrs['flg'])
##		self.Masque		= xmlattrs['msq']
		self.ShortTip		= xmlattrs['stp']
##		self.FontSize		= bool(int(xmlattrs['fs']))
##		self.FontBold		= bool(int(xmlattrs['fb']))
##		self.FontItalic		= bool(int(xmlattrs['fi']))
##		self.FontUndeline	= bool(int(xmlattrs['fu']))
##		self.Unknown08		= int(xmlattrs['u08'])
##		self.Unknown09		= int(xmlattrs['u09'])
##		self.Unknown10		= int(xmlattrs['u10'])
##		self.Unknown11		= int(xmlattrs['u11'])
##		self.Unknown12		= int(xmlattrs['u12'])
##		self.FontColor		= int(xmlattrs['fc'])
##		self.PicID		= int(xmlattrs['pid'])
##		self.HotKeyMeta		= int(xmlattrs['hkm'])
##		self.HotKeyScanCode	= int(xmlattrs['hks'])
class	c_ListBox(ctrl):
	'''
	Common parent for column controls.
	'''
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML
		@param xmlattr dict w/ xml attributes and their values.
		'''
		ctrl.LoadFromXML(self, xmlattrs)
		self.Caption		= xmlattrs['cap']
##		self.Linked		= bool(int(xmlattrs['rq']))
		self.Formula		= xmlattrs['fm']
		self.ID			= xmlattrs['id']
		self.RqUID		= xmlattrs['rid']
		self.ValueType		= xmlattrs['vtp']
##		self.ValueLen		= int(xmlattrs['vln'])
##		self.ValuePrecision	= int(xmlattrs['vpr'])
##		self.FlagPT		= int(xmlattrs['pt'])
		self.Flag		= int(xmlattrs['flg'])
##		self.Masque		= xmlattrs['msq']
		self.ShortTip		= xmlattrs['stp']
##		self.FontSize		= bool(int(xmlattrs['fs']))
##		self.FontBold		= bool(int(xmlattrs['fb']))
##		self.FontItalic		= bool(int(xmlattrs['fi']))
##		self.FontUndeline	= bool(int(xmlattrs['fu']))
##		self.Unknown08		= int(xmlattrs['u08'])
##		self.Unknown09		= int(xmlattrs['u09'])
##		self.Unknown10		= int(xmlattrs['u10'])
##		self.Unknown11		= int(xmlattrs['u11'])
##		self.Unknown12		= int(xmlattrs['u12'])
##		self.FontColor		= int(xmlattrs['fc'])
##		self.PicID		= int(xmlattrs['pid'])
##		self.HotKeyMeta		= int(xmlattrs['hkm'])
##		self.HotKeyScanCode	= int(xmlattrs['hks'])
	def	FillOutUI(self, uiitem):
		'''
		Fill UI Dialog object due to loaded data.
		@param uiitem QDialog object.
		'''
		self.uiitem = qt.QListBox(uiitem)
		#self.uiitem.setText(qt.QString().fromUtf8(self.Caption))
		ctrl.FillOutUI(self)
class	c_Radio(ctrl):
	'''
	Common parent for column controls.
	'''
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML
		@param xmlattr dict w/ xml attributes and their values.
		'''
		ctrl.LoadFromXML(self, xmlattrs)
		self.Caption		= xmlattrs['cap']
		self.Linked		= bool(int(xmlattrs['rq']))
		self.Formula		= xmlattrs['fm']
		self.ID			= xmlattrs['id']
		self.RqUID		= xmlattrs['rid']
		self.ValueType		= xmlattrs['vtp']
		self.ValueLen		= int(xmlattrs['vln'])
##		self.ValuePrecision	= int(xmlattrs['vpr'])
		self.FlagPT		= int(xmlattrs['pt'])
		self.Flag		= int(xmlattrs['flg'])
##		self.Masque		= xmlattrs['msq']
		self.ShortTip		= xmlattrs['stp']
##		self.FontSize		= bool(int(xmlattrs['fs']))
##		self.FontBold		= bool(int(xmlattrs['fb']))
##		self.FontItalic		= bool(int(xmlattrs['fi']))
##		self.FontUndeline	= bool(int(xmlattrs['fu']))
##		self.Unknown08		= int(xmlattrs['u08'])
##		self.Unknown09		= int(xmlattrs['u09'])
##		self.Unknown10		= int(xmlattrs['u10'])
##		self.Unknown11		= int(xmlattrs['u11'])
##		self.Unknown12		= int(xmlattrs['u12'])
##		self.FontColor		= int(xmlattrs['fc'])
##		self.PicID		= int(xmlattrs['pid'])
##		self.HotKeyMeta		= int(xmlattrs['hkm'])
##		self.HotKeyScanCode	= int(xmlattrs['hks'])
	def	FillOutUI(self, uiitem):
		'''
		Fill UI Dialog object due to loaded data.
		@param uiitem QDialog object.
		'''
		self.uiitem = qt.QRadioButton(uiitem)
		self.uiitem.setText(qt.QString().fromUtf8(self.Caption))
		ctrl.FillOutUI(self)
class	c_Label(ctrl):
	'''
	Common parent for column controls.
	'''
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML
		@param xmlattr dict w/ xml attributes and their values.
		'''
		ctrl.LoadFromXML(self, xmlattrs)
		self.Caption		= xmlattrs['cap']
##		self.Linked		= bool(int(xmlattrs['rq']))
		self.Formula		= xmlattrs['fm']
		self.ID			= xmlattrs['id']
		self.RqUID		= xmlattrs['rid']
		self.ValueType		= xmlattrs['vtp']
##		self.ValueLen		= int(xmlattrs['vln'])
##		self.ValuePrecision	= int(xmlattrs['vpr'])
##		self.FlagPT		= int(xmlattrs['pt'])
		self.Flag		= int(xmlattrs['flg'])
##		self.Masque		= xmlattrs['msq']
		self.ShortTip		= xmlattrs['stp']
##		self.FontSize		= bool(int(xmlattrs['fs']))
		self.Unknown03		= int(xmlattrs['u03'])
		self.FontBold		= bool(int(xmlattrs['fb']))
		self.FontItalic		= bool(int(xmlattrs['fi']))
		self.FontUndeline	= bool(int(xmlattrs['fu']))
		self.Unknown08		= int(xmlattrs['u08'])
		self.Unknown09		= int(xmlattrs['u09'])
		self.Unknown10		= int(xmlattrs['u10'])
		self.Unknown11		= int(xmlattrs['u11'])
		self.Unknown12		= int(xmlattrs['u12'])
		self.FontColor		= int(xmlattrs['fc'])
##		self.PicID		= int(xmlattrs['pid'])
##		self.HotKeyMeta		= int(xmlattrs['hkm'])
##		self.HotKeyScanCode	= int(xmlattrs['hks'])
	def	FillOutUI(self, uiitem):
		'''
		Fill UI Dialog object due to loaded data.
		@param uiitem QDialog object.
		'''
		self.uiitem = qt.QLabel(uiitem)
		self.uiitem.setText(qt.QString().fromUtf8(self.Caption))
		ctrl.FillOutUI(self)
class	c_Table(ctrl):
	'''
	Common parent for column controls.
	'''
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML
		@param xmlattr dict w/ xml attributes and their values.
		'''
		ctrl.LoadFromXML(self, xmlattrs)
		self.Caption		= xmlattrs['cap']
##		self.Linked		= bool(int(xmlattrs['rq']))
		self.Formula		= xmlattrs['fm']
		self.ID			= xmlattrs['id']
		self.RqUID		= xmlattrs['rid']
		self.ValueType		= xmlattrs['vtp']
		self.ValueLen		= int(xmlattrs['vln'])
##		self.ValuePrecision	= int(xmlattrs['vpr'])
##		self.FlagPT		= int(xmlattrs['pt'])
		self.Flag		= int(xmlattrs['flg'])
##		self.Masque		= xmlattrs['msq']
##		self.ShortTip		= xmlattrs['stp']
##		self.FontSize		= bool(int(xmlattrs['fs']))
##		self.FontBold		= bool(int(xmlattrs['fb']))
##		self.FontItalic		= bool(int(xmlattrs['fi']))
##		self.FontUndeline	= bool(int(xmlattrs['fu']))
##		self.Unknown08		= int(xmlattrs['u08'])
##		self.Unknown09		= int(xmlattrs['u09'])
##		self.Unknown10		= int(xmlattrs['u10'])
##		self.Unknown11		= int(xmlattrs['u11'])
##		self.Unknown12		= int(xmlattrs['u12'])
##		self.FontColor		= int(xmlattrs['fc'])
		self.PicID		= int(xmlattrs['pid'])
##		self.HotKeyMeta		= int(xmlattrs['hkm'])
##		self.HotKeyScanCode	= int(xmlattrs['hks'])
class	c_Picture(ctrl):
	'''
	Common parent for column controls.
	'''
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML
		@param xmlattr dict w/ xml attributes and their values.
		'''
		ctrl.LoadFromXML(self, xmlattrs)
##		self.Caption		= xmlattrs['cap']
##		self.Linked		= bool(int(xmlattrs['rq']))
##		self.Formula		= xmlattrs['fm']
		self.ID			= xmlattrs['id']
		self.RqUID		= xmlattrs['rid']
##		self.ValueType		= xmlattrs['vtp']
##		self.ValueLen		= int(xmlattrs['vln'])
##		self.ValuePrecision	= int(xmlattrs['vpr'])
##		self.FlagPT		= int(xmlattrs['pt'])
		self.Flag		= int(xmlattrs['flg'])
##		self.Masque		= xmlattrs['msq']
##		self.ShortTip		= xmlattrs['stp']
##		self.FontSize		= bool(int(xmlattrs['fs']))
##		self.FontBold		= bool(int(xmlattrs['fb']))
##		self.FontItalic		= bool(int(xmlattrs['fi']))
##		self.FontUndeline	= bool(int(xmlattrs['fu']))
##		self.Unknown08		= int(xmlattrs['u08'])
##		self.Unknown09		= int(xmlattrs['u09'])
##		self.Unknown10		= int(xmlattrs['u10'])
##		self.Unknown11		= int(xmlattrs['u11'])
##		self.Unknown12		= int(xmlattrs['u12'])
##		self.FontColor		= int(xmlattrs['fc'])
		self.PicID		= int(xmlattrs['pid'])
##		self.HotKeyMeta		= int(xmlattrs['hkm'])
##		self.HotKeyScanCode	= int(xmlattrs['hks'])
class	c_TreeView(ctrl):
	'''
	Common parent for column controls.
	'''
	def	LoadFromXML(self, xmlattrs):
		'''
		Load data from XML
		@param xmlattr dict w/ xml attributes and their values.
		'''
		ctrl.LoadFromXML(self, xmlattrs)
##		self.Caption		= xmlattrs['cap']
##		self.Linked		= bool(int(xmlattrs['rq']))
##		self.Formula		= xmlattrs['fm']
##		self.ID			= xmlattrs['id']
		self.RqUID		= xmlattrs['rid']
##		self.ValueType		= xmlattrs['vtp']
##		self.ValueLen		= int(xmlattrs['vln'])
##		self.ValuePrecision	= int(xmlattrs['vpr'])
##		self.TypeUID		= xmlattrs.get('uref')	# ! implied
##		self.FlagPT		= int(xmlattrs['pt'])
##		self.Flag		= int(xmlattrs['flg'])
##		self.Masque		= xmlattrs['msq']
##		self.ShortTip		= xmlattrs['stp']
##		self.FontSize		= bool(int(xmlattrs['fs']))
##		self.FontBold		= bool(int(xmlattrs['fb']))
##		self.FontItalic		= bool(int(xmlattrs['fi']))
##		self.FontUndeline	= bool(int(xmlattrs['fu']))
##		self.Unknown08		= int(xmlattrs['u08'])
##		self.Unknown09		= int(xmlattrs['u09'])
##		self.Unknown10		= int(xmlattrs['u10'])
##		self.Unknown11		= int(xmlattrs['u11'])
##		self.Unknown12		= int(xmlattrs['u12'])
##		self.FontColor		= int(xmlattrs['fc'])
##		self.PicID		= int(xmlattrs['pid'])
##		self.HotKeyMeta		= int(xmlattrs['hkm'])
##		self.HotKeyScanCode	= int(xmlattrs['hks'])
	def	FillOutUI(self, uiitem):
		'''
		Fill UI Dialog object due to loaded data.
		@param uiitem QDialog object.
		'''
		self.uiitem = qt.QListView(uiitem)
##		self.uiitem.setText(qt.QString().fromUtf8(self.Caption))
		self.uiitem.addColumn("")
		self.uiitem.setRootIsDecorated(True)
		a = qt.QListViewItem(self.uiitem, "Level 1")
		a.setOpen(True)
		qt.QListViewItem(qt.QListViewItem(a, "Level 2"), "Level 3")
		ctrl.FillOutUI(self)
