// mdole_l.cpp - Linux-oriented.
// Based on libole2

#include "mdole.h"

#ifdef __cplusplus
extern "C" {
#endif
#include <libole2/ms-ole.h>
#include <libole2/ms-ole-summary.h>
#ifdef __cplusplus
}
#endif

// constructor
MDOLE::MDOLE (void) {
	opened = false;
}

// destructor
MDOLE::~MDOLE () {
	if (opened)
		ms_ole_destroy (&ole);
}

// open file
bool	MDOLE::open (char *filename) {
	if (opened)
		close();
	opened = (ms_ole_open_vfs (&ole, filename, TRUE, NULL) == MS_OLE_ERR_OK);
	return (opened);
}

bool	MDOLE::open (string &filename) {
	if (opened)
		close();
	opened = (ms_ole_open_vfs (&ole, filename.c_str(), TRUE, NULL) == MS_OLE_ERR_OK);
	return (opened);
}

// close file
void	MDOLE::close (void) {
	ms_ole_destroy (&ole);
	opened = false;
}

bool	MDOLE::ls (vector<string> &names, string &dir) {
	char	**nam;
	int	i;

	if (ms_ole_directory (&nam, ole, dir.c_str()) != MS_OLE_ERR_OK) {
		return (false);
	}
	for (i = 0; nam[i]; i++) {
		names.push_back(string (nam[i]));
	}
	return (true);
}

bool	MDOLE::IsStream (string &dir, string &file) {
	MsOleStat s;

	ms_ole_stat (&s, ole, dir.c_str(), file.c_str());	// result = ...
	return (s.type == MsOleStreamT);
}

int	MDOLE::LoadStream (Pdata &data, string &dir, string &file) {
	MsOleStat	s;
	MsOleStream	*stream;
	
	data.size = 0;
	if (ms_ole_stat (&s, ole, dir.c_str(), file.c_str()) != MS_OLE_ERR_OK)
		return 1;	// cant get stat
	if (ms_ole_stream_open (&stream, ole, dir.c_str(), file.c_str(), 'r') != MS_OLE_ERR_OK)
		return 2;	// cant open stream
	data.data = (BYTE *) g_malloc (stream->size);	// !!! new - not works !!!
	if (!data.data)		// cant alloc mem
		return 3;
	stream->read_copy (stream, data.data, stream->size);
	if (!data.data)
		return 4;
	ms_ole_stream_close (&stream);
	data.size = s.size;
	return 0;
}
