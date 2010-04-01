// gallery.cpp
// parse Gallery stream

#include "catmd.h"
#include <iomanip>

extern string dRoot;
extern fstream ofile;

void	do_Glr(Pdata & data, const string & ccstr) {	///< parse Gallery
	BYTE	*bptr = data.data;
	DWORD	bmpsize, idxqty, i;
	string tmp = csGlr + ".bmp";
	Pdata	ptmp;
	treebranch *t, *p;

	bmpsize = GetDW(bptr + 38) + GetDW(bptr + 62);		// (c) Alex Dirks = 76h + 00041A00 = 268918
	// head
	ofile << "<glr" << ccstr <<
	" sign=\"" << hex08(GetDW(bptr+0)) << "\""
	" iqty=\"" << GetW(bptr+4) << "\""
	" u1=\"" << hex04(GetW(bptr+6)) << "\""
	" u2=\"" << hex04(GetW(bptr+8)) << "\""
	" iw=\"" << GetW(bptr+10) << "\""
	" ih=\"" << GetW(bptr+12) << "\""
	" u3=\"" << hex08(GetDW(bptr+14)) << "\""
	" cdep=\"" << GetW(bptr+18) << "\""
	" u4=\"" << hex08(GetDW(bptr+20)) << "\""
	" u5=\"" << hex08(GetDW(bptr+24)) << "\"";
	// tail
	bptr += (28 + bmpsize);					// goto tail
	// <hack 5618> : for gallery w/o u6 (catched by Dmitry Vinokurov)
	if (GetDW(bptr) == 0xFF000001L) {			// normal Gallery
		ofile << " u6=\"" << hex08(GetDW(bptr)) << "\"";
		bptr += 4;
	}
	// </hack 5618>
	idxqty = GetDW (bptr);					// index quantity;
	ofile <<
	" idxqty=\"" << idxqty << "\""
	" idxend=\"" << hex08(GetDW(bptr+4+(idxqty*4))) << "\""
	" fn=\"" << dGlr << dPathSep << tmp << "\">" << endl <<
	"<iblk>" << endl;
	//	indexes
	bptr += 4;						// skip attr6 & IdxQty
	for (i = 0; i < idxqty; i++) {
		ofile << "<idx val=\"" << hex08(GetDW(bptr)) << "\"/>" << endl;	// 5523; was prnf
		bptr += 4;
	}
	bptr += 4;						// skip IdxEnd
	ofile << "</iblk>" << endl;
	//	names
	ptmp.data = bptr;
	ptmp.size = data.size - (bptr - data.data);
	if (ptmp.size) {
		t = bq2tree(ptmp)->GetFolder(0);
		idxqty = t->GetSize();
		oTag("nblk", true);
		for (i = 0; i < idxqty; i++) {
			p = t->GetFolder(i);
			ofile << "<iname nm=\"" << *p->GetFile(0) << "\" idx=\"" << *p->GetFile(1) << "\"/>" << endl;
		}
		cTag("nblk");
	}
	// mid
	data.size = bmpsize;
	data.data += 28;
	dump_data (data, dGlr, tmp);
	cTag("glr");
}
