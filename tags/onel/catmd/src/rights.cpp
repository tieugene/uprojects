#include "catmd.h"

extern fstream ofile;

#define	CHKPTR(s)	if (dwptr > dwMax) { cerr << "E: Rights: " << s << " out of range!" << endl; return;}

//void	do_Rights(BYTE *data, MsOlePos size) {
void	do_Rights(Pdata & data, const string & ccstr) {
	DWORD	*dwptr, dwBQty, dwPQty, * dwMax = (DWORD *) &(data.data[data.size]), i, j;
	BYTE	*bptr = data.data + 4;
	Pdata	ptmp;
	static	int counter = 0;

//	if (data.data[0] != 6) {
//		string s = "rights" + i2s(counter++);
//		dump_data(data, dBulk, s);
//		cerr << "E: unknown Rights signature. dumped into " << dBulk << dPathSep << s << endl;
//		return;
//	}
	ptmp.size = getsize(bptr);
	ptmp.data = bptr;
	bptr += ptmp.size;
	ofile << "<rights" << ccstr << " sign=\"" << GetDW(data.data) << "\" dummy2=\"";
	print_data(ptmp);
	ofile << "\">" << endl;
//cerr << bptr-data.data << endl;
	dwBQty = GetDW(bptr);
	dwptr = (DWORD *) (bptr + 4);
	CHKPTR("1")
	for (i = 0L; i < dwBQty; i++) {			// Blocks loop
		ofile << "<r_" << hex02(dwptr[0]) << out_uref(dwptr[1]);		// 2. Prop set block (*qty & no - X)
		dwPQty = dwptr[2];
		dwptr += 3;
		CHKPTR("2")
		for (j = 0L; j < dwPQty; j++) {		// Prop loop
			ofile << " v_" << hex02(dwptr[0]) << "=\"" << dwptr[1] << "\"";	// 3. Prop
			dwptr += 2;
			CHKPTR("3")
		}
		ofile << "/>" << endl;
	}
	cTag ("rights");
}
