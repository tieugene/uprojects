/*
rpmtop.cpp - show all installed rpms - via rpm interface
ver.0.0.2 20070327

Compile:
	g++ -Wall -lrpm -o rpmtop rpmtop.cpp

Changelog:
	0.0.1	200703271800
		* 1st correctly working version
	0.0.2	200703272130
		* options handling improved
		* options Tops, Summary, Wide improved

TODO:
	* options
		* competitors
	* clean comments
	* cui/frontend
	* options:
		-w	w/ type (TAB, spaces, u-d-char
		-g	Graphiz output (future)\n"
		-o	Output filename (future)\n"
		-r	recuring
		-x	Excluding rpms (in recuring tops) (not implemented)\n"
		-X	Excluding rpms (in recuring tops) – from file (not implemented)\n"
*/

#include <fcntl.h>
#include <rpm/rpmcli.h>
#include <rpm/rpmdb.h>

#include <iostream>
#include <string>
#include <vector>
#include <set>
#include <map>

typedef	std::vector<std::string>		vString;
typedef std::set<std::string>			sString;
typedef std::map<std::string, std::string>	mSString;
typedef std::map<std::string, vString>		mSvString;	// string->[string]
typedef std::map<std::string, sString>		mSsString;	// string->[string]

const char	*Version	= "0.0.2";

static struct	{			// command-line options
	bool		Tops;
	bool		Competitors;
	std::string	OutFile;
	bool		Summary;
	int		Verbose;
	bool		Wide;
}	opts;

struct	mPkgRecord	{
	std::string	name;
	std::string	ver;
	std::string	rel;
	std::string	sum;
};

typedef	std::map<std::string, mPkgRecord>	mPkg;

// declarations
int	parseopts(int, const char *argv[]);
int	usage(void);
bool	HasKey(sString &v, const char * s) {return (v.find(s) != v.end());}
bool	HasKey(mSString &v, const char * s) {return (v.find(s) != v.end());}

// The Main
int main( int argc, const char *argv[] )
{
	parseopts(argc, argv);
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

		if (!opts.Wide)
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
	    if (opts.Tops) {
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
		// provide.files (very slow... need remake)
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
	}
	// 1.4. close iterator
	rpmdbFreeIterator(mi);
	// 1.5. close db
	rpmdbClose( db );
	mSsString	multiprovided;
    if (opts.Tops) {
	// 2. rebuild
//	fprintf(stdout, "Rebuilt...\n");
	// 2.1. files
	for (sString::const_iterator ii = required_file.begin(); ii != required_file.end(); ++ii) {
		mSString::const_iterator jj = provided_file.find (*ii);
		if (jj == provided_file.end()) {
			if (opts.Verbose)
				fprintf (stderr, "File \"%s\" is required but not provided.\n", ii->c_str());
		} else
			packages.erase (jj->second);
	}
	// 2.2. services
	for (sString::const_iterator ii = required_service.begin(); ii != required_service.end(); ++ii) {
		mSvString::const_iterator jj = provided_service.find (*ii);
		if (jj == provided_service.end()) {
			if (opts.Verbose)
				fprintf (stderr, "Service \"%s\" is required but not provided.\n", ii->c_str());
		} else {
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
    }
	for (mSString::const_iterator jj = dup_pkg.begin(); jj != dup_pkg.end(); ++jj) {				// for each dup_pkg
		mPkg::iterator kk = packages.find(jj->first);								// search in packages
		if (kk != packages.end()) {
			packages.insert(std::make_pair(jj->second, kk->second));
			packages.erase(kk);
		}
	}
	// 4. output
	// 4.1. orphans
	if (opts.Summary) {
		//int maxsize = 0;
		//for (mPkg::const_iterator ii = packages.begin(); ii != packages.end(); ++ii)
		//	maxsize = max(maxsize, ii->first.length());
		for (mPkg::const_iterator ii = packages.begin(); ii != packages.end(); ++ii)
			printf ("%s\t%s\n", ii->first.c_str(), ii->second.sum.c_str());
	} else
		for (mPkg::const_iterator ii = packages.begin(); ii != packages.end(); ++ii) {
			printf ("%s\n", ii->first.c_str());								// now can ... | expand -t 48
		}
	// 4.2. competitors
    if (opts.Verbose) {	// Competitors?
	for (mSsString::const_iterator ii = multiprovided.begin(); ii != multiprovided.end(); ++ii) {
		fprintf (stderr, "#%s:", ii->first.c_str());
		for (sString::const_iterator jj = ii->second.begin(); jj != ii->second.end(); ++jj)
//			std::cerr << " " << *jj;
			fprintf (stderr, " %s", jj->c_str());
//		for (uint_32 i = 0; i < ii->second.size(); i++)
//			printf (" %s", ii->second[i]);
		printf ("\n");
	}
    }
	// The End
//	rpmcliFini (options);
	return 0;
}

int	parseopts(int argc, const char *argv[]) {
	enum	{T_Ok = 1, C_Ok = 2, S_Ok = 3, V_Ok = 4, W_Ok = 5 };
	char	*outfile = NULL;
	static struct poptOption optionTable[] = {
	//	{ NULL, '\0', POPT_ARG_INCLUDE_TABLE, rpmcliAllPoptTable, 0, "Generic rpm options:", NULL },
		{ "tops",		't', POPT_ARG_NONE,	NULL,		T_Ok,	"List orphaned rpms.", NULL },
		{ "competitors",	'c', POPT_ARG_NONE,	NULL,		C_Ok,	"Include competitors rpms (for -t only).", NULL },
		{ "wide",		'w', POPT_ARG_NONE,	NULL,		W_Ok,	"Wide rpm name: name-version-release (default only competitors expanded).", NULL },
		{ "summary",		's', POPT_ARG_NONE,	NULL,		S_Ok,	"Print w/ rpm summary, devided by TAB; use expand -t for pretty report.", NULL },
		{ "output",		'o', POPT_ARG_STRING,	&outfile,	0,	"Output filename.", NULL },
		{ "verbose",		'v', POPT_ARG_INT,	&opts.Verbose,	0,	"Verbose level (default - 0).", NULL },
		{ "version",		'V', POPT_ARG_NONE,	NULL,		V_Ok,	"Print version and exit.", NULL },
		POPT_AUTOALIAS
		POPT_AUTOHELP
		POPT_TABLEEND
	};
	char	c;

	// 1. init options
	opts.Tops =
	opts.Competitors =
	opts.Summary =
	opts.Wide = false;
	// 2. get commanline
	poptContext options = poptGetContext(NULL, argc, argv, optionTable, 0);
	// 3. processing
	while ((c = poptGetNextOpt(options)) >= 0) {
		switch (c) {
			case T_Ok: 
				opts.Tops = true;
				break;
			case C_Ok: 
				opts.Competitors = true;
				break;
			case S_Ok:
				opts.Summary = true;
				break;
			case V_Ok:
				fprintf(stdout, "%s", Version);
				exit(0);
				break;
			case W_Ok:
				opts.Wide = true;
				break;
			default:
				fprintf(stderr, "%s: %s\n", poptBadOption(options, POPT_BADOPTION_NOALIAS), poptStrerror(c));
				exit(1);
		}
	}
	if (outfile)
		opts.OutFile = outfile;
	poptFreeContext(options);
	return 0;
}
