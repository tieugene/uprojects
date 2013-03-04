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

#ifndef	_COMMON_H
#define	_COMMON_H

/// 1. includes
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

/// 2. usefull types
#ifdef __BORLANDC__	// Windows
#include <io.h>
typedef	unsigned char	BYTE;
typedef	unsigned short	WORD;
typedef	unsigned long	DWORD;
typedef	unsigned int	uint;
#else			// Linux
typedef	__uint8_t	BYTE;
typedef	__uint16_t	WORD;
typedef	__uint32_t	DWORD;
#endif

using namespace std;

typedef vector<string>	SVector;
typedef vector<SVector>	DSVector;

//#include "parser.h"

/// 3.4. Misc
struct	Pdata	{
	DWORD	size;
	BYTE	*data;
};

/// 5. Func decls
void		Decode1C(Pdata &);
string		hex02(BYTE);
string		hex04(WORD);
string		hex08(DWORD);
const WORD	GetW(BYTE *);
const DWORD	GetDW(BYTE *);
string		i2s(int);
string		i2s(WORD);
string		i2s(DWORD);
string		out_uid(string);
string		out_uref(DWORD, char *pfx = "");
string		out_uref(string, char *pfx = "");
void		oTag (const char * s = NULL, bool close = false);
void		oTag (const string &, bool close = false);
void		eTag (void);
void		cTag (const char * s = NULL);
void		cTag (const string &);
DWORD		getsize (Pdata &);					// get Pascal-like string size
DWORD		getsize (BYTE *&);
string *	tune_str(string *);					// replace non-xml chars into entities
bool		recrmdir(const char *);
string		b2s(Pdata &);
// buffer into another
int		unpack_data(Pdata &, Pdata &);
void		print_str(char *);
void		print_data(Pdata &);					// print text stream
//void		print_sized_data(Pdata &);				// print text stream checking forward len bytes
void		print_packed_data (Pdata &, string &, string &, bool);	// print or dump packed data
void		print_bq(Pdata &);					// print "bracketed-quoted" text
void		dump_data(Pdata &, string &, string &, int mode = O_CREAT|O_RDWR|O_TRUNC);	// write bulk data into file
void		dump_fpdata(Pdata &, string &, string &);		// write bulk data into file w/ "full path"
string		catdir (string &, string &);

#endif	// _CATMD_H
