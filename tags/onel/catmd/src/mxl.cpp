// mxl.cpp
// try & process mxl-file

#include "catmd.h"

extern fstream ofile;

static DWORD TCounter = 0;

bool	MXL_Load (char *, Pdata &);

// !!! Errors: A, P
void	do_Mxl (Pdata &data, string & name, const string & ccstr) {	// call from do_stream
	MXL	mxl;
	string	sfile;

	if (data.size > 147) {		// !!! against short
		if (!MXL_Decode (data, mxl)) {
			cerr << "Error decoding MXL " << name << "; dumped." << endl;
			dump_fpdata(data, dMXL, name);
		}
		else {
			sfile = hex08(TCounter++);
			ofile << "<moxel" << ccstr << " file=\"" << dMXL << dPathSep << sfile << ".xml" << "\"/>" << endl;
			MXL_Out (mxl, dMXL, sfile);
			//cTag ("moxel");
		}
	}
	return;
}

bool	mxl_try (char *filename)	// try open file as mxl & translate it; call from 'main'
{
	MXL	mxl;
	Pdata	buffer;
	string	mxlname;

	buffer.data = NULL;
	if (!MXL_Load (filename, buffer))
		return (false);
	if (buffer.size > 147) {		// !!! against short
		if (!MXL_Decode (buffer, mxl))	{
			cerr << "(*)\tError decoding " << filename << endl;
			return (false);
		} else {
			mxlname = string(filename);
			MXL_Out (mxl, dMXL, mxlname);
		}
	}
	delete buffer.data;
	return (true);
}

bool	MXL_Load (char *fname, Pdata &buf)	{
	FILE	*fh;
	char	signature[] = "MOXCEL";

	// 1. open
	if (!(fh = fopen(fname, "rb")))	{
		cerr << "Error opening file " << fname << endl;
		return (false);
	}
	// 2. try signature
	if (fread (signature, 6, 1, fh) != 1)	{
		cerr << "(*)\tERROR: Can't read signature" << endl;
		fclose(fh);
		return (false);
	}
	if (strcmp(signature, "MOXCEL") != 0)
		return (false);
	// 3. define buffer size
	fseek (fh, 0L, SEEK_END);
	buf.size = ftell(fh);
	rewind(fh);
	// 4. alloc mem
	if (!(buf.data = new BYTE[buf.size]))	{
		cerr << "(*)\tERROR: Can't alloc mem 4 buffer" << endl;
		buf.size = 0l;
		fclose(fh);
		return (false);
	}
	// 5. load data
	if (fread(buf.data, buf.size, 1, fh) != 1)	{
		cerr << "(*)\tERROR: Can't read data 2 buffer" << endl;
		fclose(fh);
		return (false);
	}
	// 6. close & exit
	fclose(fh);
	return (true);
}
