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
		Svc: name, [provider pkgs], [requirer pkgs]
		File: name, [provider pkgs], [requirer pkgs]
*/

#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <fstream>
#include <iostream>

#include <rpm/header.h>
#include <rpm/rpmlib.h>
#include <rpm/rpmdb.h>

#include "rpmtop.hpp"

// forward decls
int	parseopts(int, char *argv[]);
int	usage(void);

// utility
bool	HasKey(sString &, std::string &);
void	Name2ID_chk(const vString &, vInt &, const mNameInt &);
void	Name2ID(const vString &, vInt &, const mNameInt &);
void	ID2IDP(const vInt &, vSvcFile &, int);
void	ID2IDR(const vInt &, vSvcFile &, int);

// The Main
int main( int argc, char *argv[] )
{
	rpmdb			db;
	rpmdbMatchIterator	mi;
	Header			h;
	int_32			__count, i;
	char			*p;
	std::string		s;
	//vString			__lps, __lpf, __lrs, __lrf;
	sString			__dps, __dpf, __drf, __drs, __dUpes;	// for one pkg
	mNameInt		_dRF, _dRS;
	mNameInt::iterator	__ini;
	mPkgRecord		_dG_record;
	mPkg			_dG;
	mPkg::iterator		__iG;
	OutRecord		__sfRec;
	vSvcFile		Svc, File;
	PkgRecord		__pRec;
	vPkg			Pkg;

	// 1. load data
	// 1.1. open db
	std::cout << "Loading..." << std::endl;
	rpmReadConfigFiles( NULL, NULL );
	if( rpmdbOpen( "", &db, O_RDONLY, 0644 ) != 0 ) {
		std::cerr << "cannot open database!" << std::endl;
		exit( 1 );
	}
	// 1.2. open iterator
	mi = rpmdbInitIterator(db, RPMTAG_NAME, NULL, 0);	// header.h; was RPMDBI_PACKAGES
	// 1.3. iterate
	while ((h = rpmdbNextIterator(mi))) {
		// 1.3.1. get all values
		// name
		headerGetEntry(h, RPMTAG_NAME,        NULL, (void **) &p, NULL);
		_dG_record.name = p;
		// version
		headerGetEntry(h, RPMTAG_VERSION,     NULL, (void **) &p, NULL);	// t=6 RPM_STRING_TYPE, c=1
		_dG_record.ver = p;
		// release
		headerGetEntry(h, RPMTAG_RELEASE,     NULL, (void **) &p, NULL);
		_dG_record.rel = p;
		// provide.svc
		headerGetEntry(h, RPMTAG_PROVIDES, NULL, (void **) &p, &__count);		// t=8 RPM_STRING_ARRAY_TYPE, c=5
		for (i=0; i < __count; i++) {
			_dG_record.PS.push_back(((char **) p)[i]);
			__dps.insert(((char **) p)[i]);
		}
		free(p);
		//std::sort(_dG_record.PS.begin(), _dG_record.PS.end());
		// provide.files
		headerGetEntry(h, RPMTAG_OLDFILENAMES, NULL, (void **) &p, &__count);
		for (i=0; i < __count; i++) {
			__dpf.insert(((char **) p)[i]);
			_dG_record.PF.push_back(((char **) p)[i]);
		}
		free(p);
		//std::sort(_dG_record.PF.begin(), _dG_record.PF.end());
		// requires
		headerGetEntry(h, RPMTAG_REQUIRENAME, NULL, (void **) &p, &__count);
		for (i=0; i < __count; i++)	{
			s = ((char **) p)[i];
			if (s[0] == '/') {
				if (!(HasKey(__drf, s)))	{	// not found
					__drf.insert(s);
					_dRF[s] = 0;
					_dG_record.RF.push_back(((char **) p)[i]);
				}
			} else {
					if (!(HasKey(__drs, s) || HasKey(__dps, s)))	{
						__drs.insert(s);
						_dRS[s] = 0;
						_dG_record.RS.push_back(((char **) p)[i]);
					}
			}
		}
		free(p);
		__dpf.clear();			// empty
		__drs.clear();			// empty
		__drf.clear();			// empty
		//std::sort(_dG_record.RS.begin(), _dG_record.RS.end());
		// check
/*		std::cout
			<< "Name: " << _dG_record.name << ", Ver: " << _dG_record.ver << ", Rel: " << _dG_record.rel << std::endl
			<< "Provide.Svc:" << std::endl;
			for (i = 0; i < _dG_record.PS.size(); i++)
				std::cout << "\t" << _dG_record.PS[i] << std::endl;
*/
		// 1.3.1. print names
		//printf("%s\n", strdup(name));
		//break;
		// and insert pkg
		if (HasKey(__dUpes, _dG_record.name))	// dup
			s = _dG_record.name + "-" + _dG_record.ver + "-" + _dG_record.rel;
		else {							// not in dup
			if ((__iG = _dG.find(_dG_record.name)) == _dG.end())				// realy uniq
				s = _dG_record.name;
			else {
				__dUpes.insert(s);
				_dG[__iG->first + "-" + __iG->second.ver + "-" + __iG->second.rel] = __iG->second;	// make as new (iterate.first is r/o)
				_dG.erase(__iG);									// erase old
				s = _dG_record.name + "-" + _dG_record.ver + "-" + _dG_record.rel;
				
			}
		}
		_dG[s] = _dG_record;
	}
	__dUpes.clear();
	// 1.4. close iterator
	rpmdbFreeIterator(mi);
	// 1.5. close db
	rpmdbClose( db );
	// 2. rebuild
	std::cout << "Rebuilding..." << std::endl;
	for(i = 0, __ini = _dRS.begin(); __ini != _dRS.end(); __ini++, i++) {		// fill real indexes
		__ini->second = i;
		__sfRec.name = __ini->first;						// w/o constructor
		Svc.push_back(__sfRec);
	}
	for(i = 0, __ini = _dRF.begin(); __ini != _dRF.end(); __ini++, i++) {		// fill real indexes./rpm	
		__ini->second = i;
		__sfRec.name = __ini->first;
		File.push_back(__sfRec);
	}
	// 3. make out data
	std::cout << "Make work data..." << std::endl;
	for (i = 0, __iG = _dG.begin(); __iG != _dG.end(); __iG++, i++) {
		// 1. fill record
		_dG_record = __iG->second;
		__pRec.fullname	= __iG->first;
		__pRec.name	= __iG->second.name;
		__pRec.ver	= __iG->second.ver;
		__pRec.rel	= __iG->second.rel;
		// 8"
		Name2ID_chk(__iG->second.PS, __pRec.PS, _dRS);
		Name2ID_chk(__iG->second.PF, __pRec.PF, _dRF);
		Name2ID    (__iG->second.RS, __pRec.RS, _dRS);
		Name2ID    (__iG->second.RF, __pRec.RF, _dRF);
		// 23"
		// save
		Pkg.push_back(__pRec);
		ID2IDP(__pRec.PS, Svc, i);
		ID2IDR(__pRec.RS, Svc, i);
		ID2IDP(__pRec.PF, File, i);
		ID2IDR(__pRec.RF, File, i);

		std::cout << i << " ";
	}	// 25"
	std::cout << "The End..." << std::endl;
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
	std::cout << "Usage: rpmtop [options]\n"
		<< "Options:\n"
		<< "-c\tw/ concurent rpms\n"
		<< "-g\tGraphiz output\n"
		<< "-h\tHelp\n"
		<< "-l\tList top rpms. Default - 0 (all rpms)\n"
		<< "-o\tOutput filename\n"
		<< "-s\tList w/ rpm summary\n"
		<< "-x\tExcluding rpms (in recuring tops)\n"
		<< "-X\tExcluding rpms (in recuring tops) – from file\n"
		<< "-v\tEnable verbose mode\n"
		<< "-V\tPrint version and exit\n"
		<< std::endl;
	return (-1);
}

bool	HasKey(sString &v, std::string &s) {return (v.find(s) != v.end());}

void	Name2ID_chk(const vString &src, vInt &dst, const mNameInt &x) {
	mNameInt::const_iterator	__ini;
	vString::const_iterator	__is;

	dst.clear();
	for(__is = src.begin(); __is != src.end(); __is++)
		if ((__ini = x.find(*__is)) != x.end())
			dst.push_back(__ini->second);
	std::sort(dst.begin(), dst.end());
}

void	Name2ID(const vString &src, vInt &dst, const mNameInt &x) {
	vString::const_iterator	__is;

	dst.clear();
	for(__is = src.begin(); __is != src.end(); __is++) {
		dst.push_back(x.find(*__is)->second);
	}
	std::sort(dst.begin(), dst.end());
}

void	ID2IDP(const vInt &src, vSvcFile &dst, int v) {
	vInt::const_iterator	i;

	for(i = src.begin(); i != src.end(); i++)
		dst[*i].P.push_back(v);
}

void	ID2IDR(const vInt &src, vSvcFile &dst, int v) {
	vInt::const_iterator	i;

	for(i = src.begin(); i != src.end(); i++)
		dst[*i].R.push_back(v);
}
