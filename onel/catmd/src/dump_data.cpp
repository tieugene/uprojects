// dump_data.cpp
#include "catmd.h"

#include <sys/types.h>
#include <sys/stat.h>
#ifndef __BORLANDC__
#include <unistd.h>
#endif

extern string dRoot;

static const char splitter = '#';	//  split char for filename (or !@#%^)

void	dump_fpdata(Pdata &data, string & dir, string & file)
// write given stream into file as "undecoded": storage|storage|...|streamname
{
	string	tmp = file;
	DWORD	i;

	for (i = 1; i < tmp.length(); i++)
		if (tmp[i] == '/')
			tmp[i] = splitter;
	dump_data(data, dir, tmp);
}

void	dump_data(Pdata &data, string & dir, string & file, int mode)	// was S_IRUSR | S_IWUSR
// write given block into file
{
	int	fn;
	string	filename;

	filename = dRoot + catdir(dir, file);
	if ((fn = open(filename.c_str(), mode, S_IREAD|S_IWRITE)) == -1)	{
		cerr << "Error opening file " << filename << endl;
		return;
	}
	if (write(fn, data.data, data.size) != data.size)
		cerr << "Error writing file " << filename << endl;
	close(fn);
	return;
}
