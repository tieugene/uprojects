// main.cpp
// main catmd module

#include "catmd.h"

#include <sys/stat.h>
#include <sys/types.h>
#ifdef __BORLANDC__
#include <dir.h>
#endif

string dRoot;
fstream ofile;

bool prepare (char *);

int main (int argc, char *argv[])
{
	MDOLE   ole;
	string  root ("/");

	if (argc != 3) {
		cerr << "Usage: " << argv[0] << " <MD|MXL-file> <target_dir>" << endl;
		return 1;
	}
	if (!prepare (argv[2])) {
		cerr << "Can't prepare target dir" << endl;
		return 1;
	}
	dRoot = string(argv[2]) + dPathSep;
	string sfile = dRoot + "cfg.xml";
	ofile.open(sfile.c_str(), ios::binary | ios::out);
	ofile << "<?xml version = '1.0' encoding = 'windows-1251'?>" << endl
	<< "<!DOCTYPE md SYSTEM \"catmd.dtd\">" << endl;
	if (!mxl_try (argv[1])) {
		if (!ole.open (argv[1])) {
			cerr << "Can't open file '" << argv[1] << "'" << endl;
			return 1;
		}
		ofile << "<md>" << endl;
		do_dir (ole, root);
		ole.close ();
		ofile << "</md>" << endl;
	}
	return 0;
}

// **** Utils ****//
void	Decode1C(Pdata & data)
// Decode given BYTE block
{
	DWORD	i;
	BYTE	key0[16] = {'\x60','\x46','\xD2','\x72','\x64','\x25','\x03','\x00','\x09','\x89','\x00','\xC0','\xDD','\x3B','\xE6','\x36'};
	BYTE	key[256], a = 0, b = 0, c = 0, d, e, g;

	// 1. Preparing coding array
	for (i = 0; i < 256; i++)
		key[i] = BYTE(i);
	for (i = 0; i < 256; i++) {
		a = key[i];
		b += (key0[i & '\xf'] + a);
		key[i] = key[b];
		key[b] = a;
	}
	// 2. Decoding
	a = 0;
	b = 0;
	c = key0[0];
	for (i = 0; i < data.size; i++) {
		a++;
		d = key[a];
		b += d;
		e = key[b];
		if (a == b)
			d = e = 0;
		key[b] = d;
		key[a] = e;
		g = d + e;
		d = data.data[i];
		data.data[i] = data.data[i] ^ c ^ key[g];
		c = d;
	}
}

bool prepare (char *d)
{
	// Prepare tag directory for usage - create needed dir and subdirs.
	// d - starting dir
	bool    retvalue = false;

	string  dir = string (d) + dPathSep;
	if (
#ifdef __BORLANDC__
		(!mkdir (dir.c_str ())) &&
		(!mkdir ((dir + dMXL ).c_str ())) &&
		(!mkdir ((dir + dBulk).c_str ())) &&
		(!mkdir ((dir + dGlr ).c_str ())) &&
		(!mkdir ((dir + dMDPT).c_str ())) &&
		(!mkdir ((dir + dDialog).c_str ())) &&
		(!mkdir ((dir + dTable).c_str ()))
#else
		(!mkdir (dir.c_str (), 0777)) &&
		(!mkdir ((dir + dMXL ).c_str (), 0777)) &&
		(!mkdir ((dir + dBulk).c_str (), 0777)) &&
		(!mkdir ((dir + dGlr ).c_str (), 0777)) &&
		(!mkdir ((dir + dMDPT).c_str (), 0777)) &&
		(!mkdir ((dir + dDialog).c_str (), 0777)) &&
		(!mkdir ((dir + dTable).c_str (), 0777))
#endif
		)
		retvalue = true;
	return retvalue;
}

void	oTag (const char * s, bool close)	// open tag
{
	ofile << "<" << s;
	if (close)
		eTag();
}

void	oTag (const string & s, bool close)	// open tag
{
	oTag(s.c_str(), close);
}

void	eTag (void)			// end tag
{
	ofile << ">" << endl;
}

void	cTag (const char * s)		// close tag
{
	if (s)
		ofile << "</" << s << ">" << endl;
	else
		ofile << "/>" << endl;
}

void	cTag (const string & s)
{
	cTag(s.c_str());
}

const WORD GetW (BYTE * bptr)
{
	return (*((WORD *) bptr));
}

const DWORD GetDW (BYTE * bptr)
{
	return (*((DWORD *) bptr));
}

string catdir (string & a, string & b)
{				// concatenate a/b
	string  r (a);

	if (a[a.length () - 1] != dPathSep[0])
		r += dPathSep;
	r += b;
	return (r);
}

string b2s (Pdata & data)
{				// return (BYTE *) to string
	string  stmp;
	char   *ctmp = (char *) malloc (data.size + 1);
	if (ctmp) {
		memcpy (ctmp, data.data, data.size);
		ctmp[data.size] = '\0';
		stmp = string (ctmp);
		free (ctmp);
	}
	return (stmp);
}

DWORD getsize (BYTE *&bptr)
{				// get Pascal-like string size
	DWORD   retvalue;

	if (*bptr != 0xFF) {	// 0..254 chars
		retvalue = *bptr;
		bptr += 1;
	} else if (GetW (bptr + 1) != 0xFFFF) {	// 255..64K-2 chars
		retvalue = GetW (bptr + 1);
		bptr += 3;
	} else if (GetDW (bptr + 3) != 0xFFFFFFFFL) {	// 4G-2
		retvalue = GetDW (bptr + 3);
		bptr += 7;
	} else {
		cerr << "Too big piece" << endl;
		return 0;
	}
	return (retvalue);
}

DWORD getsize (Pdata & data)
{				// get Pascal-like string size
	DWORD   retvalue;

	if (data.data[0] != 0xFF) {	// 0..254 chars
		retvalue = data.data[0];
		data.size -= 1;
		data.data += 1;
	} else if (GetW (data.data + 1) != 0xFFFF) {	// 255..64K-2 chars
		retvalue = GetW (data.data + 1);
		data.size -= 3;
		data.data += 3;
	} else if (GetDW (data.data + 3) != 0xFFFFFFFFL) {	// 4G-2
		retvalue = GetDW (data.data + 3);
		data.size -= 7;
		data.data += 7;
	} else {
		cerr << "Too big piece" << endl;
		return 0;
	}
	return (retvalue);
}

/* string * tune_str(string * s) {
	// prepare string for out as XML - replace & and " w/ entities
	string::size_type pos = 0;

	while ((pos = s->find_first_of('&', pos)) != string::npos)
		s->replace(pos++, 1, "&amp;");
	pos = 0;
	while ((pos = s->find_first_of('"', pos)) != string::npos)
		s->replace(pos++, 1, "&quot;");
	pos = 0;
	while ((pos = s->find_first_of('<', pos)) != string::npos)
		s->replace(pos++, 1, "&lt;");
	pos = 0;
	while ((pos = s->find_first_of('>', pos)) != string::npos)
		s->replace(pos++, 1, "&gt;");
	return s;
}*/

string * tune_str(string * s) {
	// prepare string for out as XML - replace & and " w/ entities
	DWORD	i = 0, sz = s->size(), ln;
	char	*r;

	while (i < sz) {
		switch((*s)[i])	{
			case ('&') :
				r = "&amp;";
				break;
			case ('"') :
				r = "&quot;";
				break;
			case ('<') :
				r = "&lt;";
				break;
			case ('>') :
				r = "&gt;";
				break;
			default:
				r = NULL;
		}
		if (r) {
			s->replace(i, 1, r);
			ln = strlen(r) - 1;
			i += ln;
			sz += ln;
		}
		i++;
	}
	return s;
}

static	char tmp[22];
string	hex02(BYTE a)	{ sprintf(tmp, "%02X", a);	return string(tmp); }
string	hex04(WORD a)	{ sprintf(tmp, "%04X", a);	return string(tmp); }
string	hex08(DWORD a)	{ sprintf(tmp, "%08X", a);	return string(tmp); }
string	i2s(int a)	{ sprintf(tmp, "%d",   a);	return (string(tmp)); }
string	i2s(WORD a)	{ sprintf(tmp, "%u",   a);	return (string(tmp)); }
string	i2s(DWORD a)	{ sprintf(tmp, "%lu",  a);	return (string(tmp)); }

//string	out_uid(DWORD i)	{ return (string(" uid=\"_") + i2s(i) + "\""); }
string	out_uid(string s)		{ return " uid=\"_" + s + "\""; }

string	out_uref(DWORD  i, char *pfx)	{ return ((i) ? string(" uref") + pfx + "=\"_" + i2s(i) + "\"" : ""); }
string	out_uref(string s, char *pfx)	{ return ((s != "0") ? string(" uref") + pfx + "=\"_" + s + "\"" : ""); }
