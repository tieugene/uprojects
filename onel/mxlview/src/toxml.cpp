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

// mxl_out.cpp
// out mxl block into stdout
// TODO: dump bin data

//#include	<stdio.h>
//#include	<iostream>
//#include	<fstream>
//#include	<string>
//#include	<vector>
//#include	<map>

#include	"common.h"
#include	"core.h"
#include	"toxml.h"

static	char tmp[22];
string	hex02(const BYTE a)	{ sprintf(tmp, "%02X", a);	return string(tmp); }
string	hex04(const WORD a)	{ sprintf(tmp, "%04X", a);	return string(tmp); }
string	hex08(const DWORD a)	{ sprintf(tmp, "%08X", a);	return string(tmp); }

string	cT(void)		{ return (string(">\n")); }
string	oNode(const char *s)	{ return (string("<") + string(s)); }			// open node
string	cNode(const char *s)	{ return (string("</") + string(s) + string(">\n")); }	// close node
string	cNode(void)		{ return (string("/>\n")); }				// close tag
string	oParm(const char *name)	{ return (string(" ") + name + "=\""); }
string	cParm(void)		{ return (string("\"")); }

// string	dump_bulk(MXL_Bulk *b) {
// 	Pdata	d;
// 	string fn = hex04(bulkcount++);
// 
// 	d.size = b->Len;
// 	d.data = b->Data;
// 	dump_data(d, dBulk, fn);
// 	return fn;
// }

string	ocBYTEs(const char *name, const BYTE *b, const BYTE cnt)	{
	string	s = oParm(name);
	for (BYTE i = 0; i < cnt; i++)
		s = s + hex02(b[i]) + " ";
	s += cParm();
	return (s);
}

string	ocString(const char *title, const string &text)	{
	string	s;

	s += oParm(title);
	for (DWORD i = 0; i < text.size(); i++)	{
		switch(text[i])	{
			case '"':
				s += "&quot;";
				break;
			case '&':
				s += "&amp;";
				break;
			case '<':
				s += "&lt;";
				break;
			case '>':
				s += "&gt;";
				break;
			default:
				s += text[i];
		}
	}
	s += cParm();
	return (s);
}

void	Export_Font(const Font &data, fstream &ofile) {
	ofile
	<< oNode("fnt")
	<< oParm("n") << data.no << cParm()
	<< oParm("h") << data.Height << cParm()
	<< oParm("w") << data.Width << cParm()
	<< oParm("esc") << data.Escapement << cParm()
//	<< oParm("dir") << data.Orientation << cParm()
	<< oParm("b") << data.Weight << cParm()
	<< oParm("i") << data.Italic << cParm()
	<< oParm("u") << data.Underline << cParm()
	<< oParm("so") << data.StrikeOut << cParm()
	<< oParm("cp") << int(data.CodePage) << cParm()		// FIXME:
	<< oParm("opr") << int(data.OutPrecision) << cParm()	// FIXME:
	<< oParm("cpr") << int(data.ClipPricision) << cParm()	// FIXME:
	<< oParm("pf") << int(data.PitchAndFamily) << cParm()	// FIXME:
	<< ocString("fnm", data.Name)
	<< cNode();
}

void	Export_Props(const char *title, const Props &f, fstream &ofile)	{
	ofile
	<< oNode(title)
//	<< oParm("flg")	<< hex08(f.Flag)	<< cParm()
	<< oParm("h")	<< f.size.height	<< cParm()	// u.e.
	<< oParm("w")	<< f.size.width		<< cParm();	// u.e.
	if (f.defined.backgroundcolor)
		ofile << oParm("bgc")	<< int(f.background.color)	<< cParm();	// FIXME:
	if (f.defined.fontname)
		ofile << oParm("fnm")	<< f.font.number	<< cParm();
	if (f.defined.fontsize)
		ofile << oParm("fsz")	<< f.font.size		<< cParm();
	if (f.defined.fontbold)
		ofile << oParm("fb")	<< f.font.bold		<< cParm();
	if (f.defined.fontitalic)
		ofile << oParm("fi")	<< f.font.italic	<< cParm();
	if (f.defined.fontunderline)
		ofile << oParm("fu")	<< f.font.underline	<< cParm();
	if (f.defined.fontcolor)
		ofile << oParm("fc")	<< f.font.color		<< cParm();
	if (f.defined.hallign)
		ofile << oParm("ha")	<< f.allign.h		<< cParm()
		      << oParm("os")	<< f.allign.onselected	<< cParm();
	if (f.defined.vallign)
		ofile << oParm("va")	<< f.allign.v		<< cParm();
	if (f.defined.patterntype)
		ofile << oParm("pt")	<< f.pattern.type	<< cParm();
	if (f.defined.patterncolor)
		ofile << oParm("pc")	<< f.pattern.color	<< cParm();
	if (f.defined.frameleft)
		ofile << oParm("frl")	<< int(f.frame.left)	<< cParm();	// FIXME:
	if (f.defined.frametop)
		ofile << oParm("frt")	<< int(f.frame.top)	<< cParm();	// FIXME:
	if (f.defined.frameright)
		ofile << oParm("frr")	<< int(f.frame.right)	<< cParm();	// FIXME:
	if (f.defined.framebottom)
		ofile << oParm("frb")	<< int(f.frame.bottom)	<< cParm();	// FIXME:
	if (f.defined.framecolor)
		ofile << oParm("frc")	<< f.frame.color	<< cParm();
	if (f.defined.txtctrl)
		ofile << oParm("tc")	<< f.txtprop.control	<< cParm();
	if (f.defined.txttype)
		ofile << oParm("tt")	<< f.txtprop.type	<< cParm();
	//if (ver >= ver6)
	if (f.defined.txtprot)
		ofile	<< oParm("tp")	<< f.txtprop.protection	<< cParm();
	//if (ver == ver7)
		ofile	<< oParm("ang") << f.angle << cParm();
}

void	Export_ExtProps(const char *title, const ExtProps &f, fstream &ofile)	{
	Export_Props(title, f, ofile);
	if (f.defined.text)
		ofile << ocString("txt", f.Text);
	if (f.defined.description)
		ofile << ocString("dsc", f.Description);
}

void	Export_Obj(const char *title, const Obj &f, fstream &ofile)	{
	Export_ExtProps(title, f, ofile);
	ofile
	<< oParm("typ")	<< f.Type	<< cParm()
	<< oParm("c0")	<< f.C0	<< cParm()
	<< oParm("r0")	<< f.R0	<< cParm()
	<< oParm("x0")	<< f.X0	<< cParm()
	<< oParm("y0")	<< f.Y0	<< cParm()
	<< oParm("c1")	<< f.C1	<< cParm()
	<< oParm("r1")	<< f.R1	<< cParm()
	<< oParm("x1")	<< f.X1	<< cParm()
	<< oParm("y1")	<< f.Y1	<< cParm()
	<< oParm("lvl")	<< f.Level	<< cParm();
/*	if (f.ExtProp->Type == 4)	{					// OLE
		ofile << oParm("u1") << DWORD(*f.OLE->Unknown0) << cParm();
		if (*f.OLE->Unknown0 == 0xFFFF)	{
			ofile
				<< oParm("nmlen") << f.OLE->Name->NameLen << cParm()
				<< ocNString("nmtxt", f.OLE->Name->Name, f.OLE->Name->NameLen);
		}
		ofile
			<< oParm("blen") << f.OLE->Bulk->Len << cParm();
		if (f.OLE->Bulk->Len)	// 5617 - dumping data
			ofile << oParm("file") << dump_bulk(f.OLE->Bulk) << cParm();
	}
	else if (f.ExtProp->Type == 5)	{					// Picture
		ofile
			<< oParm("blen") << f.Pic->Bulk.Len << cParm();
		if (f.Pic->Bulk.Len)	// 5617 - dumping data
			ofile << oParm("file") << dump_bulk(&f.Pic->Bulk) << cParm();
	}*/
}

void	Export_Join(const Join &data, fstream &ofile)	{
	ofile << oNode("join")
		<< oParm("c0") << data.C0 << cParm()
		<< oParm("r0") << data.R0 << cParm()
		<< oParm("c1") << data.C1 << cParm()
		<< oParm("r1") << data.R1 << cParm()
		<< cNode();
}

void	Export_Sect(const Section &data, fstream &ofile)	{
	ofile << oNode("sec")
		<< oParm("b") << data.Start << cParm()
		<< oParm("e") << data.End << cParm()
		<< oParm("p") << data.Parent << cParm()
		<< ocString("nm", data.Name)
		<< cNode();
}

void	Export_FF(const FormFeed &data, fstream &ofile)	{
	ofile << oNode("ff")
		<< oParm("n") << data.no << cParm()
		<< cNode();
}

void	Export_Name(const NamedRegion &data, fstream &ofile)	{
	ofile << oNode("name")
		<< ocString("nm", data.Name)
		<< oParm("c0") << data.C0 << cParm()
		<< oParm("r0") << data.R0 << cParm()
		<< oParm("c1") << data.C1 << cParm()
		<< oParm("r1") << data.R1 << cParm()
		<< cNode();
}
// function 2 out MXL struct into XML
// @parm:
//	@param data - struct itself
//	@param dir - where dump bin data to
//	@param filename - name of mxl-file
void	Export_XML (const Moxel & inputobject)	{
	WORD	i, imax, j;
	char	*oname;
	static char	*onames[] = {"objl", "objr", "objt", "objo", "objp"};
	string	sfile;
	fstream	ofile;

//test("Start export", inputobject);
	ofile.open("mxl.xml", ios::binary | ios::out);
	// end prepare
	ofile
		<< "<?xml version = '1.0' encoding = 'windows-1251'?>" << endl
		<< "<!DOCTYPE tml SYSTEM \"tml.dtd\">" << endl
		<< oNode ("tml")
		// Head
		<< oParm ("ver") << inputobject.ver << cParm() << cT();
	// Table prop
	Export_Props("tbl", inputobject.table, ofile); ofile << cNode();
	// Fonts
	for (mFont::const_iterator FontIter = inputobject.font.begin(); FontIter != inputobject.font.end(); FontIter++)
		Export_Font(FontIter->second, ofile);
	// Header prop
	Export_ExtProps("tblh", inputobject.header, ofile); ofile << cNode();
	// Footer prop
	Export_ExtProps("tblf", inputobject.footer, ofile); ofile << cNode();
// Дальше - segfault
	// Colums
//cout << "Out cols" << endl;
	for (mColumn::const_iterator Iter = inputobject.col.begin(); Iter != inputobject.col.end(); Iter++) {
		Export_ExtProps("col", Iter->second, ofile);
		ofile << oParm("n") << Iter->second.no << cParm()
		<< cNode();
	}
	// Rows
//cout << "Out rows" << endl;
	for (mRow::const_iterator Iter = inputobject.row.begin(); Iter != inputobject.row.end(); Iter++) {
		Export_Props("row", Iter->second, ofile);
		ofile << oParm("n") << Iter->second.no << cParm()
		<< cNode();
	}
	// Cells
//cout << "Out cells" << endl;
//	for (i = 0; i < inputobject.cell.size(); i++)	{
//		Export_ExtProps("cell", inputobject.cell[i], ofile);
//		ofile << oParm("r") << inputobject.cell[i].row << cParm()
//		<< oParm("c") << inputobject.cell[i].col << cParm()
	for (vCell::const_iterator Iter = inputobject.cell.begin(); Iter != inputobject.cell.end(); Iter++) {
		Export_ExtProps("cell", *Iter, ofile);
		ofile << oParm("r") << Iter->row << cParm()
		<< oParm("c") << Iter->col << cParm()
		<< cNode();
	}
	// Objs
//cout << "Out objs" << endl;
	for (vObject::const_iterator Iter = inputobject.obj.begin(); Iter != inputobject.obj.end(); Iter++) {
cout << Iter->Type << endl;
//		oname = onames[Iter->Type - 1];	// FIXME: хня всякое... 0 или дофега
		oname = onames[1];
		Export_Obj(oname, *Iter, ofile);
		ofile << cNode();
	}
	// Joins
//goto TheEnd;
//cout << "Out joins" << endl;
	for (vJoin::const_iterator Iter = inputobject.join.begin(); Iter != inputobject.join.end(); Iter++)
		Export_Join(*Iter, ofile);
	// Sections
	for (vSection::const_iterator Iter = inputobject.sect.begin(); Iter != inputobject.sect.end(); Iter++)
		Export_Sect(*Iter, ofile);
	// FFs
	for (vFormFeed::const_iterator Iter = inputobject.ff.begin(); Iter != inputobject.ff.end(); Iter++)
		Export_FF(*Iter, ofile);
	// Names
//	if (ver >= ver6) {
	for (vNamedRegion::const_iterator Iter = inputobject.named.begin(); Iter != inputobject.named.end(); Iter++)
		Export_Name(*Iter, ofile);
//TheEnd:
	ofile << cNode ("tml");
	ofile.close();
}
