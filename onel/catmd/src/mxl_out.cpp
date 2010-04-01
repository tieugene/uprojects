// mxl_out.cpp
// out mxl block into stdout
// TODO: dump bin data

#include "catmd.h"

//extern fstream ofile;
extern string dRoot;

static fstream ofile;
static	mxlver	ver;		// flag to show that it's v.7 MXL - w/ angle field
static	WORD	bulkcount = 0;

string	cT(void)		{ return (string(">\n")); }
string	oNode(char *s)		{ return (string("<") + string(s)); }			// open node
string	cNode(char *s)		{ return (string("</") + string(s) + string(">\n")); }	// close node
string	cNode(void)		{ return (string("/>\n")); }				// close tag
string	oParm(char *name)	{ return (string(" ") + name + "=\""); }
string	cParm(void)		{ return (string("\"")); }

string	dump_bulk(MXL_Bulk *b) {
	Pdata	d;
	string fn = hex04(bulkcount++);

	d.size = b->Len;
	d.data = b->Data;
	dump_data(d, dBulk, fn);
	return fn;
}

// ****
// string	ocNB(MXL_NumbersBlock *nb)	{	// out NumberBlock
// 	WORD	i;
// 	string	s;
// 
// 	s = s
// 		+ oNode("NB")
// 		+ oParm("Qty")
// 		+ i2s(nb->Qty)
// 		+ cParm();
// 	if (nb->Qty)	{
// 		cT();
// 		for (i = 0; i < nb->Qty; i++)	{
// 			s = s + cNode("Num") + oParm("val") + i2s(nb->Number[i]) + cParm() + cNode();
// 		}
// 		s += cNode("NB");
// 	}
// 	else
// 		s += cNode();
// 	return (s);
// }

string	ocBYTEs(char *name, BYTE *b, BYTE cnt)	{
	string	s = oParm(name);
	for (BYTE i = 0; i < cnt; i++)
		s = s + hex02(b[i]) + " ";
	s += cParm();
	return (s);
}

string	ocNString(char *title, char text[], WORD len)	{
	WORD	i;
	string	s;

	if (len)	{
		s += oParm(title);
		for (i = 0; i < len; i++)	{
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
	}
	return (s);
}

string	ocPString(char *title, MXL_PString &text)	{
	return (ocNString(title, text.Text, text.Len));
}

void	PrintProps(char *title, MXL_Prop *f)	{
	ofile
	<< oNode(title)
	<< oParm("flg")	<< hex08(f->Flag)	<< cParm()
	<< oParm("h")	<< f->Height/4	<< cParm()	// u.e.
	<< oParm("w")	<< f->Width/8	<< cParm()	// u.e.
	<< oParm("bgc")	<< WORD(f->BGColor)	<< cParm()
	<< oParm("fnm")	<< f->FontN	<< cParm()
	<< oParm("fsz")	<< i2s((f->FontS) ? (0xFFFF-f->FontS+1)/4 : 0) << cParm()
	<< oParm("fb")	<< WORD(f->FontB)	<< cParm()
	<< oParm("fi")	<< WORD(f->FontI)	<< cParm()
	<< oParm("fu")	<< WORD(f->FontU)	<< cParm()
	<< oParm("fc")	<< WORD(f->FontColor)	<< cParm()
	<< oParm("ha")	<< WORD(f->PosHA)	<< cParm()
	<< oParm("va")	<< WORD(f->PosVA)	<< cParm()
	<< oParm("pt")	<< WORD(f->PatType)	<< cParm()
	<< oParm("pc")	<< WORD(f->PatColor)	<< cParm()
	<< oParm("frl")	<< WORD(f->FrameL)	<< cParm()
	<< oParm("frt")	<< WORD(f->FrameT)	<< cParm()
	<< oParm("frr")	<< WORD(f->FrameR)	<< cParm()
	<< oParm("frb")	<< WORD(f->FrameB)	<< cParm()
	<< oParm("frc")	<< WORD(f->FrameColor)	<< cParm()
	<< oParm("tc")	<< WORD(f->TextCtrl)	<< cParm()
	<< oParm("tt")	<< WORD(f->TextType)	<< cParm();
	if (ver >= ver6)
		ofile
			<< oParm("tp")	<< WORD(f->TextProt)	<< cParm()
			<< oParm("u0")	<< hex02(f->Unknown0)	<< cParm();
	if (ver == ver7)
		ofile
			<< oParm("ang") << WORD(f->Angle) << cParm();
}

void	PrintExtProps(char *title, MXL_ExtProp &f)	{
	PrintProps(title, f.Prop);
	ofile
		<< ocPString("txt", f.Text)
		<< ocPString("dsc", f.Desc);
}

void	PrintObjProps(MXL_ObjProp &f)	{
	ofile
	<< oParm("typ")	<< f.ExtProp->Type	<< cParm()
	<< oParm("c0")	<< f.ExtProp->Col0	<< cParm()
	<< oParm("r0")	<< f.ExtProp->Row0	<< cParm()
	<< oParm("x0")	<< f.ExtProp->X0	<< cParm()
	<< oParm("y0")	<< f.ExtProp->Y0	<< cParm()
	<< oParm("c1")	<< f.ExtProp->Col1	<< cParm()
	<< oParm("r1")	<< f.ExtProp->Row1	<< cParm()
	<< oParm("x1")	<< f.ExtProp->X1	<< cParm()
	<< oParm("y1")	<< f.ExtProp->Y1	<< cParm()
	<< oParm("lvl")	<< f.ExtProp->Level	<< cParm();
	if (f.ExtProp->Type == 4)	{					// OLE
		ofile << oParm("u1") << DWORD(*f.OLE->Unknown0) << cParm();
		if (*f.OLE->Unknown0 == 0xFFFF)	{
			ofile
				<< oParm("nmu0") << f.OLE->Name->Unknown0 << cParm()
				<< oParm("nmlen") << f.OLE->Name->NameLen << cParm()
				<< ocNString("nmtxt", f.OLE->Name->Name, f.OLE->Name->NameLen);
		}
		ofile
			<< oParm("u2") << f.OLE->Trash->Unknown1 << cParm()
			<< oParm("u3") << f.OLE->Trash->Unknown2 << cParm()
			<< oParm("u4") << f.OLE->Trash->Unknown3 << cParm()
			<< oParm("u5") << f.OLE->Trash->Unknown4 << cParm()
			<< oParm("u6") << f.OLE->Trash->Unknown5 << cParm()
			<< oParm("blen") << f.OLE->Bulk->Len << cParm();
		if (f.OLE->Bulk->Len)	// 5617 - dumping data
			ofile << oParm("file") << dump_bulk(f.OLE->Bulk) << cParm();
	}
	else if (f.ExtProp->Type == 5)	{					// Picture
		ofile
			<< oParm("u1") << f.Pic->Unknown0 << cParm()
			<< oParm("blen") << f.Pic->Bulk.Len << cParm();
		if (f.Pic->Bulk.Len)	// 5617 - dumping data
			ofile << oParm("file") << dump_bulk(&f.Pic->Bulk) << cParm();
	}
}

void	PrintSect(char *name, MXL_Sect &sect)	{
	ofile << oNode(name)
	<< oParm("qty") << *sect.Qty << cParm();
	if (*sect.Qty)	{
		ofile << cT();
		for (int i = 0; i < *sect.Qty; i++)	{
			ofile << oNode("sec")
				<< oParm("b") << sect.Prop[i].Prop->Beg << cParm()
				<< oParm("e") << sect.Prop[i].Prop->End << cParm()
				<< oParm("p") << sect.Prop[i].Prop->Parent << cParm()
				<< oParm("u0") << sect.Prop[i].Prop->Unknown0 << cParm()
				<< ocPString("nm", sect.Prop[i].Name)
			<< cNode();
		}
		ofile << cNode(name);
	} else
		ofile << cNode();
}

void	PrintFF(char *name, MXL_FormFeed *FF)	{
	ofile << oNode(name)
	<< oParm("qty") << FF->Qty << cParm();
	if (FF->Qty)	{
		ofile << cT();
		for (int i = 0; i < FF->Qty; i++)	{
			ofile << oNode("ff")
			<< oParm("n") << FF->RowCol[i] << cParm()
			<< cNode();
		}
		ofile << cNode(name);

	} else
		ofile << cNode();
}

// function 2 out MXL struct into XML
// @parm:
//	@param data - struct itself
//	@param dir - where dump bin data to
//	@param filename - name of mxl-file
void	MXL_Out (MXL &data, string &dir, string &filename)	{
	WORD	i, j;
	char	*oname;
	static char	*onames[] = {"objl", "objr", "objt", "objo", "objp"};
	string	sfile;

	switch (data.Head->Version) {
		case(2):
			ver = ver2;
			break;
		case(6):
			ver = ver6;
			break;
		case(7):
			ver = ver7;
			break;
		default:
			cerr <<  "Unsupported MXL version:" << data.Head->Version << endl;
			return;
	}
	// 5C11: prepare out file for dialog
	sfile = catdir(dir, filename);
	sfile = dRoot + sfile + ".xml";
	ofile.open(sfile.c_str(), ios::binary | ios::out);
	// end prepare
	ofile
		<< "<?xml version = '1.0' encoding = 'windows-1251'?>" << endl
		<< "<!DOCTYPE tml SYSTEM \"tml.dtd\">" << endl
		<< oNode ("tml")
		// Head
		<< oParm ("u0") << hex02(data.Head->Unknown0[0]) << " " << hex02(data.Head->Unknown0[1]) << " " << hex02(data.Head->Unknown0[2]) << " " << hex02(data.Head->Unknown0[3]) << " " << hex02(data.Head->Unknown0[4]) << cParm()
		<< oParm ("ver") << data.Head->Version << cParm()
		<< oParm ("cqty") << data.Head->ColQty << cParm()
		<< oParm ("rqty") << data.Head->RowQty << cParm()
		<< oParm ("oqty") << data.Head->ObjQty << cParm();
	if (ver == ver2)
		ofile << oParm ("u1") << *data.Unknown1 << cParm();	// !!! where  Unknown1 ? !!!
	ofile << cT();
	// Table prop
	PrintProps("tbl", data.Table); ofile << cNode();
	// Fonts
	ofile << oNode("fnts")
	<< oParm("qty") << *data.Font.Qty << cParm();
	// NB
	if (*data.Font.Qty)	{
		ofile << cT();
		for (i = 0; i < *data.Font.Qty; i++)	{
			ofile
			<< oNode("fnt")
			<< oParm("n") << data.Font.NB->Number[i] << cParm()
			<< oParm("h") << data.Font.Prop[i].Height << cParm()
			<< oParm("w") << data.Font.Prop[i].Width << cParm()
			<< oParm("esc") << data.Font.Prop[i].Escapement << cParm()
			<< oParm("dir") << data.Font.Prop[i].Orientation << cParm()
			<< oParm("b") << data.Font.Prop[i].Weight << cParm()
			<< oParm("i") << int(data.Font.Prop[i].Italic) << cParm()
			<< oParm("u") << int(data.Font.Prop[i].Underline) << cParm()
			<< oParm("so") << int(data.Font.Prop[i].StrikeOut) << cParm()
			<< oParm("cp") << int(data.Font.Prop[i].CodePage) << cParm()
			<< oParm("opr") << int(data.Font.Prop[i].OutPrecision) << cParm()
			<< oParm("cpr") << int(data.Font.Prop[i].ClipPricision) << cParm()
			<< oParm("pf") << int(data.Font.Prop[i].PitchAndFamily) << cParm()
			<< oParm("fnm") << data.Font.Prop[i].FontName << cParm();
			BYTE l = strlen((char *) data.Font.Prop[i].FontName);
			ofile
			<< ocBYTEs("tsh", &data.Font.Prop[i].FontName[l], 32 - l)
			<< cNode();
		}
		ofile << cNode("fnts");
	} else
		ofile << cNode();
	// Header prop
	PrintExtProps("tblh", data.Header); ofile << cNode();
	// Footer prop
	PrintExtProps("tblf", data.Footer); ofile << cNode();
	// Colums
	ofile
		<< oNode("cols")
		<< oParm("qty") << *data.Column.Qty << cParm();
	if (*data.Column.Qty)	{
		ofile << cT();
		for (i = 0; i < *data.Column.Qty; i++)	{
			PrintExtProps("col", data.Column.Prop[i]);
			ofile << oParm("n") << data.Column.NB->Number[i] << cParm()
			<< cNode();
		}
		ofile << cNode("cols");
	} else
		ofile << cNode();
	// Rows
	ofile << oNode("rows")
	<< oParm("qty") << *data.Row.Qty << cParm();
	if (data.Row.Qty)	{
		ofile << cT();
		for (i = 0; i < *data.Row.Qty; i++)	{
			PrintProps("row", data.Row.Prop[i].Prop);
			ofile << oParm("n") << data.Row.NB->Number[i] << cParm()
			<< cNode(); // Row.Prop
		}
		ofile << cNode("rows");
	} else
		ofile << cNode();
	// Cells
	ofile << oNode("cells") << cT();
	for (i = 0; i < *data.Row.Qty; i++)	{
		for (j = 0; j < *data.Row.Prop[i].Cell.Qty; j++)	{
			PrintExtProps("cell", data.Row.Prop[i].Cell.Prop[j]);
			ofile << oParm("r") << data.Row.NB->Number[i] << cParm()
			<< oParm("c") << data.Row.Prop[i].Cell.NB->Number[j] << cParm()
			<< cNode();
		}
	}
	ofile << cNode("cells");
	// Objs
	ofile << oNode("objs")
		<< oParm("qty") << *data.Obj.Qty << cParm();
	if (*data.Obj.Qty)	{
		ofile << cT();
		for (i = 0; i < *data.Obj.Qty; i++)	{
			oname = onames[data.Obj.Prop[i].ExtProp->Type - 1];
			PrintExtProps(oname, data.Obj.Prop[i].Prop);
			PrintObjProps(data.Obj.Prop[i]);
			ofile << cNode();
		}
		ofile << cNode("objs");
	} else
		ofile << cNode();
	// Joins
//goto TheEnd;
	ofile << oNode("joins")
	<< oParm("qty") << data.Join->Qty << cParm();
	if (data.Join->Qty)	{
		ofile << cT();
		for (i = 0; i < data.Join->Qty; i++)	{
			ofile << oNode("join")
			<< oParm("c0") << data.Join->Prop[i].Col0 << cParm()
			<< oParm("r0") << data.Join->Prop[i].Row0 << cParm()
			<< oParm("c1") << data.Join->Prop[i].Col1 << cParm()
			<< oParm("r1") << data.Join->Prop[i].Row1 << cParm()
			<< cNode();
		}
		ofile << cNode ("joins");
	} else
		ofile << cNode();
	// VSects
	PrintSect("vsecs", data.VSect);
	// HSects
	PrintSect("hsecs", data.HSect);
	// VFFs
	PrintFF("vffs", data.VFormFeed);
	// HFFs
	PrintFF("hffs", data.HFormFeed);
	// Names
	if (ver >= ver6) {
		ofile << oNode("names")
		<< oParm("qty") << *data.Name.Qty << cParm();
		if (*data.Name.Qty)	{
			ofile << cT();
			for (DWORD i = 0; i < *data.Name.Qty; i++)	{
				ofile << oNode("name")
				<< ocPString("nm", data.Name.Prop[i].Name)
				<< oParm("u0") << data.Name.Prop[i].Prop->Unknown0 << cParm()
				<< oParm("u1") << data.Name.Prop[i].Prop->Unknown1 << cParm()
				<< oParm("u2") << data.Name.Prop[i].Prop->Unknown2 << cParm()
				<< oParm("c0") << data.Name.Prop[i].Prop->Col0 << cParm()
				<< oParm("r0") << data.Name.Prop[i].Prop->Row0 << cParm()
				<< oParm("c1") << data.Name.Prop[i].Prop->Col1 << cParm()
				<< oParm("r1") << data.Name.Prop[i].Prop->Row1 << cParm()
				<< cNode();
			}
			ofile << cNode("names");
		} else
			ofile << cNode();
	}
//TheEnd:
	ofile << cNode ("tml");
	ofile.close();
}
