/***************************************************************************
 *            mxl.h
 *
 *  Fri Feb 27 11:52:56 2004
 *  Copyright  2004  eugene
 *  eugene@admincomp.spb.rosgazservice.com
 ****************************************************************************/

/*
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Library General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 */
 
 /* (c) Eugene A. Pivnev mailto:eugene@spb.rosgazservice.com
 	Using Dmitry Pavlyuk hard work results
*/
#ifndef	_MXL_H
#define _MXL_H
#include <sys/types.h>

#pragma pack(1)
/*#ifdef __BORLANDC__
typedef unsigned char	BYTE;
typedef unsigned short	WORD;
typedef unsigned long	DWORD;
#else
typedef __uint8_t	BYTE;
typedef __uint16_t	WORD;
typedef __uint32_t	DWORD;
#endif*/

// 1.1. Atomic structs

struct	MXL_NumbersBlock	{
	WORD			Qty;		// Numbers quantity
	DWORD			Number[];	// subj
};

struct	MXL_PString	{			// Pascal-like string
	WORD			Len;		// String len (in Word, if BLen = 0xFF)
	char			*Text;		// subj
};

struct	MXL_Prop	{			// Table, Row, Column & Cell common Props
	DWORD			Flag;		// NoAuto & Defined bit flags	
	WORD			Height;		// Row height in 1/8th of u.e.
	WORD			Width;		// Col width in 1/4th of u.e.
	WORD			FontN;		// Font.Number
	WORD			FontS;		// Font.Size = -4*pt
	BYTE			FontB;		// Font.Bold status
	BYTE			FontI;		// Font.Italic status
	BYTE			FontU;		// Font.Underline status
	BYTE			PosHA;		// Position.HorisontalAllign
	BYTE			PosVA;		// Position.VerticalAllign
	BYTE			PatType;	// Pattern.Type
	BYTE			FrameL;		// Frame.Left
	BYTE			FrameT;		// Frame.Top
	BYTE			FrameR;		// Frame.Right
	BYTE			FrameB;		// Frame.Bottom
	BYTE			PatColor;	// Pattern.Color
	BYTE			FrameColor;	// Frame.Color
	BYTE			FontColor;	// Font.Color
	BYTE			BGColor;	// Background color
	BYTE			TextCtrl;	// Text.Control ...
	BYTE			TextType;	// Text.Type
	BYTE			TextProt;	// Text.Protection status (new in v.6+), optional
	BYTE			Unknown0;	// ? (new in v.6+), optional
	WORD			Angle;		// Angle (new in v.6+ (7.70.025+)), optional
};

/*// Dialog props
struct	MXL_DP_1	{
	BYTE			...;
	BYTE			...;
	BYTE			...;
	BYTE			...;
	BYTE			...;
};

struct	MXL_DP_2	{
	
};

struct	MXL_DProp	{
	MXL_DP_1		*Prop1;
	MXL_PString		Text;		// ! if Text defined; if not = NULL
	MXL_PString		Desc;		// ! if Description defined; if not = NULL
	MXL_DP_2		*Prop2;
	MXL_PString		Text;		// ! if Text defined; if not = NULL
};
*/
struct	MXL_ExtProp	{
	MXL_Prop		*Prop;		// Standard props
	MXL_PString		Text;		// ! if Text defined; if not = NULL
	MXL_PString		Desc;		// ! if Description defined; if not = NULL
//	MXL_DProp		DProp;		// Dialog props - added 4822
};

// Used structures
// 2.1. Header
struct	MXL_Head	{			// MXL-file header; 25 bytes
	char			Signature[6];	// For "MOXCEL"
	BYTE			Unknown0[5];	// ? zeros; may be MOXCEL\0<DWORD> ?
	WORD			Version;	// ? 0x0006
	DWORD			ColQty;		// Columns quantity
	DWORD			RowQty;		// Rows quantity
	DWORD			ObjQty;		// Objects quantity
};
// 2.2. Font
struct	MXL_FontProp	{			// Font Props, 60 bytes
	DWORD			Height;
	DWORD			Width;
	DWORD			Escapement;
	DWORD			Orientation;
	DWORD			Weight;
	BYTE			Italic;
	BYTE			Underline;
	BYTE			StrikeOut;
	BYTE			CodePage;		// Code page
	BYTE			OutPrecision;		// 3
	BYTE			ClipPricision;		// 2
	BYTE			Quality;		// 1
	BYTE			PitchAndFamily;
	BYTE			FontName[32];	// Font name + \0 + Trash
};

struct	MXL_Font	{
	MXL_NumbersBlock	*NB;
	WORD			*Qty;		// Props quantity
	MXL_FontProp		*Prop;
};

// 2.4. Rows (/w Cells)
struct	MXL_Cell	{
	MXL_NumbersBlock	*NB;
	WORD			*Qty;
	MXL_ExtProp		*Prop;		// !!! alloc mem
};

struct	MXL_RowProp	{
	MXL_Prop		*Prop;
	MXL_Cell		Cell;
};

struct	MXL_Row	{
	MXL_NumbersBlock	*NB;
	WORD			*Qty;
	MXL_RowProp		*Prop;		// !!! alloc
};

// 2.5. Objects
struct	MXL_Bulk	{
	DWORD			Len;		// Data len
	BYTE			Data[];		// ?
};

struct	MXL_Pic	{
	DWORD			Unknown0;	// ? 0x0000746C
	MXL_Bulk		Bulk;
};

struct	MXL_OLEName	{
	WORD			Unknown0;	// 0
	WORD			NameLen;	// OLE name len - 0x000E allways
	char			Name[14];	// OLE name - "CSheetCntrItem" always
};

struct	MXL_OLETrash	{
	DWORD			Unknown1;	// 0x00000100
	DWORD			Unknown2;	// ?
	DWORD			Unknown3;	// 1-OLE/0x0012f150-Dia
	WORD			Unknown4;	// 0
	DWORD			Unknown5;	// 1
};

struct	MXL_OLE	{
	WORD			*Unknown0;	// 0xFFFF/0x8001
	MXL_OLEName		*Name;		// !!! Option !!!
	MXL_OLETrash		*Trash;
	MXL_Bulk		*Bulk;
};

struct	MXL_ExtObjProp	{
	DWORD			Type;		// Object type
	DWORD			Col0;		// Start column
	DWORD			Row0;		// Start row
	DWORD			X0;		// Start X-coordinate
	DWORD			Y0;		// Start Y-coordinate
	DWORD			Col1;		// End column
	DWORD			Row1;		// End row
	DWORD			X1;		// End X-coordinate
	DWORD			Y1;		// End Y-coordinate
	DWORD			Level;		// Plan level ?
};

struct	MXL_ObjProp	{
	MXL_ExtProp		Prop;		// common cell props
	MXL_ExtObjProp		*ExtProp;	// extended obj props - type, coords, level
	MXL_Pic			*Pic;		// if it is picture
	MXL_OLE			*OLE;		// if it is OLE
};

struct	MXL_Obj	{
	WORD			*Qty;
	MXL_ObjProp		*Prop;		// !!! alloc
};

// 2.6. Joins
struct	MXL_JoinProp	{
	DWORD			Col0;		// Start column
	DWORD			Row0;		// Start row
	DWORD			Col1;		// End column
	DWORD			Row1;		// End row
};

struct	MXL_Join	{
	WORD			Qty;
	MXL_JoinProp		Prop[];
};

// 2.7. Sections
struct	MXL_SectData	{
	DWORD			Beg;		// Start row|column
	DWORD			End;		// End row|column
	WORD			Parent;		// If is included in other group = number of this group
	WORD			Unknown0;	// 0
};
struct	MXL_SectProp	{
	MXL_SectData		*Prop;
	MXL_PString		Name;
};

struct	MXL_Sect	{
	WORD			*Qty;
	MXL_SectProp		*Prop;		// !!! alloc
};

// 2.8. FormFeeds
struct	MXL_FormFeed	{
	WORD			Qty;
	DWORD			RowCol[];	// Row|Col number
};

// 2.9. Names
struct	MXL_NameData	{
	DWORD			Unknown0;	// ? 00 00 00 01
	DWORD			Unknown1;	// ? 00 12 F9 E8
	DWORD			Unknown2;	// ? 00 00 00 03
	DWORD			Col0;		// Start column
	DWORD			Row0;		// Start row
	DWORD			Col1;		// End column
	DWORD			Row1;		// End row
};

struct	MXL_NameProp	{
	MXL_PString		Name;
	MXL_NameData		*Prop;
};

struct	MXL_Name	{
	DWORD			*Qty;
	MXL_NameProp		*Prop;		// !!! alloc
};

// 3. Whole file
struct	MXL	{
	MXL_Head		*Head;
	MXL_Prop		*Table;
	MXL_Font		Font;
	DWORD			*Unknown0;
	MXL_ExtProp		Header;
	MXL_ExtProp		Footer;
	MXL_Cell		Column;
	MXL_Row			Row;
	MXL_Obj			Obj;
	WORD			*Unknown1;	// v.2: WORD?
	MXL_Join		*Join;
	MXL_Sect		VSect;
	MXL_Sect		HSect;
	MXL_FormFeed		*VFormFeed;
	MXL_FormFeed		*HFormFeed;
	MXL_Name		Name;		// v.2: absent
};

enum	mxlver	{ver2, ver6, ver7};

#endif
