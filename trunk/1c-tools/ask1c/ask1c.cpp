// main.cpp
// Want to get:
//	1cv7.md:
//		* cfg name
//		* cfg rel
//		* guiddata
//		* rights
//		* interfaces
//	USERS.USR:
//		* name
//		* password
//		* rights
//		* interface
// Functions:
//	* get raw mms
//	* get cfg name
//	* get cfg ver
//	* get GUIDData (DWORD size + size*uint16)
/*
- Метаданные
	- Идентификатор	"Бухгалтерский учет, редакция 4.5"
	- Комментарий	"7.70.483"

/Metadata/Main MetaData Stream/TaskItem
/Metadata/GUIDData

*/

#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <stdio.h>
#include <list>
#include <string>
#include <regex.h>
#include <err.h>
#include <iconv.h>

#include "mdole.h"

const char *mask = "{\"TaskItem\",\r\n{\"\\(\\w*\\)\",\"\\([^\"]*\\)\",\"\\([^\"]*\\)\",\"\\([^\"]*\\)\",\"\\([^\"]*\\)\",\"\\([^\"]*\\)\",\"\\([^\"]*\\)\",\"\\([^\"]*\\)\",\"\\([^\"]*\\)\",\"\\([^\"]*\\)\"";
//{"TaskItem",\r\n{"1","Бухгалтерский учет, редакция 4.5","7.70.483","","","1","493","0","0","493"}}

const int TOKENS = 10;

DWORD	pls(BYTE* &ptr)
/*
 * handle pascal-like string:
 * 1. return real size
 * 2. move ptr into real start
 */
{
	DWORD result = 0L;
	result = *ptr;
	ptr++;
	if (result == 0xFF) {
		result = *((WORD *) ptr);
		ptr += 2;
		if (result == 0xFFFF) {
			result = *((DWORD *) ptr);
			ptr += 4;
		}
	}
	return result;
}

void	desize(Pdata &src)
/*
 * Remove head pascal size
 */
{
	BYTE *ptr = src.data, *newdata;
	DWORD newsize = pls(ptr);
	newdata = (BYTE *) malloc(newsize + 1);
	if (newdata == NULL) {
		printf("desize: Error allocating memory for buffer\n");
		return;
	}
	memcpy(newdata, ptr, newsize + 1);
	g_free(src.data);
	src.data = newdata;
	src.size = newsize;
}

void	win2utf(Pdata &data)
/*
 * Converts inbound string from cp1251 to utf - inplace
*/
{
	size_t ssize = data.size, dsize = data.size * 2;
	BYTE *sptr = data.data, *dptr, *newdata;
	// 1. alloc mem
	newdata = (BYTE *) malloc(dsize);
	if (newdata == NULL) {
		printf("win2utf: Error allocating memory for buffer\n");
		return;
	}
	dptr = newdata;
	iconv_t d = iconv_open("UTF-8", "CP1251");
	iconv(d, (char **) &sptr, &ssize, (char **) &dptr, &dsize);
	iconv_close(d);
	free(data.data);
	data.size = (data.size * 2) - dsize;
	data.data = (BYTE *) realloc (newdata, data.size);
}

void	decode(BYTE *buffer, SVector &names)
{
	int		reti;
	unsigned char	*term[TOKENS];
	regex_t		regex;
	regmatch_t	match[TOKENS + 1];

	// 1. prepare regex
	reti = regcomp(&regex, mask, 0);
	if( reti )
		err(-1, "Error compiling regex");
	// 5. split on parts
	reti = regexec(&regex, (const char *) buffer, TOKENS + 1, match, 0);
	if (reti)
		err(-2, "Error matching regex");
	for (int i = 0; i < TOKENS; i++) {
		buffer[match[i + 1].rm_eo] = '\0';	// set EOL
		term[i] = &buffer[match[i+1].rm_so];	// set term
	// 6. show values
		names.push_back(string((const char *) term[i]));
		//printf("\"%s\"\t", term[i]);
	}
}

void	out(Pdata data, char *fn)
{
	std::ofstream file;
	file.open( fn, std::ios::binary|std::ios::out );
	file.write( (const char*) data.data, data.size );
	file.close();

}

void	outguid(Pdata data, char *fn)
{
	DWORD size = *((DWORD *) data.data);
	DWORD *ptr = (DWORD *) (data.data + 4);

	cout << "Size:" << size << endl;
	std::ofstream file;
	file.open( fn, std::ios::binary|std::ios::out );
	for (int i = 0; i < size; i++) {
		//cout << hex << uppercase << ptr[3] << ptr[2] << ptr[1] << ptr[0] << endl;
		printf ("%08X%08X%08X%08X\n", ptr[3], ptr[2], ptr[1], ptr[0]);
		ptr += 4;
	}
	file.write( (const char*) data.data+4, data.size-4 );
	file.close();

}

int	main(int argc, char *argv[])
{
	MDOLE	ole;
        Pdata	mms, guid, guidtmp, rights, ifs;
	SVector	smms;

	if( argc != 2 )
	{
		std::cout << "Usage:" << std::endl;
		std::cout << argv[0] << " filename" << std::endl;
		return 0;
	}

	if (!ole.open (argv[1])) {
		cerr << "Can't open file '" << argv[1] << "'" << endl;
		return 1;
	}
        if (ole.LoadStream (mms, csMD, csMMS))
		cerr << "Can't load Metadata/MMS" << endl;
        if (ole.LoadStream (guid, csMD, csGD))
		cerr << "Can't load Metadata/GUIDData" << endl;
	ole.close ();

	desize(mms);
	win2utf(mms);
	decode(mms.data, smms);
	//for (int i=0; i < smms.size(); i++)
	cout << smms[1] << "\t" << smms[2] << endl;
	guidtmp.data = guid.data + 4; guidtmp.size = guid.size - 4;
	out(guid, "guid.raw");
	out(guidtmp, "guid.bin");
	outguid(guid, "guid.hex");
	//extract( storage, "/Metadata/GUIDData", "guiddata.bin");			// GUIDData
	//extract (storage, "/UserDef/Page.1/Container.Contents", "interfaces.txt");	// Interfaces
	//extract (storage, "/UserDef/Page.2/Container.Contents", "rights.txt");	// Rights
	// Storage: UserDef/Page.1/Container.Contents
	// Storage: UserDef/Page.2/Container.Contents (Page.X) - rights
	// USERS.USR: /Container.Contents
	// USERS.USR: /Page.1
		
	return 0;
}
