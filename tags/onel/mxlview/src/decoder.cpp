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

/*!	\file decoder.cpp
	decode parsed mxl into core object
	TODO: init core objects by constructors
*/

#include "common.h"
#include "parser.h"
#include "core.h"
#include "decoder.h"

static	mxlver	ver;		// flag to show that it's v.7 MXL - w/ angle field
static	char *strptr;		// current string buffer pointer

union	UnionFlag	{
	Props::TypeFlag	out;
	DWORD		in;
}	FlagConvert;

// ===	utility
/*!	Store bulk data into Obj.Data
*/
void	dump_bulk(MXL_Bulk *data, Bulk &out) {
	if (data->Len) {
		out.Data = new BYTE[data->Len];
		memcpy(data->Data, out.Data, data->Len);
	} else
		out.Data = NULL;
}

/*!	Convert P-string into strng
*/
void	PS2S(const MXL_PString &data, string &out)	{
	//out = strncpy(strptr, data.Text, data.Len);
	//strptr += (data.Len + 1);
	char *p = data.Text;
	for (int i = 0; i < data.Len; i++)
		out += *p++;
}

// ===	decoders
/*!	Decode MXL_Font into Font
*/
Font	DecodeFont(const int no, const MXL_FontProp &data, Font &out) {
//	Font	out = Font();
//return (out);
	out.no			= no;
	out.Height		= data.Height;
	out.Width		= data.Width;
	out.Escapement		= data.Escapement;
	out.Weight		= data.Weight;
	out.Italic		= bool(data.Italic);
	out.Underline		= bool(data.Underline);
	out.StrikeOut		= bool(data.StrikeOut);
	out.CodePage		= BYTE(data.CodePage);
	out.OutPrecision	= BYTE(data.OutPrecision);
	out.ClipPricision	= BYTE(data.ClipPricision);
	out.PitchAndFamily	= BYTE(data.PitchAndFamily);
//	out.Name = strcpy(strptr, data.FontName);
	//out.Name		= data.FontName;
//	strptr += (strlen(data.FontName) + 1);

	return(out);
}

/*!	Decode properties into Prop
*/
void	DecodeProps(const MXL_Prop *data, Props &out)	{
	FlagConvert.in		= data->Flag;
	out.defined		= FlagConvert.out;
	out.size.height		= data->Height/4;	// u.e.
	out.size.width		= data->Width/8;	// u.e.
	if (out.defined.backgroundcolor)
		out.background.color	= WORD(data->BGColor);
	if (out.defined.fontname)
		out.font.number		= data->FontN;
	if (out.defined.fontsize)
		out.font.size		= (data->FontS) ? (0xFFFF-data->FontS+1)/4 : 0;
	if (out.defined.fontbold)
		out.font.bold		= (data->FontB == 7);
	if (out.defined.fontitalic)
		out.font.italic		= bool(data->FontI);
	if (out.defined.fontunderline)
		out.font.underline	= bool(data->FontU);
	if (out.defined.fontcolor)
		out.font.color		= BYTE(data->FontColor);
	if (out.defined.hallign) {
		switch (data->PosHA & 0x1F) {		// was: out.Allign.H = BYTE(data->PosHA);
			case(0):
				out.allign.h = Props::TypeAllign::Left;
				break;
			case(2):
				out.allign.h = Props::TypeAllign::Right;
				break;
			case(4):
				out.allign.h = Props::TypeAllign::Width;
				break;
			case(6):
				out.allign.h = Props::TypeAllign::HCenter;
				break;
			default:
				cerr << "Bad HAllign: " << data->PosHA << endl;
				break;
		}
		out.allign.onselected	= bool(data->PosHA & 0x20);
	}
	if (out.defined.vallign)
		switch (data->PosVA) {		// was: out.Allign.V = BYTE(data->PosVA);
			case(0):
				out.allign.v = Props::TypeAllign::Top;
				break;
			case(0x08):
				out.allign.v = Props::TypeAllign::Bottom;
				break;
			case(0x18):
				out.allign.v = Props::TypeAllign::VCenter;
				break;
			default:
				cerr << "Bad VAllign: " << data->PosHA << endl;
				break;
		}
	if (out.defined.patterntype)
		out.pattern.type	= BYTE(data->PatType);
	if (out.defined.patterncolor)
		out.pattern.color	= BYTE(data->PatColor);
	if (out.defined.frameleft)
		out.frame.left		= BYTE(data->FrameL);
	if (out.defined.frametop)
		out.frame.top		= BYTE(data->FrameT);
	if (out.defined.frameright)
		out.frame.right		= BYTE(data->FrameR);
	if (out.defined.framebottom)
		out.frame.bottom	= BYTE(data->FrameB);
	if (out.defined.framecolor)
		out.frame.color		= BYTE(data->FrameColor);
	if (out.defined.txtctrl)
		switch (data->TextCtrl) {		// was: out.TxtProp.Control	= BYTE(data->TextCtrl);
			case(0):
				out.txtprop.control = Props::TypeTxtProp::Auto;
				break;
			case(1):
				out.txtprop.control = Props::TypeTxtProp::Cut;
				break;
			case(2):
				out.txtprop.control = Props::TypeTxtProp::Stopup;
				break;
			case(3):
				out.txtprop.control = Props::TypeTxtProp::Wrap;
				break;
			case(4):
				out.txtprop.control = Props::TypeTxtProp::Red;
				break;
			case(5):
				out.txtprop.control = Props::TypeTxtProp::StopupAndRed;
				break;
			default:	// Can B 255
				cerr << "Bad TextCtrl: " << data->TextCtrl << endl;
				break;
		}
	if (out.defined.txttype)
		switch (data->TextType) {		// was: out.TxtProp.Type	= BYTE(data->TextType);
			case(0):
				out.txtprop.type = Props::TypeTxtProp::Text;
				break;
			case(1):
				out.txtprop.type = Props::TypeTxtProp::Expression;
				break;
			case(2):
				out.txtprop.type = Props::TypeTxtProp::Template;
				break;
			case(3):
				out.txtprop.type = Props::TypeTxtProp::FixedTemplate;
				break;
			default:
				cerr << "Bad TextType: " << data->TextType << endl;
				break;
		}
	if ((ver >= ver6) && out.defined.txtprot)
		out.txtprop.protection	= !(bool(data->TextProt));
	if (ver == ver7)				// ? defined
		out.angle	= WORD(data->Angle);
}

/*!	Decode extended properties into ExtProp
*/
void	DecodeExtProps(const MXL_ExtProp &data, ExtProps &out)	{
	DecodeProps(data.Prop, out);
	if (out.defined.text)
		PS2S(data.Text, out.Text);
	if (out.defined.description)
		PS2S(data.Desc, out.Description);
}

/*!	Decode object properties into Obj
*/
void	DecodeObjProps(const MXL_ObjProp &data, Obj &out)	{
	out.C0		= data.ExtProp->Col0;
	out.R0		= data.ExtProp->Row0;
	out.X0		= data.ExtProp->X0;
	out.Y0		= data.ExtProp->Y0;
	out.C1		= data.ExtProp->Col1;
	out.R1		= data.ExtProp->Row1;
	out.X1		= data.ExtProp->X1;
	out.Y1		= data.ExtProp->Y1;
	out.Level	= data.ExtProp->Level;
	switch (data.ExtProp->Type) {
		case (1):
			out.Type = Obj::Line;
			break;
		case (2):
			out.Type = Obj::Rectangle;
			break;
		case (3):
			out.Type = Obj::TextFrame;
			break;
		case (4):
			if (data.OLE->Trash->Unknown3 == 1)	// OLE
				out.Type = Obj::OLE;
			else					// Diagramm
				out.Type = Obj::Diagram;
	//		dump_bulk(data.OLE->Bulk, out);		// FIXME: некорректная инициализация ссылки типа ‘Bulk&’ из выражения типа ‘Obj’
			break;
		case (5):
			out.Type = Obj::Picture;
			break;
		default:
			cerr << "Bad Object type: " << data.ExtProp->Type << endl;
	}
}

Join	DecodeJoin(const MXL_JoinProp &data)	{
	Join	out = Join();
	out.C0 = data.Col0;
	out.R0 = data.Row0;
	out.C1 = data.Col1;
	out.R1 = data.Row1;
	return(out);
}

Section	DecodeSection(const MXL_SectProp &data, const bool dir)	{
	Section	out = Section();
	out.Direction	= dir;
	out.Start	= data.Prop->Beg;
	out.End		= data.Prop->End;
	out.Parent	= data.Prop->Parent;
	PS2S(data.Name, out.Name);
	return(out);
}

FormFeed	DecodeFormFeed(const DWORD &data, const bool dir)	{
	FormFeed	out = FormFeed();
	out.Direction	= dir;
	out.no		= data;
	return(out);
}

NamedRegion	DecodeNamed(const MXL_NameProp &data)	{
	NamedRegion	out = NamedRegion();
	PS2S(data.Name, out.Name);
	out.C0 = data.Prop->Col0;
	out.R0 = data.Prop->Row0;
	out.C1 = data.Prop->Col1;
	out.R1 = data.Prop->Row1;
	return (out);
}

// ===	main loop
// function 2 out MXL struct into XML
// @parm:
//	@param data - struct itself
//	@param dir - where dump bin data to
//	@param filename - name of mxl-file
bool	MXL_Decode (const MXL & data, Moxel &out)	{
	RC	i, imax, j, jmax, no, r, c;
	Column	col;
	Row	row;
	Cell	cell;
	Obj	obj;

//test("Start0 decode", out);
//cout << "[296] Cols: " << out.col.size() << endl;
	// prepare data
	// 1. strings
//	if (!(out.strings = new char[data.TotalChars + data.TotalStrings])) {
//		cout << "Can't alloc mem for strings" << endl;
//		return(false);
//	}
//	strptr = out.strings;
	// Lets go
	switch (data.Head->Version) {
		case(2):
		case(6):
		case(7):
			out.ver = data.Head->Version;
			break;
		default:
			cerr <<  "Unknown MXL version:" << data.Head->Version << endl;
			return (false);
	}
	// Table
//test("table", out);
	DecodeProps(data.Table, out.table);
	// Fonts
//test("fonts", out);
	imax = *data.Font.Qty;
	for (i = 0; i < imax; i++) {
		no = data.Font.NB->Number[i];
		Font f = Font();
		DecodeFont(no, data.Font.Prop[i], f);
		out.font.insert(make_pair(no, f));
		//out.font[no] = f;
	}
	// Header prop
//test("header", out);
	DecodeExtProps(data.Header, out.header);
	// Footer prop
//test("footer", out);
	DecodeExtProps(data.Footer, out.footer);
	// Colums
//test("columns", out);
//cout << "columns" << out.col.size() << "/" << imax << endl;
	imax = *data.Column.Qty;
//test("Start col", out);
	for (i = 0; i < imax; i++)	{
		col = Column();
		col.no = data.Column.NB->Number[i];
		DecodeExtProps(data.Column.Prop[i], col);
//cout << "in: " << out.col.size() << endl;
		out.col[col.no] = col;
//cout << "out: " << out.col.size() << endl;
	}
//test("End col", out);
//test("Start rows", out);
	// Rows
//test("rows", out);
	imax = *data.Row.Qty;
//cout << "Rows: " << imax << endl;
	for (i = 0; i < imax; i++)	{
		row = Row();
		row.no = data.Row.NB->Number[i];
		DecodeProps(data.Row.Prop[i].Prop, row);
		out.row[row.no] = row;
	}
//test("Start cells", out);
	// Cells
//test("cells", out);
	imax = *data.Row.Qty;
	for (i = 0; i < imax; i++)	{
//test("Start row", out);
		jmax = *data.Row.Prop[i].Cell.Qty;
		for (j = 0; j < jmax; j++)	{
			cell = Cell();
			cell.row = data.Row.NB->Number[i];
			cell.col = data.Row.Prop[i].Cell.NB->Number[j];
			DecodeExtProps(data.Row.Prop[i].Cell.Prop[j], cell);
//test("Start cell insert", out);
			out.cell.push_back(cell);
//test("End cell insert", out);
		}
	}
//test("objs", out);
	// Objs
	for (i = 0; i < *data.Obj.Qty; i++)	{
		obj = Obj();
		DecodeExtProps(data.Obj.Prop[i].Prop, obj);
		DecodeObjProps(data.Obj.Prop[i], obj);
//cout << obj.Type << endl;
		out.obj.push_back(obj);
	}
	// Joins
//test("joins", out);
	for (i = 0; i < data.Join->Qty; i++)
		out.join.push_back(DecodeJoin(data.Join->Prop[i]));
	// VSects
//test("joins", out);
	for (int i = 0; i < *data.VSect.Qty; i++)
		out.sect.push_back(DecodeSection(data.VSect.Prop[i], true));
	// HSects
//test("hsect", out);
	for (int i = 0; i < *data.HSect.Qty; i++)
		out.sect.push_back(DecodeSection(data.HSect.Prop[i], false));
	// VFFs
//test("vffs", out);
	for (int i = 0; i < data.VFormFeed->Qty; i++)
		out.ff.push_back(DecodeFormFeed(data.VFormFeed->RowCol[i], true));
	// HFFs
//test("hffs", out);
	for (int i = 0; i < data.HFormFeed->Qty; i++)
		out.ff.push_back(DecodeFormFeed(data.HFormFeed->RowCol[i], true));
	// Names
//test("named", out);
	if (ver >= ver6) {
		for (DWORD i = 0; i < *data.Name.Qty; i++)	{
			out.named.push_back(DecodeNamed(data.Name.Prop[i]));
		}
	}
//test("End decode", out);
	return (true);
}
