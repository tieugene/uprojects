/// Parse GUIDData stream

#include "catmd.h"
extern fstream ofile;

void	do_GD(Pdata & data, const string & ccstr) {
	DWORD	sz = *((DWORD *) data.data);
	BYTE	*ptr = data.data + sizeof(sz);
	WORD	i, j;
	
	if (sz != (data.size >> 4))	// each rec 16 bytes long
		cerr << "Misplaced GIUDData size: GUIDData.size=" << sz << ", streamsize=" << data.size << endl;
	else {
		ofile << "<guids" << ccstr << ">" << endl;
		for (i = 0; i < sz; i++) {
			ofile << "<g no=\"" << i << "\" v=\"";
			for (j = 0; j < 16; j++)
				ofile << hex02(*ptr++);	// 5523; was prnf
			ofile << "\"/>" << endl;
		}
		cTag("guids");
	}
}
