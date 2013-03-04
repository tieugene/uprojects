#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Main module
@author TI_Eugene
'''

class	PropertyItem(qt.QListViewItem):
	def	__init__(self, l, after, prop, propName ):
		'''
		PropertyLists *l, PropertyItem *after, PropertyItem *prop, const QString &propName
		'''
		qt.QListViewItem.__init__(self, l, after )

		self.listview = l
		self.property = prop
		self.propertyName = propName

		self.setSelectable( False )
		self.open = False
		self.setText( 0, self.propertyName )
		self.changed = False
		self.setText( 1, "" )
		self.resetButton = 0

	#~PropertyItem()

	def	paintCell( self, p, cg, column, width, align ):
		'''
		QPainter *p, const QColorGroup &cg, int column, int width, int align
		'''
		g = qt.QColorGroup( cg )
		g.setColor( qt.QColorGroup.Base, self.backgroundColor() )
		g.setColor( qt.QColorGroup.Foreground, qt.Qt.black )
		g.setColor( qt.QColorGroup.Text, qt.Qt.black )
		indent = 0
		if ( column == 0 ):
			if (self.property):	# indent = 20 + ( self.property ? 20 : 0 )
				indent = 40
			else:
				indent = 20
			p.fillRect( 0, 0, width, self.height(), self.backgroundColor() )
			p.save()
			p.translate( indent, 0 )

		if ( self.isChanged() and (column == 0) ):
			p.save()
			f = qt.QFont(p.font())
			f.setBold( True )
			p.setFont( f )

		if ( (not self.hasCustomContents()) or (column != 1) ):
			qt.QListViewItem.paintCell( self, p, g, column, width - indent, align )
		else:
			p.fillRect( 0, 0, width, self.height(), self.backgroundColor() )
			self.drawCustomContents( p, qt.QRect( 0, 0, width, self.height() ) )

		if ( self.isChanged() and (column == 0) ):
			p.restore()
		if ( column == 0 ):
			p.restore()
		if ( self.hasSubItems() and (column == 0) ):
			p.save()
			p.setPen( cg.foreground() )
			p.setBrush( cg.base() )
			p.drawRect( 5, height() / 2 - 4, 9, 9 )
			p.drawLine( 7, self.height() / 2, 11, self.height() / 2 )
			if ( not self.isOpen() ):
				p.drawLine( 9, self.height() / 2 - 2, 9, self.height() / 2 + 2 )
			p.restore()
		p.save()
		p.setPen( qt.QPen( cg.dark(), 1 ) )
		p.drawLine( 0, self.height() - 1, width, self.height() - 1 )
		p.drawLine( width - 1, 0, width - 1, self.height() )
		p.restore()

		if ( (self.listview.currentItem() == self) and (column == 0) and (not self.listview.hasFocus()) and (not self.listview.viewport().hasFocus()) ):
			self.paintFocus( p, cg, qt.QRect( 0, 0, width, self.height() ) )

	def	paintBranches( self, p, cg, w, y, h ):
		'''
		QPainter * p, const QColorGroup & cg, int w, int y, int h
		'''
		g = qt.QColorGroup( cg )
		g.setColor( qt.QColorGroup.Base, self.backgroundColor() )
		qt.QListViewItem.paintBranches( self, p, g, w, y, h )
	def	paintFocus( self, p, cg, r ):
		'''
		QPainter *p, const QColorGroup &cg, const QRect &r
		'''
		p.save();
		qt.QApplication.style().drawPrimitive(qt.QStyle.PE_Panel, p, r, cg, qt.QStyle.Style_Sunken, qt.QStyleOption(1,1) )
		p.restore();

	def	hasSubItems(self):
		'''
		virtual bool
		'''
		return False
	def	createChildren(self):
		'''
		virtual void
		'''
		pass
	def	initChildren(self):
		'''
		virtual void
		'''
		pass
	def	isOpen(self):
		return self.open
	def	setOpen( self, b ):
		'''
		@param b:bool
		'''
		if ( b == self.open ):
			return
		open = b

		if ( not open ):
			self.children.setAutoDelete( True )
			self.children.clear()
			set.children.setAutoDelete( False )
			qt.qApp.processEvents()
			self.listview.updateEditorSize()
			return

		self.createChildren()
		self.initChildren()
		qt.qApp.processEvents()
		self.listview.updateEditorSize()

	def	showEditor(self):
		'''
		virtual void 
		'''
		self.createResetButton()
		self.resetButton.parentWidget().show()
	def	hideEditor(self):
		'''
		virtual void 
		'''
		self.createResetButton()
		self.resetButton.parentWidget().hide()

	def	setValue( self, v ):
		'''
		virtual void setValue( const QVariant &v )
		'''
		self.val = v
	def	value(self):
		return self.val
	def	name(self):
		return propertyName
	def	notifyValueChange(self):
		'''
		virtual void
		'''
		if ( not self.propertyParent() ):
			self.listview.valueChanged( self )
			self.setChanged( True )
			if ( self.hasSubItems() ):
				self.initChildren()
		else:
			self.propertyParent().childValueChanged( self )
			self.setChanged( True )

	def	setChanged( self, b, updateDb = True ):
		'''
		virtual void setChanged( bool b, bool updateDb = TRUE )
		'''
		if ( self.propertyParent() ):
			return
		if ( self.changed == b ):
			return;
		self.changed = b
		self.repaint()
		if ( updateDb ):
			qt.MetaDataBase.setPropertyChanged( self.listview.propertyEditor().widget(), self.name(), self.changed );
		self.updateResetButtonState();

	def	isChanged(self):
		return self.changed

	def	placeEditor( self, w ):
		'''
		virtual void placeEditor( QWidget *w )
		'''
		self.createResetButton()
		r = self.listview.itemRect( self )
		if ( not r.size().isValid() ):
			self.listview.ensureItemVisible( self )
			r = self.listview.itemRect( self )
		r.setX( self.listview.header().sectionPos( 1 ) );
		r.setWidth( self.listview.header().sectionSize( 1 ) - 1 )
		r.setWidth( r.width() - self.resetButton.width() - 2 )
		r = qt.QRect( self.listview.viewportToContents( r.topLeft() ), r.size() )
		w.resize( r.size() )
		self.listview.moveChild( w, r.x(), r.y() );
		self.resetButton.parentWidget().resize( self.resetButton.sizeHint().width() + 10, r.height() )
		self.listview.moveChild( self.resetButton.parentWidget(), r.x() + r.width() - 8, r.y() )
		self.resetButton.setFixedHeight( qt.QMAX( 0, r.height() - 3 ) )

	def	propertyParent(self):
		'''
		virtual PropertyItem *
		'''
		return self.property
	def	childValueChanged( self, child ):
		'''
		virtual void
		@prop PropertyItem *child
		'''
		pass

	def	addChild( self, i ):
		self.children.append( i )
	def	childCount(self):
		return self.children.count()
	def	child( self, i ):
		return self.children.at( i )

	def	hasCustomContents(self):
		'''
		virtual bool
		'''
		return False
	def	drawCustomContents( p, r ):
		'''
		virtual void drawCustomContents( QPainter *p, const QRect &r )
		'''
		pass

	def	updateBackColor(self):
		if ( self.itemAbove() and (self != self.listview.firstChild()) ):
			if ( self.itemAbove().backColor == backColor1 ):
				self.backColor = self.backColor2
			else:
				self.backColor = self.backColor1
		else:
			self.backColor = self.backColor1
		if ( self.listview.firstChild() == self ):
			self.backColor = self.backColor1

	def	setup(self):
		qt.QListViewItem.setup(self)
		self.setHeight( qt.QListViewItem.height(self) + 2 )

	def	currentItem(self):
		'''
		virtual QString
		'''
		return qt.QString.null
	def	currentIntItem(self):
		'''
		virtual int
		'''
		return -1
	def	setCurrentItem( self, s ):
		'''
		virtual void
		@param const QString &s | int
		'''
		pass
	def	currentIntItemFromObject(self):
		'''
		virtual int
		'''
		return -1
	def	currentItemFromObject(self):
		'''
		virtual QString
		'''
		return qt.QString.null

	def	setFocus( w ):
		if ( (not self.qApp.focusWidget()) or self.listview.propertyEditor().formWindow() and ( (not self.MainWindow.self.isAFormWindowChild( self.qApp.focusWidget() ) ) and (not self.qApp.focusWidget().inherits( "Editor" ) ) ) ):
			w.setFocus()

	def	toggle():
		'''
		virtual void
		'''
		pass
	def	setText( self, col, t ):
		txt = qt.QString( t )
		if ( col == 1 ):
			txt = txt.replace( "\n", " " )
		QListViewItem.setText( self, col, txt )

	# protected:
	#PropertyList *_listview
	#QVariant val

	#private:
	def	backgroundColor(self):
		self.updateBackColor()
		if ( this == self.listview.currentItem() ):
			return self.selectedBack
		return self.backColor

	def	createResetButton(self):
		'''    if ( resetButton ) {
			resetButton->parentWidget()->lower();
			return;
		    }
		    QHBox *hbox = new QHBox( listview->viewport() );
		    hbox->setFrameStyle( QFrame::StyledPanel | QFrame::Sunken );
		    hbox->setLineWidth( 1 );
		    resetButton = new QPushButton( hbox );
		    setupStyle( resetButton );
		    resetButton->setPixmap( QPixmap::fromMimeSource( "designer_resetproperty.png" ) );
		    resetButton->setFixedWidth( resetButton->sizeHint().width() );
		    hbox->layout()->setAlignment( Qt::AlignRight );
		    listview->addChild( hbox );
		    hbox->hide();
		    QObject::connect( resetButton, SIGNAL( clicked() ),
				      listview, SLOT( resetProperty() ) );
		    QToolTip::add( resetButton, PropertyEditor::tr( "Reset the property to its default value" ) );
		    QWhatsThis::add( resetButton, PropertyEditor::tr( "Click this button to reset the property to its default value" ) );
		    updateResetButtonState();
		'''
		pass
	def	updateResetButtonState(self):
		if ( not self.resetButton ):
			return
		if ( self.propertyParent() or (not qt.WidgetFactory.canResetProperty( self.listview.propertyEditor().widget(), self.name() ) )):
			self.resetButton.setEnabled( False )
		else:
			self.resetButton.setEnabled( self.isChanged() )

	#bool open, changed
	#PropertyItem *property
	#QString propertyName
	#QPtrList<PropertyItem> children
	#QColor backColor
	#QPushButton *resetButton
