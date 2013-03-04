// Show all installed rpms - via rpm interface
// Compile: gcc -Wall -lrpm -o rpmtop rpmtop.cpp

/*
TODO:
  * name all dup packets as name-ver-rel (< map: name>Array(name, ver, rel))
  * rpmgraph
Data:
	In:
		map PkgHash: [full]name > name, ver, rel, summary
	Mid:
		
	Out:
		Pkg: fullname, name, ver, rel, need, [PS], [PF], [RS], [RF]
		Svc: name, [provider packages], [requirer packages]
		File: name, [provider packages], [requirer packages]
*/

#include <fcntl.h>
#include <rpm/rpmcli.h>
#include <rpm/rpmdb.h>

#include <iostream>
#include <string>
#include <vector>
#include <set>
#include <map>

typedef	std::vector<std::string>	vString;
typedef std::set<std::string>		sString;

struct	Options		{	// command-line options
	bool	Concurent;
	bool	Graphics;
	bool	Level;
	vString	Exclude;
	int	Verbose;
};

// temporary
struct	mPkgRecord	{
	std::string	name;
	std::string	ver;
	std::string	rel;
};

typedef std::map<std::string, std::string>	mSString;
typedef std::map<std::string, vString>		mSMString;	// string->[string]
typedef	std::map<std::string, mPkgRecord>	mPkg;

static struct poptOption optionTable[] = {
	{ NULL, '\0', POPT_ARG_INCLUDE_TABLE, rpmcliAllPoptTable, \
		0, "Generic rpm options:", NULL },
	POPT_AUTOHELP
	POPT_TABLEEND
};

// declarations
int	parseopts(int, char *argv[]);
int	usage(void);
bool	HasKey(sString &v, const char * s) {return (v.find(s) != v.end());}

// The Main
int main( int argc, char *argv[] )
{

	// 1. load data
	// 1.1. open db
	poptContext options = rpmcliInit (argc, argv, optionTable);

	if (rpmReadConfigFiles (NULL, NULL) != 0) {
		fprintf (stderr, "rpmReadConfigFiles fail.\n");
		exit (1);
	}

	rpmdb db;

	if (rpmdbOpen ("", &db, O_RDONLY, 0) != 0) {
		fprintf (stderr, "rpmdbOpen failed.\n");
		exit (1);
	}

	rpmdbMatchIterator mi = rpmdbInitIterator (db, RPMTAG_NAME, NULL, 0);

	if (mi == NULL) {
		fprintf (stderr, "rpmdbInitIterator failed.\n");
		exit (1);
	}

	// 1.3. iterate
	mPkg		packages;
	mSMString	provided_service;
	mSString	provided_file;
	sString		dup_pkg, required_file, required_service;
	while (Header head = rpmdbNextIterator (mi)) {
		// 1.3.1. get all values
		const char * name;
		const char * version;
		const char * release;
	
		int res = headerNVR (head, &name, &version, &release);
		assert (res == 0);
		std::string fullname = name;
		fullname += "-";
		fullname += version;
		fullname += "-";
		fullname += release;
		// and insert pkg
		// 0. name
		mPkgRecord	_dG_record;
		_dG_record.name = name;
		_dG_record.ver = version;
		_dG_record.rel = release;

		if (!HasKey(dup_pkg, name)) {				// dup chk
			mPkg::iterator __iG = packages.find(name);
			if (__iG == packages.end())				// realy uniq
				fullname = name;
			else {
				dup_pkg.insert(name);
				packages[__iG->first + "-" + __iG->second.ver + "-" + __iG->second.rel] = __iG->second;	// make as new (iterate.first is r/o)
				packages.erase(__iG);									// erase old
			}
		}
		packages[fullname] = _dG_record;

		// provides
		int_32	htype;
		//hPTR_t	hptr;
		void	*hptr;
		int_32	hcount;

		// provide.svc
		sString		__dps;
		headerGetEntry(head, RPMTAG_PROVIDES, &htype, &hptr, &hcount);
		assert (htype == RPM_STRING_ARRAY_TYPE);
		for (int_32 i = 0; i != hcount; ++i) {
			const char * p = ((const char * const *) hptr)[i];
			__dps.insert(p);
			provided_service[p].push_back(fullname);
		}
		// provide.files
		sString		__dpf;
		headerGetEntry(head, RPMTAG_OLDFILENAMES, &htype, &hptr, &hcount);
		assert (htype == RPM_STRING_ARRAY_TYPE);
		for (int_32 i=0; i != hcount; ++i) {
			const char * p = ((const char * const *) hptr)[i];
			__dpf.insert(p);
			provided_file[p] = fullname;
		}
		// requires
		sString		__drf, __drs;
		headerGetEntry(head, RPMTAG_REQUIRENAME, &htype, &hptr, &hcount);
		assert (htype == RPM_STRING_ARRAY_TYPE);
		for (int_32 i=0; i != hcount; ++i)	{
			const char * p = ((const char * const *) hptr)[i];
			if (*p == '/') {
				if (!(HasKey(__drf, p)))	{	// against dupes
					__drf.insert(p);
					required_file.insert(p);
				}
			} else {
					if (!(HasKey(__drs, p) || HasKey(__dps, p)))	{	// against dupes and loopback
						__drs.insert(p);
						required_service.insert(p);
					}
			}
		}
		__dpf.clear();			// empty
		__dps.clear();			// empty
		__drf.clear();			// empty
		__drs.clear();			// empty
	}
	dup_pkg.clear();
	// 1.4. close iterator
	rpmdbFreeIterator(mi);
	// 1.5. close db
	rpmdbClose( db );
	// 2. rebuild
	// 2.1. files
	for (sString::const_iterator ii = required_file.begin(); ii != required_file.end(); ++ii) {
		mSString::const_iterator jj = provided_file.find (*ii);
		if (jj == provided_file.end())
			fprintf (stderr, "File \"%s\" is required but not provided.\n", ii->c_str());
		else
			packages.erase (jj->second);
	}
	// 2.2. services
	mSMString	multiprovided;
	for (sString::const_iterator ii = required_service.begin(); ii != required_service.end(); ++ii) {
		mSMString::const_iterator jj = provided_service.find (*ii);
		if (jj == provided_service.end())
			fprintf (stderr, "Service \"%s\" is required but not provided.\n", ii->c_str());
		else {
			if (jj->second.size() == 1)	// uniq provider
				packages.erase (jj->second[0]);
			else				// multiprovided
//				for (sString::const_iterator kk = jj->second.begin(); kk != jj->second.end(); ++kk)
//					multiprovided[*ii].push_back(*kk);
				multiprovided[*ii] = jj->second;
		}
	}
	// 3. tune competitors
	// 4. output
	// 4.1. orphans
	for (mPkg::const_iterator ii = packages.begin(); ii != packages.end(); ++ii) {
		printf ("%s\n", ii->first.c_str());
	}
	// 4.2. competitors
	fprintf(stdout, "=== Competitors ===\n");;
	for (mSMString::const_iterator ii = multiprovided.begin(); ii != multiprovided.end(); ++ii) {
		printf ("%s:\n", ii->first.c_str());
//		for (vString::const_iterator jj = ii->second.begin(); jj != ii->second.end(); ++jj)
//			printf (" %s", *jj);
//		for (uint_32 i = 0; i < ii->second.size(); i++)
//			printf (" %s", ii->second[i]);
		//printf ("\n");
	}
	// The End
	rpmcliFini (options);
	return 0;
}

int	parseopts(int argc, char *argv[]) {
	// Parse the command line arguments
	char ch, lastChar;
	extern char *optarg;
	std::string a, b;
	
	while ((ch = getopt(argc, argv, "h:i:")) != EOF)
		switch (ch) {
		case 'h':
			a = optarg;
			lastChar = *optarg;
			if (lastChar != '/' && lastChar != '\\')
				return (usage());
			break;
		case 'i':
			b = optarg;
			break;
		case '?':
		default:
			return (usage());
			break;
		}
	return (0);
}

int	usage(void) {
	fprintf(stdout, "Usage: rpmtop [options]\n"
		"Options:\n"
		"-c\tw/ concurent rpms\n"
		"-g\tGraphiz output\n"
		"-head\tHelp\n"
		"-l\tList top rpms. Default - 0 (all rpms)\n"
		"-o\tOutput filename\n"
		"-s\tList w/ rpm summary\n"
		"-x\tExcluding rpms (in recuring tops)\n"
		"-X\tExcluding rpms (in recuring tops) – from file\n"
		"-v\tEnable verbose mode\n"
		"-V\tPrint version and exit\n");
	return (-1);
}
