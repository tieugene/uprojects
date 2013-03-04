/***************************************************************************
 *   Copyright (C) 2007 by Eugene A. Pivnev   *
 *   ti.eugene@gmail.com   *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program; if not, write to the                         *
 *   Free Software Foundation, Inc.,                                       *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
 ***************************************************************************/

//#include <map>
//#include "common.h"
#include "core.h"
void	test(const char * s, const Moxel &m) {
	cerr << "Test: "  << s << ";"
		" Fonts:" << m.font.size() << ","
		" Cols:"  << m.col.size() << ","
		" Rows:"  << m.row.size() << ","
		" Cells:" << m.cell.size() << ","
		<< endl;
}

//#define err(s)	cerr << s << endl

/// Props
Props::Props() {
//err("Props empty generating start.");
 	defined.fontname	= false;
	defined.fontsize	= false;
	defined.fontbold	= false;
	defined.fontitalic	= false;
	defined.fontunderline	= false;
	defined.fontcolor	= false;
	defined.frameleft	= false;
	defined.frametop	= false;
	defined.frameright	= false;
	defined.framebottom	= false;
	defined.framecolor	= false;
	defined.flag1		= false;
	defined.flag2		= false;
	defined.hallign		= false;
	defined.vallign		= false;
	defined.backgroundcolor	= false;
	defined.patterntype	= false;
	defined.patterncolor	= false;
	defined.txtctrl		= false;
	defined.txttype		= false;
	defined.txtprot		= false;
	defined.text		= false;
	defined.description	= false;
	// variables
	size.height		= 0;
	size.width		= 0;
	font.number		= 0;
	font.size		= 0;
	font.color		= 0;
	font.bold		= false;
	font.italic		= false;
	font.underline		= false;
	allign.h		= TypeAllign::Left;
	allign.onselected	= false;
	allign.v		= TypeAllign::Top;
	background.color	= 0;
	pattern.type		= 0;
	pattern.color		= 0;
	frame.left		= 0;
	frame.right		= 0;
	frame.top		= 0;
	frame.bottom		= 0;
	txtprop.control		= TypeTxtProp::Auto;
	txtprop.type		= TypeTxtProp::Text;
	txtprop.protection	= false;
	angle			= 0;
//err("Props empty generating stop.");
}

Props::Props(const Props &src) {
//err("Props copying start.");
	defined.fontname	= src.defined.fontname;
	defined.fontsize	= src.defined.fontsize;
	defined.fontbold	= src.defined.fontbold;
	defined.fontitalic	= src.defined.fontitalic;
	defined.fontunderline	= src.defined.fontunderline;
	defined.fontcolor	= src.defined.fontcolor;
	defined.frameleft	= src.defined.frameleft;
	defined.frametop	= src.defined.frametop;
	defined.frameright	= src.defined.frameright;
	defined.framebottom	= src.defined.framebottom;
	defined.framecolor	= src.defined.framecolor;
	defined.flag1		= src.defined.flag1;
	defined.flag2		= src.defined.flag2;
	defined.hallign		= src.defined.hallign;
	defined.vallign		= src.defined.vallign;
	defined.backgroundcolor	= src.defined.backgroundcolor;
	defined.patterntype	= src.defined.patterntype;
	defined.patterncolor	= src.defined.patterncolor;
	defined.txtctrl		= src.defined.txtctrl;
	defined.txttype		= src.defined.txttype;
	defined.txtprot		= src.defined.txtprot;
	defined.text		= src.defined.text;
	defined.description	= src.defined.description;
	// variables
	size.height		= src.size.height;
	size.width		= src.size.width;
	font.number		= src.font.number;
	font.size		= src.font.size;
	font.color		= src.font.color;
	font.bold		= src.font.bold;
	font.italic		= src.font.italic;
	font.underline		= src.font.underline;
	allign.h		= src.allign.h;
	allign.onselected	= src.allign.onselected;
	allign.v		= src.allign.v;
	background.color	= src.background.color;
	pattern.type		= src.pattern.type;
	pattern.color		= src.pattern.color;
	frame.left		= src.frame.left;
	frame.right		= src.frame.right;
	frame.top		= src.frame.top;
	frame.bottom		= src.frame.bottom;
	txtprop.control		= src.txtprop.control;
	txtprop.type		= src.txtprop.type;
	txtprop.protection	= src.txtprop.protection;
	angle			= src.angle;
//err("Props copying end.");
}

Props::~Props() {
//err("Props destroyed.");
}

/// ExtProps
ExtProps::ExtProps() : Props() {
//err("ExtProps empty generating start.");
//	Text = string();
//	Description = string();
//err("ExtProps empty generating stop.");
}

ExtProps::ExtProps(const ExtProps &src) : Props(src) {
//err("ExtProps copy generating start.");
	Text		= src.Text;
	Description	= src.Description;
//err("ExtProps copy generating stop.");
}

ExtProps::~ExtProps() {
//err("ExtProps destroyed.");
}

/// Region
Region::Region() {
}

Region::Region(const Region &src) {
}

Region::~Region() {
}

/// Obj
Obj::Obj() : ExtProps(), Region() {
}

Obj::Obj(const Obj &src) : ExtProps(src), Region(src) {
}

Obj::~Obj() {
}

/// Named
Named::Named() {
}

Named::Named(const Named &src) {
	Name = src.Name;
}

Named::Named(const string &src) {
	Name = src;
}

Named::~Named() {
}

/// Bulk
Bulk::Bulk() {
}

Bulk::Bulk(const Bulk &src) {
}

Bulk::~Bulk() {
}

/// Directed
Directed::Directed() {
}

Directed::Directed(const Directed &src) {
}

Directed::~Directed() {
}

/// Font
Font::Font() : Named () {
}

Font::Font(const Font &src) : Named(src) {
}

Font::~Font() {
}

/// HeaderFooter
HeaderFooter::HeaderFooter() : ExtProps() {
}

HeaderFooter::HeaderFooter(const HeaderFooter &src) : ExtProps(src) {
}

HeaderFooter::~HeaderFooter() {
}

/// Table
Table::Table() : Props() {
}

Table::Table(const Table &src) : Props(src) {
}

Table::~Table() {
}

/// Column
Column::Column() : ExtProps() {
//err("Column empty generating start.");
	no = 0;
//err("Column empty generating end.");
}

Column::Column(const RC n) : ExtProps() {
//err("Column " << n << " generating start.");
	no = n;
//err("Column " << n << " generating end.");
}

Column::Column(const Column &src) : ExtProps(src) {
//err("Column " << src.no << " copying start.");
	no = src.no;
//err("Column " << src.no << " copying end.");
}

Column::~Column() {
//err("Column destroyed.");
}

/// Row
Row::Row() : Props() {
	no = 0;
}

Row::Row(const RC n) : Props() {
	no = n;
}

Row::Row(const Row &src) : Props(src) {
	no = src.no;
}

Row::~Row() {
}

/// Cell
Cell::Cell() : ExtProps() {
}

Cell::Cell(const Cell &src) : ExtProps(src) {
}

Cell::~Cell() {
}

/// Line
Line::Line() : Obj() {
}

Line::Line(const Line &src) : Obj(src) {
}

Line::~Line() {
}

/// Rect
Rect::Rect() : Obj() {
}

Rect::Rect(const Rect &src) : Obj(src) {
}

Rect::~Rect() {
}

/// Frame
Frame::Frame() : Obj() {
}

Frame::Frame(const Frame &src) : Obj(src) {
}

Frame::~Frame() {
}

/// Picture
Picture::Picture() : Obj(), Bulk() {
}

Picture::Picture(const Picture &src) : Obj(src), Bulk(src) {
}

Picture::~Picture() {
}

/// Diagram
Diagram::Diagram() : Obj(), Named(), Bulk() {
}

Diagram::Diagram(const Diagram &src) : Obj(), Named(src), Bulk(src) {
}

Diagram::~Diagram() {
}

/// OLE
OLE::OLE() : Obj(), Bulk() {
}

OLE::OLE(const OLE &src) : Obj(src), Bulk(src) {
}

OLE::~OLE() {
}

/// Join
Join::Join() : Region() {
}

Join::Join(const Join &src) : Region(src) {
}

Join::~Join() {
}

/// Section
Section::Section() : Named(), Directed() {
}

Section::Section(const Section &src) : Named(src), Directed(src) {
}

Section::~Section() {
}

/// NamedRegion
NamedRegion::NamedRegion() : Region(), Named() {
}

NamedRegion::NamedRegion(const NamedRegion &src) : Region(src), Named(src) {
}

NamedRegion::~NamedRegion() {
}

/// FormFeed
FormFeed::FormFeed() : Directed() {
}

FormFeed::FormFeed(const FormFeed &src) : Directed(src) {
}

FormFeed::~FormFeed() {
}

/// Moxel
Moxel::Moxel() {
//	cerr << "Moxel empty" << endl;
	ver	= 0;
/*	font	= mFont();
	header	= HeaderFooter();
	footer	= HeaderFooter();
	table	= Table();
	col	= mColumn();
	row	= mRow();
	cell	= vector <Cell> ();
	obj	= vector <Obj> ();
	join	= vector <Join> ();
	sect	= vector <Section> ();
	named	= vector <NamedRegion> ();
	ff	= vector <FormFeed> ();*/
	//strings	= NULL;
}

Moxel::Moxel(Moxel &src) {
	cerr << "Moxel copy" << endl;
	ver	= src.ver;
	font	= src.font;
	header	= src.header;
	footer	= src.footer;
	table	= src.table;
	col	= src.col;
	row	= src.row;
	cell	= src.cell;
	obj	= src.obj;
	join	= src.join;
	sect	= src.sect;
	named	= src.named;
	ff	= src.ff;
	//strings	= NULL;
}

Moxel::~Moxel() {
}
