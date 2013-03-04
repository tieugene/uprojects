// commands.cpp - parse Commands stream

#include "catmd.h"
extern fstream ofile;

#define CHK(s)	if (ptr > eptr) { cerr << "E: Comand." << s << " ptr (" << (ptr - data.data) << ") out of range - " << eptr << endl; return; } else cerr << s << ptr-data.data << endl;

void	PrnCmdAttr(BYTE *&bptr, const char *name) {
	Pdata	ptmp;

	ptmp.size = getsize(bptr);
	ptmp.data = bptr;
	bptr += ptmp.size;
	ofile << " " << name << "=\"";
	print_data(ptmp);
	ofile << "\"";
}

void	do_Commands (Pdata & data, bool subflag, const string & ccstr) {	// subflag = true if it is SubUsersInterfaceType
	DWORD	*dwptr, cmdqty, signature;
	string	stmp, sname;
	Pdata	ptmp;
	BYTE	*bptr = data.data;
	string s;
	static int counter = 0;

	// close start tag
	dwptr = (DWORD *) bptr;
	signature = GetDW(bptr);
	if ((signature != 0x00000007L) && (signature != 0x00000008L)) {
		s = "cmd" + i2s(counter++);
		dump_data(data, dBulk, s);
		cerr << "E: This is not Commands. Dumped as " << dBulk << dPathSep << s << endl;
		return;
	} else {
		// name/parent_name
		if (!subflag)
			ofile << "<" << (sname = "cmds") << ccstr << " cnm=\"";
		else
			ofile << "<" << (sname = "scmds") << ccstr << " pnm=\"";
		bptr += 4;
		ptmp.size = getsize(bptr);
		ptmp.data = bptr;
		print_data(ptmp);
		bptr += ptmp.size;
		// operations, nonauth
		ofile << "\" nop=\"" << GetDW(bptr) << "\" nau=\"" << GetDW(bptr + 4) << "\"";
		bptr += 8;
		if (subflag)
			// submenu - name
			PrnCmdAttr(bptr, "cnm");
		// commands qty
		cmdqty = GetDW(bptr);
		ofile << " cqty=\"" << cmdqty << "\">" << endl;
		bptr += 4;
		// * commands
		while (cmdqty > 0) {
			if (!subflag) {
			// ID
				ofile << "<cmd id=\"" << GetDW(bptr) << "\"";
				bptr += 4;
			// short tip
				PrnCmdAttr(bptr, "stip");
			// tip
				PrnCmdAttr(bptr, "tip");
			// hotkey
				ofile << " mk=\"" << int(bptr[0]) << "\" sc=\"" << GetW(bptr + 1) << "\"";
				bptr += 3;
			} else
				ofile << "<scmd";
			// command itself
			PrnCmdAttr(bptr, "cmd");
			// addon
			PrnCmdAttr(bptr, "ad");
			// next
			cmdqty--;
			ofile << "/>" << endl;
		}
		cTag(sname);
	}
//	if ((ptr - data.data) != data.size)
//		cerr << "E: Panel: " << (ptr - data.data) << " bytes processed when wanted " << (data.size) << endl;
}
