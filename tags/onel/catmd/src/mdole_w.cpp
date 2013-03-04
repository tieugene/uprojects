// mdole_w.cpp - Windows-oriented.
// Based on POLE

#include "catmd.h"

// constructor
MDOLE::MDOLE (void) {
	opened = false;
}

// destructor
MDOLE::~MDOLE () {
	if (opened)
		delete storage;
}

// open file
bool	MDOLE::open (char *filename) {

	if (opened)
		close();
	storage = new POLE::Storage(filename);
	opened = storage->open();
	return (opened);
}

bool	MDOLE::open (string &filename) {
	if (opened)
		close();
	storage = new POLE::Storage(filename.c_str());
	opened = storage->open();
	return (opened);
}

// close file
void	MDOLE::close (void) {
	storage->close();
	opened = false;
}

bool	MDOLE::ls (vector<string> &names, string &dir)
{
	std::list<std::string> entries;
	string P;
	P = '/';
	if (dir.c_str() == P)
		entries = storage->entries(dir);
	else
		entries = storage->entries((dir[0] == '/') ? dir.substr(1) : dir);
	std::list<std::string>::iterator it;
	for( it = entries.begin(); it != entries.end(); ++it )
	{
		std::string n = *it;
		names.push_back(n);
	}
	return true;
}

bool MDOLE::IsStream (string &dir, string &file) {
    string stream_name;
	string P;
	P = '/';
	if (dir.c_str() != P)
		stream_name = ((dir[0]=='/')? dir.substr(1):dir) + '/' + file;
    else
		stream_name = file;
	return !storage->isDirectory(stream_name);
}

int	MDOLE::LoadStream (Pdata &data, string &dir, string &file)
{
    string stream_name;
	string P;
	P = '/';
    if (dir.c_str() != P)
		stream_name = ((dir[0]=='/')?dir.substr(1):dir) + '/' + file;
    else
		stream_name = file;

    data.size = 0;
	POLE::Stream* stream = new POLE::Stream(storage, stream_name );
	if( !stream )
		return 2; // cant open stream

	data.data = (BYTE*) malloc (stream->size());
	if (!data.data)	
		return 3;// cant alloc

	unsigned read = stream->read(data.data,stream->size());
	if (!data.data)
		return 4;//cant read
	data.size = read;
	return 0;
}
