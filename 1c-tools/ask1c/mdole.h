// mdole.h

#ifndef _MDOLE_H
#define _MDOLE_H

/// 1. includes
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

/// 2. usefull types
typedef	__uint8_t	BYTE;
typedef	__uint16_t	WORD;
typedef	__uint32_t	DWORD;
extern "C" {
#include <libole2/ms-ole.h>
}

using namespace std;

typedef vector<string>	SVector;
typedef vector<SVector>	DSVector;

/// 3. Constants
/// 3.1. Stream names
static string csCC	("Container.Contents");
static string csMD	("Metadata");
static string csMMS	("Main MetaData Stream");
static string csGD	("GUIDData");

/// 3.2. Storage names
static string csIF	("/UserDef/Page.1/Page.");
static string csPg1	("Page.1");
static string csPg2	("Page.2");
static string csRights	("/UserDef/Page.2");
static string csSUIT	("SubUsersInterfaceType");

/// 3.3. Dirs
static string dPathSep	("/");

//extern string dRoot;
/// 3.4. Misc
struct	Pdata	{
	DWORD	size;
	BYTE	*data;
};

class	MDOLE	{
	public:
			MDOLE (void);
			~MDOLE ();
		bool	open (string &);			// open CIF
		bool	open (char *);				// open CIF
		void	close (void);				// close CIF
		bool	ls (vector<string> &, string &);	// ls dir
		bool	IsStream (string &, string &);		// test stream type
		int	LoadStream(Pdata &, string &, string &);	// Load data from stream into Pdata
	private:
		bool	opened;					// "CIF opened" flag
		MsOle	*ole;					// CIF handler
};

#endif	// _MDOLE_H
