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

/*!	\file core.h
	\brief Core classes definitions
	TODO: namespace
*/

#ifndef	_CORE_H
#define	_CORE_H

#include	<string>
#include	<vector>
//#include	<wchar.h>
#include	<map>
#include	"common.h"

// Usual things
typedef	BYTE	COLOR;			// 0..55
typedef	BYTE	PATTERN;		// 0..15
typedef	BYTE	FRAME;			// 0..9(15?)
typedef	WORD	ANGLE;			// 0...
//typedef	BYTE	TXTCTRL;		// 0..5|255
//typedef	BYTE	TXTTYPE;		// 0..4|255
typedef	DWORD	RC;			// row or column no
typedef	DWORD	XY;			// x or y coord

// Parent classes

/// Main parent
class	Props {
	// variabes
 	public:
		//DWORD			Flag;		// NoAuto & Defined bit flags
		struct	TypeFlag	{
			bool fontname		: 1;
			bool fontsize		: 1;
			bool fontbold		: 1;
			bool fontitalic		: 1;
			bool fontunderline	: 1;
			bool frameleft		: 1;
			bool frametop		: 1;
			bool frameright		: 1;
			bool framebottom	: 1;
			bool framecolor		: 1;
			bool flag1		: 1;
			bool flag2		: 1;
			bool hallign		: 1;
			bool vallign		: 1;
			bool fontcolor		: 1;
			bool backgroundcolor	: 1;
			bool patterntype	: 1;
			bool patterncolor	: 1;
			bool txtctrl		: 1;
			bool txttype		: 1;
			bool txtprot		: 1;
			int  dummy		: 9;
			bool description	: 1;
			bool text		: 1;
		}			defined;
		struct	{
			WORD		height;		// Row height in 1/8th of u.e.
			WORD		width;		// Col width in 1/4th of u.e.
		}			size;
		struct	{
			WORD		number;		// Number
			WORD		size;		// = -4*pt
			COLOR		color;
			bool		bold;
			bool		italic;
			bool		underline;
		}			font;
		struct	TypeAllign {
			enum	HAllign	{
				Left,
				HCenter,
				Right,
				Width
			}		h;
			bool	onselected;
			enum	VAllign	{
				Top,
				VCenter,
				Bottom
			}		v;
		}			allign;
		struct	{
			COLOR		color;
		}			background;
		struct	{
			PATTERN		type;		// Type
			COLOR		color;
		}			pattern;
		struct	{
			FRAME		left;
			FRAME		top;
			FRAME		right;
			FRAME		bottom;
			COLOR		color;		// for all
		}			frame;
		struct	TypeTxtProp	{
			enum	EnumTxtCtrl	{
				Auto,
				Cut,
				Stopup,
				Wrap,
				Red,
				StopupAndRed,
				Unknown
			}		control;
			enum	EnumTxtType	{
				Text,
				Expression,
				Template,
				FixedTemplate
			}		type;
			bool		protection;	// optional
		}			txtprop;
		ANGLE			angle;		// Angle (new in v.6+ (7.70.025+)), optional
	// functions
	Props	();
	Props	(const Props &);
	~Props	();
};

class	ExtProps : public Props {
 	public:
		string			Text, Description;
//		char			*Text, *Description;	// wchar
	// members
	ExtProps	();
	ExtProps	(const ExtProps &);
	~ExtProps	();
};

class	Region {
 	public:
		RC		R0;
		RC		C0;
		RC		R1;
		RC		C1;
		Region		();
		Region		(const Region &);
		~Region		();
};

class	Obj : public ExtProps, public Region {
 	public:
		enum	EnumType	{
			Line,		// 1
			Rectangle,	// 2
			TextFrame,	// 3
			Picture,	// 5 > 4
			Diagram,	// 4 > 5
			OLE,		// 4 > 6
		}	Type;
		//BYTE			Type;
		XY			X0;
		XY			Y0;
		XY			X1;
		XY			Y1;
		DWORD			Level;
	Obj		();
	Obj		(const Obj &);
	~Obj		();
};

class	Named {
 	public:
		string			Name;
//		char			*Name;	// wchar
		Named	();
		Named	(const Named &);
		Named	(const string &);
		~Named	();
};

class	Bulk {
 	public:
		BYTE			*Data;	// ? []
	// functions
		Bulk	();
		Bulk	(const Bulk &);
		~Bulk	();
};

class	Directed {
 	public:
		bool			Direction;
	// functions
		Directed	();
		Directed	(const Directed &);
		~Directed	();
};

// Main structes
class	Font : public Named {
 	public:
		DWORD			no;			// ?
		DWORD			Height;
		DWORD			Width;
		DWORD			Escapement;
		DWORD			Weight;
		bool			Italic;
		bool			Underline;
		bool			StrikeOut;
		BYTE			CodePage;		// Code page
		BYTE			OutPrecision;		// 3
		BYTE			ClipPricision;		// 2
		BYTE			Quality;		// 1
		BYTE			PitchAndFamily;
		// functions
		Font	();
		Font	(const RC);
		Font	(const Font &);
		~Font	();
};

class	HeaderFooter : public ExtProps {
	public:
		// functions
		HeaderFooter	();
		HeaderFooter	(const HeaderFooter &);
		~HeaderFooter	();
};

class	Table : public Props {
	public:
		// functions
		Table	();
		Table	(const Table &);
		~Table	();
};

class	Column : public ExtProps {
 	public:
		RC			no;
	// members
		Column	();
		Column	(const RC);
		Column	(const Column &);
		~Column	();
};

class	Row : public Props {
 	public:
		RC			no;
		// members
		Row	();
		Row	(const RC);
		Row	(const Row &);
		~Row	();
};

class	Cell : public ExtProps {
 	public:
		RC			row;
		RC			col;
		Cell	();
		Cell	(const RC);
		Cell	(const Cell &);
		~Cell	();
};

class	Line : public Obj {
	public:
		Line	();
		Line	(const Line &);
		~Line	();
};

class	Rect : public Obj {
	public:
		Rect	();
		Rect	(const Rect &);
		~Rect	();
};

class	Frame : public Obj {
	public:
		Frame	();
		Frame	(const Frame &);
		~Frame	();
};

class	Picture : public Obj, public Bulk {
	public:
		Picture	();
		Picture	(const Picture &);
		~Picture	();
};

class	Diagram : public Obj, public Named, public Bulk {
	public:
		Diagram	();
		Diagram	(const Diagram &);
		~Diagram	();
};

class	OLE : public Obj, public Bulk {
	public:
		OLE	();
		OLE	(const OLE &);
		~OLE	();
};

class	Join : public Region {
	public:
		Join	();
		Join	(const Join &);
		~Join	();
};

class	Section : public Named, public Directed {
 	public:
		RC			Start;
		RC			End;
		DWORD			Parent;
		Section	();
		Section	(const Section &);
		~Section	();
};

class	NamedRegion : public Region, public Named {
	public:
		NamedRegion	();
		NamedRegion	(const NamedRegion &);
		~NamedRegion	();
};

class	FormFeed : public Directed {
	public:
		DWORD			no;
		FormFeed	();
		FormFeed	(const FormFeed &);
		~FormFeed	();
};

// support for map struct
//struct ltdw { bool operator()(const DWORD i1, const DWORD i2) const { return i1 < i2; } };
// The Main container

typedef map <DWORD, Font>	mFont;
typedef map <DWORD, Column>	mColumn;
typedef map <DWORD, Row>	mRow;
typedef vector <Cell>		vCell;
typedef vector <Obj>		vObject;
typedef vector <Join>		vJoin;
typedef vector <Section>	vSection;
typedef vector <NamedRegion>	vNamedRegion;
typedef vector <FormFeed>	vFormFeed;

class	Moxel {
	public:
		DWORD			ver;
		mFont			font;
		HeaderFooter		header;
		HeaderFooter		footer;
		Table			table;
		mColumn			col;
		mRow			row;
		vector <Cell>		cell;
		vector <Obj>		obj;
		vector <Join>		join;
		vector <Section>	sect;
		vector <NamedRegion>	named;
		vector <FormFeed>	ff;
		// utility
		//char			*strings;
		// functions
		Moxel();
		Moxel(Moxel &);
		~Moxel();
};

void	test(const char*, const Moxel &);

#endif
