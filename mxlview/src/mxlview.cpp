/***************************************************************************
 *   Copyright (C) 2007 by Eugene A. Pivnev   *
 *   ti.eugene@gmail.com   *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program; if not, write to the                         *
 *   Free Software Foundation, Inc.,                                       *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
 ***************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <iostream>
#include <cstdlib>
#include "common.h"
#include "parser.h"
#include "core.h"
#include "decoder.h"
#include "toxml.h"

using	namespace std;

//char	*test_argv1 = "/mnt/shares/home/eugene/Projects/mxlview/debug/src/test.mxl";

static	DWORD TCounter = 0;

//Moxel	data;	// какого-то хрена нельзя внутри mxl_try - разрушается при вызове MXL_Decode


bool	mxl_try (char *);
bool	MXL_Load (char *, Pdata &);

int	main(int argc, char *argv[])
{
	fstream ofile;

	if (argc != 2) {
		cerr << "Usage: " << argv[0] << " <MXL-file>" << endl;
		return 1;
	}
	if (!mxl_try (argv[1])) {
			cerr << "Can't open file '" << argv[1] << "'" << endl;
			return 1;
		}
	return EXIT_SUCCESS;
//	mxl_try (test_argv1);
}

bool	mxl_try (char *filename)	// try open file as mxl & translate it; call from 'main'
{
	MXL	mxl;
	Moxel	outobject;
	Pdata	buffer;

	buffer.data = NULL;
	if (!MXL_Load (filename, buffer))
		return (false);
	if (buffer.size > 147) {		// !!! against short
cerr << "Loaded OK" << endl;
		if (!MXL_Parse (buffer, mxl))	{
			cerr << "(*)\tError decoding " << filename << endl;
			return (false);
		} else {
cerr << "Parsed OK. Start decode..." << endl;
			MXL_Decode(mxl, outobject);
cerr << "Decoded OK" << endl;
			Export_XML(outobject);
cerr << "Exported OK" << endl;
		}
	}
	return (true);
}

bool	MXL_Load (char *fname, Pdata &buf)	{	// Alloc mem for mxl and Load mxl-file into
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
