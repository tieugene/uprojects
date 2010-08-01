// main.cpp
// Tool to extract guiddata and version from 1C 7.7
// Want:
//	* get cfg name
//	* get cfg ver.rel
//	* get guiddata
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

#include "pole.h"

//const char *mask = "^{{\"Server\",\"\\(\\w*\\)\"},{\"DB\",\"\\(\\w*\\)\"},{\"UID\",\"\\(\\w*\\)\"},{\"PWD\",\"\\(\\w*\\)\"},{\"Checksum\",\"\\(\\w*\\)\"}}$";
const char *mask = "{\"TaskItem\",\n{\"\\(\\w*\\)\",\"\\(\\w*\\)\",\"\\(\\w*\\)\",\"\\(\\w*\\)\",\"\\(\\w*\\)\",\"\\(\\w*\\)\",\"\\(\\w*\\)\",\"\\(\\w*\\)\",\"\\(\\w*\\)\",\"\\(\\w*\\)\"}";
//{"TaskItem",
//{"1","Бухгалтерский учет, редакция 4.5","7.70.483","","","1","493","0","0","493"}}

void dump( POLE::Storage* storage, char* stream_name )
{
	POLE::Stream* stream = new POLE::Stream( storage, stream_name );
	if( !stream ) return;
	if( stream->fail() ) return;
	
	// std::cout << "Size: " << stream->size() << " bytes" << std::endl;
	unsigned char buffer[16];
	for( ;; )
	{
			unsigned read = stream->read( buffer, sizeof( buffer ) );
			for( unsigned i = 0; i < read; i++ )
				printf( "%02x ", buffer[i] );
			std::cout << "    ";
			for( unsigned i = 0; i < read; i++ )
				printf( "%c", ((buffer[i]>=32)&&(buffer[i]<128)) ? buffer[i] : '.' );
			std::cout << std::endl;      
			if( read < sizeof( buffer ) ) break;
	}
	
	delete stream;
}

void extract( POLE::Storage* storage, char* stream_name, char* outfile )
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
		file.write( (const char*)buffer, read  );
		if( read < sizeof( buffer ) ) break;
	}
	file.close();
	
	delete stream;
}

int main(int argc, char *argv[])
{
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

	extract( storage, "/Metadata/Main\ MetaData\ Stream", "mms.txt");	// Metadata
	extract( storage, "/Metadata/GUIDData", "guiddata.bin");			// GUIDData
	//extract (storage, "/UserDef/Page.1/Container.Contents", "interfaces.txt");	// Interfaces
	//extract (storage, "/UserDef/Page.2/Container.Contents", "rights.txt");	// Rights
	// Storage: UserDef/Page.1/Container.Contents
	// Storage: UserDef/Page.2/Container.Contents (Page.X) - rights
	// USERS.USR: /Container.Contents
	// USERS.USR: /Page.1
		
	delete storage;
	
	return 0;
}
