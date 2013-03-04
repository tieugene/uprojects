#include "catmd.h"

extern fstream ofile;

//#define CHK(s)	if (ptr > eptr) { cerr << "E: Panel." << s << " ptr (" << (ptr - data.data) << ") out of range - " << eptr << endl; return; } else cerr << s << ptr-data.data << endl;

//void	do_Panel(BYTE *data, MsOlePos size, char * name) {
void	do_Panel(Pdata &data, string & name, const string & ccstr) {
	DWORD * dwptr = (DWORD *) data.data, dwQty, dwBQty = 0L, i, signature;
	BYTE	*store = data.data, *ptr = data.data;	//, *eptr = data.data + data.size;
	Pdata	ptmp;
	string s;
	static int counter = 0;

	signature = *dwptr;
	if ((signature != 0xFFFFFFFDL) && (signature != 0xFFFFFFFEL))	{
		s = "panel" + i2s(counter++);
		dump_data(data, dBulk, s);
		cerr << "E: This is not Panel. Dumped as " << dBulk << dPathSep << s << endl;
		return;
	}
	// 1. Panels
	ofile << "<panels" << ccstr << ">" << endl;
	dwQty = dwptr[1];
	if (signature == 0xFFFFFFFEL) {		// old format
		ptr += (8 + (dwQty * 4));
		if (dwQty != GetDW(ptr)) {
			s = "panel" + i2s(counter++);
			dump_data(data, dBulk, s);
			cerr << "E: Panel: PanelsQty <> PanelNamesQty. Panel dumped as " << dBulk << dPathSep << s << endl;
			return;
		}
		dwptr++;	// Panels qty
		ptr += 4;	// 1st panel name
		for (i = 0L; i < dwQty; i++) {
			ofile << "<pnl name=\"";
			ptmp.size = ptr[0];
			ptmp.data = ptr + 1;
			print_data(ptmp);
			ptr += (ptr[0] + 1);
			dwptr++;
			ofile << "\" qty=\"" << dwptr[0] << "\"/>" << endl;
			dwBQty += dwptr[0];
		}
	} else {				// new format
		ptr += 8;	// min: 8
		for (i = 0L; i < dwQty; i++) {
			ofile << "<pnl name=\"";
			ptmp.size = ptr[0];
			ptmp.data = ptr + 1;
			print_data(ptmp);
			ptr += (ptr[0] + 1);
			dwptr = (DWORD *) ptr;
			ofile << "\" qty=\"" << dwptr[0] << "\" pos=\"" << dwptr[1] << "\" show=\"" << dwptr[2] << "\" newline=\"" << dwptr[3] << "\"/>" << endl;
			dwBQty += dwptr[0];
			ptr += 16;
		}
	}
	// 2. Buttons IDs
	dwptr = (DWORD *) ptr;
	for (i = 0L; i < dwBQty; i++) {
		if (*dwptr)
			ofile << "<btn id=\"" << *dwptr << "\"/>" << endl;	// !!! %08X
		else
			ofile << "<sep/>" << endl;
		dwptr++;
	}
	ptr += ((dwBQty << 2) + 4);	// min: 12
	// 3. Buttons w/ text
	dwQty = *dwptr;
	for (i = 0L; i < dwQty; i++) {
		ofile << "<btn name=\"";
		ptmp.size = ptr[0];
		ptmp.data = ptr + 1;
		print_data(ptmp);
		ptr += (ptr[0] + 1);
		dwptr = (DWORD *) ptr;
		ofile << "\" id=\"" << *dwptr << "\"/>" << endl;
		ptr += 4;
	}
	// 4. Buttons w/ pic
	dwptr = (DWORD *) ptr;		// min: *12
	dwQty = *dwptr;
	for (i = 0L; i < dwQty; i++) {
		ofile << "<btn id=\"" << *dwptr << "\"/>" << endl;
		dwptr++;
	}
	ptr += ((dwQty << 2) + 4);	// min: 16
	// 5. Out BMP
	if ((data.size - (ptr - store)))	{
		ptmp.size = data.size - (ptr - store);
		ptmp.data = ptr;
		string tmpstring = name.substr(16, name.length() -  10) + ".bmp";	// !!!
		dump_data(ptmp, dPic, tmpstring);
		ofile << "<panelpic file=\"" << dPic << dPathSep << tmpstring << "\"/>" << endl;
	}
	cTag ("panels");
//	if ((ptr - data.data) != data.size)
//		cerr << "E: Panel: " << (ptr - data.data) << " bytes processed when wanted " << (data.size) << endl;
}
