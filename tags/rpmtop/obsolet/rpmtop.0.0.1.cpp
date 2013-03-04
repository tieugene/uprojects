//	rpmtop.cpp - show all installed rpms - via rpm interface
//	ver.0.0.1 20070327
//	Compile: g++ -Wall -lrpm -o rpmtop rpmtop.cpp
/*
TODO:
	* options
		* w/ summary
		* -c
		* -wide
		* -a
	* clean comments
	* cui/frontend
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
	std::string	sum;
};

typedef std::map<std::string, std::string>	mSString;
typedef std::map<std::string, vString>		mSvString;	// string->[string]
typedef std::map<std::string, sString>		mSsString;	// string->[string]
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
bool	HasKey(mSString &v, const char * s) {return (v.find(s) != v.end());}

// The Main
int main( int argc, char *argv[] )
{

	// 1. load data
	// 1.1. open db
//	poptContext options = rpmcliInit (argc, argv, optionTable);

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
	mSvString	provided_service;
	mSString	provided_file, dup_pkg;
	sString		required_file, required_service;
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

		if (!HasKey(dup_pkg, name)) {									// dup chk
			mPkg::iterator __iG = packages.find(name);
			if (__iG == packages.end())								// realy uniq
				fullname = name;
			else
				dup_pkg.insert(std::make_pair(name, __iG->second.name + "-" + __iG->second.ver + "-" + __iG->second.rel));
//fprintf(stdout, "Pkg %s duplicated\n", name);
		}

		// provides
		int_32	htype;
		//hPTR_t	hptr;
		void	*hptr;
		int_32	hcount;

		// summary
		headerGetEntry(head, RPMTAG_SUMMARY, &htype, &hptr, &hcount);
		_dG_record.sum = (const char *) hptr;
		packages[fullname] = _dG_record;
		// provide.svc
		sString		__dps;
		headerGetEntry(head, RPMTAG_PROVIDES, &htype, &hptr, &hcount);
		assert (htype == RPM_STRING_ARRAY_TYPE);
		for (int_32 i = 0; i != hcount; ++i) {
			const char * p = ((const char * const *) hptr)[i];
			if (!HasKey(__dps, p)) {
				__dps.insert(p);
				provided_service[p].push_back(fullname);
			}
		}
		// provide.files
		sString		__dpf;
		vString		__dirname;
		void		*__dirindex;
///		headerGetEntry(head, RPMTAG_OLDFILENAMES, &htype, &hptr, &hcount);
		// 1. get all dirs
		headerGetEntry(head, RPMTAG_DIRNAMES, &htype, &hptr, &hcount);
		for (int_32 i = 0; i < hcount; i++)
			__dirname.push_back(((const char * const *) hptr)[i]);
		// 2. get all indexes
		headerGetEntry(head, RPMTAG_DIRINDEXES, &htype, &__dirindex, &hcount);
		// 3. get all names
		headerGetEntry(head, RPMTAG_BASENAMES, &htype, &hptr, &hcount);
		for (int_32 i = 0; i < hcount; i++) {
			std::string p = __dirname[((int_32 *) __dirindex)[i]] + ((const char * const *) hptr)[i];
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
				if (!HasKey(__drf, p))	{	// against dupes
					__drf.insert(p);
					required_file.insert(p);
				}
			} else {
					if (!(HasKey(__drs, p) || HasKey(__dps, p)))	{			// against dupes and loopback
						__drs.insert(p);
						required_service.insert(p);
					}
			}
		}
	}
	// 1.4. close iterator
	rpmdbFreeIterator(mi);
	// 1.5. close db
	rpmdbClose( db );
	// 2. rebuild
//	fprintf(stdout, "Rebuilt...\n");
	// 2.1. files
	for (sString::const_iterator ii = required_file.begin(); ii != required_file.end(); ++ii) {
		mSString::const_iterator jj = provided_file.find (*ii);
		if (jj == provided_file.end())
			fprintf (stderr, "File \"%s\" is required but not provided.\n", ii->c_str());
		else
			packages.erase (jj->second);
	}
	// 2.2. services
	mSsString	multiprovided;
	for (sString::const_iterator ii = required_service.begin(); ii != required_service.end(); ++ii) {
		mSvString::const_iterator jj = provided_service.find (*ii);
		if (jj == provided_service.end())
			fprintf (stderr, "Service \"%s\" is required but not provided.\n", ii->c_str());
		else {
			if (jj->second.size() == 1)	// uniq provider
				packages.erase (jj->second[0]);
			else {				// multiprovided
//fprintf(stdout, "Service %s provided by %d pkgs:\n", jj->first.c_str(), jj->second.size());
				for (vString::const_iterator kk = jj->second.begin(); kk != jj->second.end(); ++kk)
					multiprovided[*ii].insert(*kk);
			}
		}
	}
	// 3. tune competitors
	// 3.1. clean
	bool NeedNext;
	do {
		NeedNext = false;
		vString mp2del;												// multiprovided to delete
		for (mSsString::iterator ii = multiprovided.begin(); ii != multiprovided.end(); ++ii) {			// for each service
			vString mpkg2del;										// pkgs from this multiprovided to delete
//			std::vector <sString::const_iterator> mpkg2del;
			switch (ii->second.size()) {
			case (0):											// empty
				mp2del.push_back(ii->first);								// delete this entry later
//fprintf(stderr, "Service \"%s\" removed.\n", ii->first.c_str());
				NeedNext = true;
				break;
			case (1):
				//packages.erase(*ii->second.begin());
				mp2del.push_back(ii->first);								// delete this entry later
//fprintf(stderr, "From service \"%s\" removed last pkg \"%s\".\n", ii->first.c_str(), ii->second.begin()->c_str());
				NeedNext = true;
				break;
			default:
				for (sString::const_iterator jj = ii->second.begin(); jj != ii->second.end(); ++jj) {	// and for each pkg
					if (packages.find(*jj) == packages.end()) {					// pkg not in orphaned
						mpkg2del.push_back(*jj);
//fprintf(stderr, "From service \"%s\" removed pkg \"%s\".\n", ii->first.c_str(), jj->c_str());
						NeedNext = true;
					}
				}
			}
			for (vString::const_iterator jj = mpkg2del.begin(); jj != mpkg2del.end(); ++jj)			// delete marked pkgs from service
//			for (std::vector<sString::const_iterator>::const_iterator jj = mpkg2del.begin(); jj != mpkg2del.end(); ++jj)			// delete marked pkgs from service
				ii->second.erase(*jj);
		}
		for (vString::const_iterator jj = mp2del.begin(); jj != mp2del.end(); ++jj)				// delete empty services (try iterator)
			multiprovided.erase(*jj);
	} while (NeedNext);
	// 3.2. rename 1st of duplicated to full name - for correct sorting
	// 3.2.1. multiprovided
	for (mSsString::iterator ii = multiprovided.begin(); ii != multiprovided.end(); ++ii)				// for each multiprovided
//		for (sString::iterator jj = ii->second.begin(); jj != ii->second.end(); ++jj)
		for (mSString::const_iterator jj = dup_pkg.begin(); jj != dup_pkg.end(); ++jj) {			// for each dup_pkg
			sString::iterator kk = ii->second.find(jj->first);						// search in multiprovided pkgs
			if (kk != ii->second.end()) {
				ii->second.insert(jj->second);								// insert new
				ii->second.erase(kk);
			}
		}
	// 3.2.2. packages
	for (mSString::const_iterator jj = dup_pkg.begin(); jj != dup_pkg.end(); ++jj) {				// for each dup_pkg
		mPkg::iterator kk = packages.find(jj->first);								// search in packages
		if (kk != packages.end()) {
			packages.insert(std::make_pair(jj->second, kk->second));
			packages.erase(kk);
		}
	}
	// 4. output
	// 4.1. orphans
	for (mPkg::const_iterator ii = packages.begin(); ii != packages.end(); ++ii)
		printf ("%s\n", ii->first.c_str());
	// 4.2. competitors
	for (mSsString::const_iterator ii = multiprovided.begin(); ii != multiprovided.end(); ++ii) {
		printf ("#%s:", ii->first.c_str());
		for (sString::const_iterator jj = ii->second.begin(); jj != ii->second.end(); ++jj)
//			std::cerr << " " << *jj;
			printf (" %s", jj->c_str());
//		for (uint_32 i = 0; i < ii->second.size(); i++)
//			printf (" %s", ii->second[i]);
		printf ("\n");
	}
	// The End
//	rpmcliFini (options);
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
		"-g\tGraphiz output (future)\n"
		"-h\tHelp\n"
		"-o\tOutput filename (future)\n"
		"-s\tList w/ rpm summary\n"
		"-l\tList top rpms. Default - 0 (all rpms)\n"
		"-x\tExcluding rpms (in recuring tops) (not implemented)\n"
		"-X\tExcluding rpms (in recuring tops) – from file (not implemented)\n"
		"-v\tEnable verbose mode\n"
		"-V\tPrint version and exit\n"
		"-w\tWide format for all pkgs - name-version-release (default - for competitors only)\n");
	return (-1);
}
