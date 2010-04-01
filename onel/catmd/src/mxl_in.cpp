//#include <stdio.h>
//#include <iostream>

#include "catmd.h"

static	BYTE	*btmp;
static	mxlver	ver;		// flag to show that it's v.7 MXL - w/ angle field

void	prnPstring(BYTE *s) {
	BYTE i = *s++;

	while (i--)
		cerr << char(*s++);
}

void	SetWQty(BYTE *&ptr, WORD *&qty)	{
	qty = (WORD *) ptr;
	ptr += sizeof(WORD);
}

void	SetPString(BYTE *&ptr, MXL_PString &ps)	{
	WORD	*wptr;
	wptr = (WORD *) &(ptr[1]);
	if (*ptr == 0xFF)					// long text
		{ps.Len = *wptr; ptr += sizeof(WORD);}
	else
		ps.Len = *ptr;
	ptr++;
	if (ps.Len > 0)
		ps.Text = (char *) ptr;
	else
		ps.Text = NULL;
	ptr += ps.Len;
}

void	ResetPString(MXL_PString &ps)	{
	ps.Len = 0; ps.Text = NULL;
}

void	SetProp(BYTE *&ptr, MXL_Prop *&item)	{
	item = (MXL_Prop *) ptr;
//	ptr += sizeof(MXL_Prop);
	switch (ver) {
		case(ver2):
			ptr += (sizeof(MXL_Prop) - 4);	// MXL_Prop.(Text.Prot + Unknown + Angle)
			break;
		case(ver6):
			ptr += (sizeof(MXL_Prop) - 2);	// MXL_Prop.Angle
			break;
		default:	// ver7
			ptr += sizeof(MXL_Prop);
	}
}

void	SetExtProp(BYTE *&ptr, MXL_ExtProp &item)	{
	//BYTE	dlen;

	SetProp(ptr, item.Prop);
	if (item.Prop->Flag & 0x80000000L) {	// Text
		SetPString(ptr, item.Text);
	}
	else
		ResetPString(item.Text);
	if (item.Prop->Flag & 0x40000000L) {	// Desc
		SetPString(ptr, item.Desc);
	}
	else
		ResetPString(item.Desc);
}

void	SetNB(BYTE *&ptr, MXL_NumbersBlock *&nb)	{
	nb = (MXL_NumbersBlock *) ptr;
	ptr += (sizeof(WORD) + nb->Qty * sizeof(DWORD));
}

int	SetCell(BYTE *&ptr, MXL_Cell &cb)	{
	WORD	i;

//cerr << "NB: " << ptr - btmp << endl;
	SetNB(ptr, cb.NB);						// Numbers Block
	SetWQty(ptr, cb.Qty);
	if (*cb.Qty)	{
		if (!(cb.Prop = new MXL_ExtProp[*cb.Qty]))
			return 1;
		for (i = 0; i < *cb.Qty; i++) {
//cerr << "Cell[" << i << "]: " << ptr - btmp << endl;
			SetExtProp(ptr, cb.Prop[i]);
			if (cb.Prop[i].Prop->Flag & 0x00200000L) {	// Table in Dialog
//cerr << "W: Table-In-Dialog !" << endl;
				ptr += (*((WORD *) ptr) + sizeof(WORD));		// drop dialog props => TODO !!! commented 'cause Aspect.Jeweller
			}
		}
	}
//	else
//		cb.Prop = NULL;
	return 0;
}
int	SetSect(BYTE *&ptr, MXL_Sect &sect)	{
	WORD	i;

	SetWQty(ptr, sect.Qty);
	if (*sect.Qty)	{
		if (!(sect.Prop = new MXL_SectProp[*sect.Qty]))	// alloc mem
			return 1;
		for (i = 0; i < *sect.Qty; i++)	{		// 4 each of section ('cause of Text)
			sect.Prop[i].Prop = (MXL_SectData *) ptr;
			ptr += sizeof(MXL_SectData);
			SetPString(ptr, sect.Prop[i].Name);		// load Name
		}
	}
//	else
//		sect.Prop = NULL;
	return 0;
}

// ********

#define CHKPTR(s)	if (ptr > eptr) { cerr << "MXL Error! after " << (s) << " decoded " << (ptr - btmp) << " bytes against needed " << buffer.size << endl; return (false); }

bool	MXL_Decode (Pdata &buffer, MXL &data)	{
	bool	bfirstole = true;
	BYTE	*ptr = buffer.data, *eptr = buffer.data + buffer.size;	//, *bmax = buffer.data + buffer.size;
	WORD	i;

	btmp = buffer.data;

	// 1. load Head
	data.Head = (MXL_Head *) ptr; ptr += sizeof(MXL_Head);
	if (strncmp(data.Head->Signature, "MOXCEL", 6))	{
		cerr <<  "It isn't MOXEL file" << endl;
		return (false);
	}
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
			cerr << "Unsupported MXL version:" << data.Head->Version << endl;
			return (false);
	}
	// 2. load Table Props
	SetProp(ptr, data.Table);
	// 3. load Fonts
	SetNB(ptr, data.Font.NB);						// Numbers Block
	SetWQty(ptr, data.Font.Qty);
	if (data.Font.Qty) {
		data.Font.Prop = (MXL_FontProp *) ptr;
	}
	ptr += (*data.Font.Qty * sizeof(MXL_FontProp));
	// 4. load Unknown0
	data.Unknown0 = (DWORD *) ptr;
	ptr += sizeof(DWORD);
	// 5. load Header Props
	SetExtProp(ptr, data.Header);
	CHKPTR("Header")
	// 6. load Footer Props
	SetExtProp(ptr, data.Footer);
	CHKPTR("Footer")
//cerr << ptr - buffer.data << endl;
	// 7. load Columns
	if (SetCell(ptr, data.Column))
		return (false);
	CHKPTR("Cols")
	// 8. load Rows
	SetNB(ptr, data.Row.NB);						// Numbers Block
	SetWQty(ptr, data.Row.Qty);
	if (*data.Row.Qty)	{
		if (!(data.Row.Prop = new MXL_RowProp[*data.Row.Qty]))
			return (false);
		for (i = 0; i < *data.Row.Qty; i++)	{
			SetProp(ptr, data.Row.Prop[i].Prop);
			SetCell(ptr, data.Row.Prop[i].Cell);
		}
	}
	CHKPTR("Rows")
	// 9. load Objects
	SetWQty(ptr, data.Obj.Qty);
	if (*data.Obj.Qty)	{
		if (!(data.Obj.Prop = new MXL_ObjProp[*data.Obj.Qty]))		// alloc mem
			return (false);
		for (i = 0; i < *data.Obj.Qty; i++)	{			// process each Obj
			SetExtProp(ptr, data.Obj.Prop[i].Prop);			// Common props
			data.Obj.Prop[i].ExtProp = (MXL_ExtObjProp *) ptr;
			ptr += sizeof(MXL_ExtObjProp);
			if (data.Obj.Prop[i].ExtProp->Type == 5)	{	// picture
				data.Obj.Prop[i].OLE = NULL;
				data.Obj.Prop[i].Pic = (MXL_Pic *) ptr;
				ptr += (2 * sizeof(DWORD) + data.Obj.Prop[i].Pic->Bulk.Len);		// drop Unknown0, Len & Data
			}
			else if (data.Obj.Prop[i].ExtProp->Type == 4)	{	// OLE
				data.Obj.Prop[i].Pic = NULL;
				if (!(data.Obj.Prop[i].OLE = new MXL_OLE))
					return (false);
				data.Obj.Prop[i].OLE->Unknown0 = (WORD *) ptr;	// set unknown0
				ptr += sizeof(WORD);
				if (bfirstole)	{					// 1st OLE (!!!) - w/ 18 bytes
					bfirstole = false;
					data.Obj.Prop[i].OLE->Name = (MXL_OLEName *) ptr;
					ptr += sizeof(MXL_OLEName);
				}
				else
					data.Obj.Prop[i].OLE->Name = NULL;
				data.Obj.Prop[i].OLE->Trash = (MXL_OLETrash *) ptr;	// others unknown
				ptr += sizeof(MXL_OLETrash);
				data.Obj.Prop[i].OLE->Bulk = (MXL_Bulk *) ptr;		// Bulk
				ptr += (sizeof(DWORD) + data.Obj.Prop[i].OLE->Bulk->Len);		// drop Len & Data
			}
			else	{
				data.Obj.Prop[i].OLE = NULL;	// zero Pic & OLE ptr
				data.Obj.Prop[i].Pic = NULL;
			}
		}
	}
	CHKPTR("Objs")
	// 10. load Unknown1 (v.2)
	if (ver == ver2) {
		data.Unknown1 = (WORD *) ptr;
		if (*data.Unknown1)
			cerr << "MXL v.2 warning: Unknow1 (" << (ptr - buffer.data) << ") = " << *data.Unknown1 << endl;
		ptr += sizeof(WORD);
	}
	CHKPTR("U1")
	// 11. Load Joins
	data.Join = (MXL_Join *) ptr;
//if (ver == ver2)	{ cerr << (ptr - buffer.data) << ": Join.Qty:" << data.Join->Qty << endl; return false; }
	ptr += (sizeof(WORD) + data.Join->Qty * sizeof(MXL_JoinProp));		// drop Len & Data
	CHKPTR("Joins")
	// 12. Load Vertical Sections
	if (SetSect(ptr, data.VSect))
		return (false);
	CHKPTR("VSec")
//if (ver == ver2)	cerr << (ptr - buffer.data) << ": VSect.Qty:" << *data.VSect.Qty << endl;
	// 12. Load Horisontal Sections
	if (SetSect(ptr, data.HSect))
		return (false);
	CHKPTR("HSec")
	// 13. Load Vertical FormFeeds
	data.VFormFeed= (MXL_FormFeed *) ptr;
	ptr += (sizeof(WORD) + data.VFormFeed->Qty * sizeof(DWORD));
	CHKPTR("VFF")
	// 14. Load Horizontal FormFeeds
	data.HFormFeed= (MXL_FormFeed *) ptr;
	ptr += (sizeof(WORD) + data.HFormFeed->Qty * sizeof(DWORD));
	CHKPTR("HFF")
	// 15. Load Names
	if (ver >= ver6) {
		data.Name.Qty = (DWORD *) ptr;
		ptr += sizeof(DWORD);
		if (*data.Name.Qty)	{
			if (!(data.Name.Prop = new MXL_NameProp[*data.Name.Qty]))	// alloc mem
				return (false);
			for (i = 0; i < *data.Name.Qty; i++)	{		// 4 each of Name ('cause of Name.Text)
				SetPString(ptr, data.Name.Prop[i].Name);
				data.Name.Prop[i].Prop = (MXL_NameData *) ptr;
				ptr += sizeof(MXL_NameData);
			}
		}
	}
	// The End
	if ((ptr - buffer.data) != buffer.size) {
		cerr << "MXL Error! decoded " << (ptr - buffer.data) << " bytes against wanted " << buffer.size << endl;
		return (false);
	}
	return (true);
}
