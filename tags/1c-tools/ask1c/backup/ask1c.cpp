// main.cpp
// Want to get:
//	1cv7.md:
//		* cfg name
//		* cfg ver.rel
//		* guiddata
//		* rights
//		* interfaces
//	USERS.USR:
//		* name
//		* password
//		* rights
//		* interface
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

#include "pole.h"

const char *mask = "{\"TaskItem\",\r\n{\"\\(\\w*\\)\",\"\\([^\"]*\\)\",\"\\([^\"]*\\)\",\"\\([^\"]*\\)\",\"\\([^\"]*\\)\",\"\\([^\"]*\\)\",\"\\([^\"]*\\)\",\"\\([^\"]*\\)\",\"\\([^\"]*\\)\",\"\\([^\"]*\\)\"";
//{"TaskItem",\r\n{"1","Бухгалтерский учет, редакция 4.5","7.70.483","","","1","493","0","0","493"}}

const int TOKENS = 10;

unsigned long	pls(POLE::Stream* stream)
/*
Get Pascal-like size of buffer and skip them
*/
{
	unsigned long result = 0L;
	stream->read( (unsigned char *) &result, 1);
	if (result == 0xFF) {
		stream->read( (unsigned char *) &result, 2);
		if (result == 0xFFFF)
			stream->read( (unsigned char *) &result, 4);
	}
	return result;
}

unsigned long	getbq( POLE::Storage* storage, char* stream_name, unsigned char* &buffer )
/*
Get bracket-quoted string w/ stream len in beginning
*/
{
	// 1. create stream
	POLE::Stream* stream = new POLE::Stream( storage, stream_name );
	if( !stream ) {
		printf ("Stream is none\n");
		return 0L;
	}
	if( stream->fail() ) {
		printf ("Stream is failed\n");
		return 0L;
	}
	// 2. get stream size
	unsigned long size = pls(stream);
	printf("Stream size: %d\n", size);
	// 3. make buffer
	buffer = (unsigned char *) malloc(size);
	if (buffer == NULL) {
		printf("Error allocating memory for buffer\n");
		return 0L;
	}
	// 4. read stream
	unsigned long read = stream->read( buffer, size );
	if( read != size ) {
		printf("Error loading stream\n");
		return 0L;
	}
	// x. that's all
	delete stream;
	return read;
}

unsigned long	cp1251_utf8(unsigned char* &buffer, unsigned long size)
/*
Converts inbound string from cp1251 to utf - inplace
*/
{
	iconv_t d;
	size_t ssize = size;
	size_t dsize = size * 2;
	char *result;
	char *sptr = (char *) buffer, *dptr;
	// 1. alloc mem
	result = (char *) malloc(dsize);
	if (result == NULL) {
		printf("Error allocating memory for buffer\n");
		return 0L;
	}
	d=iconv_open("UTF-8","CP1251");
	dptr = result;
	iconv(d, &sptr, &ssize, &dptr, &dsize);
	iconv_close(d);
	//free(buffer);
	unsigned long newsize = (size * 2) - dsize;
	buffer = (unsigned char *) realloc (result, newsize);
	//buffer =  (unsigned char *) result;
	return newsize;
}

void	extract( POLE::Storage* storage, char* stream_name, char* outfile )
{
	POLE::Stream* stream = new POLE::Stream( storage, stream_name );
	if( !stream ) return;
	if( stream->fail() ) return;

	std::ofstream file;
	file.open( outfile, std::ios::binary|std::ios::out );

	unsigned char buffer[16];
	for( ;; )
	{
		unsigned read = stream->read( buffer, sizeof( buffer ) );
		file.write( (const char*) buffer, read  );
		if( read < sizeof( buffer ) ) break;
	}
	file.close();

	delete stream;
}

void	decode(unsigned char *buffer)
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
		printf("\"%s\"\t", term[i]);
	}
	printf("\n");
}

void	out(unsigned char *s, unsigned long l, char *fn)
{
	std::ofstream file;
	file.open( fn, std::ios::binary|std::ios::out );
	file.write( (const char*) s, l );
	file.close();

}
int	main(int argc, char *argv[])
{
	unsigned char *mms;

	if( argc != 2 )
	{
		std::cout << "Usage:" << std::endl;
		std::cout << argv[0] << " filename" << std::endl;
		return 0;
	}

	char* filename = argv[1];

	POLE::Storage* storage = new POLE::Storage( filename );
	storage->open();
	if( storage->result() != POLE::Storage::Ok )
	{
		std::cout << "Error on file " << filename << std::endl;
		return 1;
	}

	//extract( storage, "/Metadata/Main\ MetaData\ Stream", "mms.txt");	// Metadata
	unsigned long size = getbq( storage, "/Metadata/Main\ MetaData\ Stream", mms);	// Metadata
	// 5. convert them
	printf("%d\n", size);
	//size = cp1251_utf8(mms, size);
	if (mms)	out(mms, size, "mms.txt");
	//extract( storage, "/Metadata/GUIDData", "guiddata.bin");			// GUIDData
	decode(mms);
	//extract (storage, "/UserDef/Page.1/Container.Contents", "interfaces.txt");	// Interfaces
	//extract (storage, "/UserDef/Page.2/Container.Contents", "rights.txt");	// Rights
	// Storage: UserDef/Page.1/Container.Contents
	// Storage: UserDef/Page.2/Container.Contents (Page.X) - rights
	// USERS.USR: /Container.Contents
	// USERS.USR: /Page.1
		
	delete storage;
	
	return 0;
}
