#include "catmd.h"

#include <sys/types.h>
#ifndef __BORLANDC__
#include <unistd.h>
#endif

extern string dRoot;
extern fstream ofile;

void	parse(Pdata & data, BYTE *array[])
// parse bq-string, set \0 into ends of substrings, fill array[] w/ substrings starts
{
	BYTE	*endptr = data.data + data.size, *destptr, i = 0;
	bool	inquot = false;	// true == inside quotes; false == outside quotes

	while(data.data < endptr) {
		if (inquot) {					// inside "..."
			if (*data.data == '"') {			// end of item or double-quote
				if (data.data[1] == '"')		// "" (== ")
					*destptr++ = *data.data++;
				else {				// end of item
					*destptr = '\0';	// close string
					i++;
					inquot = false;
				}
			} else					// simple char
				*destptr++ = *data.data;
		} else {					// outside "..."
			if (*data.data == '"') {			// start next item; else - skip
				destptr = data.data + 1;		// set float pointer
				array[i] = destptr;		// set next item start
				inquot = true;
			}
		}
		data.data++;
	}
}

DWORD	debase64(BYTE *data) {
	/*
	converts 6-bit bytes into normal
	@param data - buffer
	@param size - buffer size in bytes
	@return - new size.
	*/
	BYTE	*ptr = data, a, b, c, d;
	DWORD	size, i;

	size = strlen((char *) data);
	if (!size)
		return (0);
//	if (size & 3) {	// ask lower 2 bits (== %4)	!!! FIXME !!!
//		cerr << "Size of base64 input (" << size << ") must B multiple times of 4." << endl;
//		return (0);
//	}

	for (i = 0; i < size; i += 4) {
		a = data[i+0] - ' ';
		b = data[i+1] - ' ';
		c = data[i+2] - ' ';
		d = data[i+3] - ' ';
		ptr[0] = (a << 2) | (b >> 4);
		ptr[1] = ((b << 4) & '\xF0') | (c >> 2);
		ptr[2] = ((c << 6) & '\xC0') | d;
		ptr += 3;
	}
	return (size * 3 / 4);
}

void	BMP(string & fname, BYTE *data)
// decode input string as 6-to-8-bit & write as BMP-file
{
	Pdata	head, buffer;
	WORD	nb;
	DWORD	nc, *a;
	BYTE	tratata[14];

	head.size = 14;
	head.data = tratata;
	buffer.size = strlen((char *) data);
	buffer.size = debase64(data);
	nb = *((WORD *) (data + 0x0E));		// Bits per pixel
	nc = *((DWORD *) (data + 0x20));	// Colours
	if ((nb == 8) && (nc == 0))
		nc = 0x100;
	head.data[0] = 'B';
	head.data[1] = 'M';
	a = ((DWORD *) (head.data + 2));
	a[0] = buffer.size + 14;
	a[1] = 0L;
	a[2] = (nc * 4) + 54;
	dump_data(head, dTS, fname);
	buffer.data = data;
	dump_data(buffer, dTS, fname, O_RDWR|O_APPEND);
}

void do_TS (Pdata & data, const string & ccstr)	// parse TagStream
{
	BYTE	*array[10] = {NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL};	// ptrs to TagStream substreams

	// 1. decode stream
	Decode1C(data);
	// 2. skip "pascal" header
	getsize(data);
	// 3. parse
	parse(data, array);
	// 4. out
	ofile << "<ts" << ccstr;
	// 4.1. hash
	if (*array[1])
		ofile << " hash=\"" << array[1] << "\"";
	// 4.2. short description
	if (*array[3]) {
		ofile << " short =\"";
		print_str((char *) array[3]);
		ofile << "\"";
	}
	// 4.3. logo
	if (*array[7]) {
		BMP(fTSlogo, array[7]);
		ofile << " logo=\"" << dTS + dPathSep + fTSlogo  << "\"";
	}
	// 4.4. splash
	if (*array[9]) {
		BMP(fTSsplash, array[9]);
		ofile << " splash=\"" << dTS + dPathSep + fTSsplash  << "\"";
	}
	// 4.5. long description
	ofile << ">";
	if (*array[5])
		print_str((char *)array[5]);
	cTag("ts");
}
