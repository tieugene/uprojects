#include "catmd.h"

extern fstream ofile;

// simply print data, replacing non-xml chars
void	print_str(char *data)
{
	Pdata	tmp;
	tmp.size = strlen(data);
	tmp.data = (BYTE *) data;
	print_data(tmp);
}

void	print_data(Pdata &data)
{
	DWORD i;
	
	for (i = 0; i < data.size; i++)	{
		switch(data.data[i])	{
			case '&':
				ofile << "&amp;";
				break;
			case '<':
				ofile <<  "&lt;";
				break;
			case '>':
				ofile <<  "&gt;";
				break;
			case '"':
				ofile <<  "&quot;";
				break;
			case '\t':
			case '\x0D':
			case '\x0A':
				ofile << char(data.data[i]);	// 5523; was putchar
				break;
			default:
				if (data.data[i] < ' ')	// nonprintable
					ofile << "&#x" << hex02(data.data[i]) << ";";	// 5523. was prnf("&#x%02X;", data.data[i]);
				else
					ofile << char(data.data[i]);	// 5523; was putchar
		}
	}
}

// print "Pascal-string" data
/*void	print_sized_data(Pdata &data)
{
	BYTE	bsz;
	WORD	wsz;
	DWORD	sz;
	Pdata	tmp;

	tmp.size = data.size;
	tmp.data = data.data;
	if (tmp.data[0] != 0xFF) {		// 0..254 chars
		sz = *((BYTE *) tmp.data);
		if (sz != (tmp.size - 1)) {
			cerr << "Bad size: " << sz << endl;
		} else {
			tmp.size--;
			tmp.data++;
		}
		print_data(tmp);
	} else if (*((WORD *) (tmp.data + 1)) != 0xFFFF) {	// 0..65534 chars
		sz = *((WORD *) (tmp.data + 1));
		if (sz != (tmp.size - 3)) {
			ofile << "Bad size: " << sz << endl;
		} else {
			tmp.size -= 3;
			tmp.data += 3;
		}
		print_data(tmp);
	} else if (*((DWORD *) (tmp.data + 5)) != 0xFFFFFFFFL) {	// many chars
		sz = *((DWORD *) (tmp.data + 3));
		if (sz != (tmp.size - 7)) {
			ofile << "Bad size: " << sz << endl;
		} else {
			tmp.size -= 7;
			tmp.data += 7;
		}
		print_data(tmp);
	} else {
		cerr << "Too big piece" << endl;
		return;
	}
}*/

// printing data, unpack it B4
void	print_packed_data(Pdata &data, string &dir, string &file, bool mode) {	// mode: 0=text, 1=bin
	Pdata	out;

	if(!unpack_data(data, out)) {	// out = unpacked
		if (mode)				// bin
			dump_fpdata(out, dir, file);
		else					// text
			print_data(out);
	} else {
		cerr << dir << file << " dumped packed." << endl;
		dump_fpdata(data, dir, file);
	}
	return;
}

void	print_bq (Pdata &data) {	// print "bracketed-quoted" text; data.data = {{...}, ...}
	BYTE	*ptr = data.data;
	BYTE	*pmax = ptr + data.size;
	bool	inquot = false;

	while (ptr < pmax) {	// mail loop
		switch (*ptr) {
			case '"':
				if (inquot) {
					inquot = false;
					ofile << "\"/>" << endl;
				} else {
					inquot = true;
					ofile << "<p v=\"";
				}
				break;
			case '{':
				if (!inquot)
					ofile << "<n>" << endl;
				break;
			case '}':
				if (!inquot)
					ofile << "</n>" << endl;
				break;
			default:
				if (inquot)
					switch (*ptr)	{
						case '&':
							ofile << "&amp;";
							break;
						case '<':
							ofile <<  "&lt;";
							break;
						case '>':
							ofile <<  "&gt;";
							break;
						default:
							ofile << *ptr;
					}
		}
		ptr++;
	}
}
