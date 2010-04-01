// pic.cpp
// unpack and dump pictures

#include "catmd.h"

extern string dRoot;
extern fstream ofile;

//void	do_Pic(BYTE *data, MsOlePos size, char * name) {
void	do_Pic(Pdata & data, string & name, const string & ccstr) {
	Pdata	out, tmp;
	DWORD	sign;
	string	stmp = name.substr(csPic.length(), name.length() - csPic.length());
	string	ext, fname;

	if(!unpack_data(data, out)) {	// out = unpacked
		sign = *((DWORD *) out.data);
		if (sign != 0x0000746C) {
			cerr << "W: unknown picture type: " << dRoot << dPic << dPathSep <<  stmp << endl;
			dump_data(out, dPic, stmp);
		} else {	// correct sign
			sign = *((DWORD *) (out.data + 4));
			if (sign != (out.size - 8)) {
				cerr << "W: Bad picture size: " << dRoot << dPic << dPathSep << stmp << endl;
				dump_data(out, dPic, stmp);
			} else {	// correct pic size
				tmp.size = out.size - 8;
				tmp.data = out.data + 8;
				// define picture type
				switch (GetW(tmp.data)) {
					case (0x4D42):	// BM...
						ext = ".bmp";
						break;
					case (0xCDD7):	// ือ
						ext = ".wmf";
						break;
					case (0x0000):	// \0\0
						ext = ".ico";
						break;
				}
				fname = stmp + ext;
				dump_data(tmp, dPic, fname);
			}
		}
	} else {
		cerr << "Picture " << stmp << " dumped packed." << endl;
		dump_fpdata(data, dPic, stmp);
	}
	ofile << "<pic" << ccstr << " uid=\"" << stmp << "\" fn=\"" << dPic << dPathSep << stmp << ext << "\"/>" << endl;
}
