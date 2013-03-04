# -*- coding: utf-8 -*-

'''
QPropertyItem analog for property list of Table cell.
@author TI_Eugene
'''

import	qt

BoolPic = (
	["16 16 2 1",
	" 	c #000000",
	".	c #FFFFFF",
	"                ",
	" .............. ",
	" .............. ",
	" .............. ",
	" .............. ",
	" .............. ",
	" .............. ",
	" .............. ",
	" .............. ",
	" .............. ",
	" .............. ",
	" .............. ",
	" .............. ",
	" .............. ",
	" .............. ",
	"                "],
	["16 16 2 1",
	" 	c #000000",
	".	c #FFFFFF",
	"                ",
	" .............. ",
	" ............ . ",
	" ............ . ",
	" ........... .. ",
	" ........... .. ",
	" .... ..... ... ",
	" .... ..... ... ",
	" ..... ... .... ",
	" ..... ... .... ",
	" ...... . ..... ",
	" ...... . ..... ",
	" ....... ...... ",
	" ....... ...... ",
	" .............. ",
	"                "]
)

class	PropertyItem(qt.QListViewItem):
	def	__init__(self, p, a, n, v = None ):
		'''
		@param p - parent list|item
		@param a - after
		@param n - name
		@param v - value
		'''
		if (a):	# after defined
			qt.QListViewItem.__init__(self, p, a, n )
		else:
			qt.QListViewItem.__init__(self, p, n )
		self.setSelectable( True )
		self.value = v
class	PropertyItemNone(PropertyItem):
	def	__init__(self, p, a, n, v = None):
		'''
		@param p - parent list|item
		@param a - after
		@param n - name
		@param v - value
		'''
		PropertyItem.__init__(self, p, a, n, v)
	def	paintCell( self, p, cg, column, width, align ):
		'''
		QPainter *p, const QColorGroup &cg, int column, int width, int align
		'''
		if (column != 1):
			qt.QListViewItem.paintCell( self, p, cg, column, width, align )
		else:
			p.save()
			p.fillRect( 0, 0, width, self.height(), qt.QBrush(qt.Qt.white) )
			p.setPen( qt.QPen( cg.dark(), 1 ) )
			p.drawLine( 0, 0, width - 1, self.height() - 1 )
			p.drawLine( 0, self.height() - 1, width - 1, 0 )
			p.restore()
class	PropertyItemBool(PropertyItem):
	def	__init__(self, p, a, n, v = False):
		'''
		@param p - parent list|item
		@param a - after
		@param n - name
		@param k - sort key
		'''
		PropertyItem.__init__(self, p, a, n, v)
		if (v):
			p = 1
		else:
			p = 0
		self.setPixmap(1, qt.QPixmap(BoolPic[p]))
class	PropertyItemText(PropertyItem):
	def	__init__(self, p, a, n, v = ""):
		'''
		@param p - parent list|item
		@param a - after
		@param n - name
		@param v - value (text)
		'''
		PropertyItem.__init__(self, p, a, n, v)
		self.setText(1, v)
class	PropertyItemColor(PropertyItem):
	def	__init__(self, p, a, n, v = (0xFF, 0xFF, 0xFF)):
		'''
		@param p - parent list|item
		@param a - after
		@param n - name
		@param v - value ((r, g, b) touple)
		'''
		PropertyItem.__init__(self, p, a, n, v)
		self.v = qt.QColor(v[0], v[1], v[2])
	def	paintCell( self, p, cg, column, width, align ):
		'''
		QPainter *p, const QColorGroup &cg, int column, int width, int align
		'''
		if (column != 1):
			qt.QListViewItem.paintCell( self, p, cg, column, width, align )
		else:
			p.save()
			p.fillRect( 0, 0, width, self.height(), qt.QBrush(self.v) )
			p.restore()
class	PropertyItemPattern(PropertyItem):
	def	__init__(self, p, a, n, v = None):
		'''
		@param p - parent list|item
		@param a - after
		@param n - name
		@param v - value (xpm)
		'''
		PropertyItem.__init__(self, p, a, n, v)
		if (v):
			#self.setPixmap(1, qt.QPixmap(v))
			self.v = qt.QPixmap(v)
	def	paintCell( self, p, cg, column, width, align ):
		'''
		QPainter *p, const QColorGroup &cg, int column, int width, int align
		'''
		if (column != 1):
			qt.QListViewItem.paintCell( self, p, cg, column, width, align )
		else:
			p.save()
			p.drawTiledPixmap( 0, 0, width, self.height(), self.v )
			p.restore()
class	PropertyItemFrame(PropertyItem):
	def	__init__(self, p, a, n, v):
		'''
		@param p - parent list|item
		@param a - after
		@param n - name
		@param v - value (xpm)
		'''
		PropertyItem.__init__(self, p, a, n, v)
		self.v = qt.QPixmap(v)
	def	paintCell( self, p, cg, column, width, align ):
		'''
		QPainter *p, const QColorGroup &cg, int column, int width, int align
		'''
		if (column != 1):
			qt.QListViewItem.paintCell( self, p, cg, column, width, align )
		else:
			p.save()
			p.drawTiledPixmap( 0, self.height()/2 - 1, width, self.v.height(), self.v )
			p.restore()
