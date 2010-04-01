#include "catmd.h"

extern fstream ofile;

void	do_SubMenu(BYTE **);

//void	do_Menu(BYTE *data, MsOlePos size) {
void	do_Menu(Pdata & data, const string & ccstr) {
	DWORD * dwptr = (DWORD *) data.data, dwQty, i;
	BYTE	* ptr = data.data + 8;

	if (*dwptr != 1L)	{
		cerr << "This is not Menu." << endl;
		return;
	}
	dwQty = dwptr[1];
	ofile << "<menus" << ccstr << ">" << endl;
	for (i = 0L; i < dwQty; i++)
		do_SubMenu(&ptr);
	cTag ("menus");
}

void	do_SubMenu(BYTE **data) {
	DWORD dw = *((DWORD *) (*data)), i;
	Pdata	tmp;

	if (dw == 0L) {			// separator
		ofile << "<sep/>" << endl;
		(*data)  += 4;
	} else if (dw == 0xFFFFFFFF) {	// menu
		ofile << "<menu nm=\"";
		tmp.size = (*data)[4];
		tmp.data = (*data) + 5;
		print_data(tmp);
		ofile << "\">" << endl;
		(*data) = (*data) + 5 + (*data)[4];
		dw = *((DWORD *) (*data));
		(*data) += 4;
		for (i = 0L; i < dw; i++)
			do_SubMenu(data);
		ofile << "</menu>" << endl;
	} else if (dw >= 0x0000C000) {	// menuitem
		ofile << "<mitem id=\"" << dw << "\" nm=\"";	// !!! %08X
		tmp.size = (*data)[4];
		tmp.data = (*data) + 5;
		print_data(tmp);
		ofile << "\"/>" << endl;
		(*data) = (*data) + 5 + (*data)[4];
	} else
		cerr << "Unknow menu object." << endl;
	return;
}
