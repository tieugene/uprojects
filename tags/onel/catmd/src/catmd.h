// catmd.h

#ifndef _CATMD_H
#define _CATMD_H

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
#ifdef __BORLANDC__	// Windows
#include <io.h>
#include "pole.h"
typedef	unsigned char	BYTE;
typedef	unsigned short	WORD;
typedef	unsigned long	DWORD;
typedef	unsigned int	uint;
#else			// Linux
typedef	__uint8_t	BYTE;
typedef	__uint16_t	WORD;
typedef	__uint32_t	DWORD;
extern "C" {
#include <libole2/ms-ole.h>
}
#endif

using namespace std;

typedef vector<string>	SVector;
typedef vector<SVector>	DSVector;

#include "mxl.h"

/// 3. Constants
/// 3.1. Stream names
static string csCC	("Container.Contents");
static string csCP	("Container.Profile");
static string csDS	("Dialog Stream");
static string csMMS	("Main MetaData Stream");
static string csCmd	("Commands");
static string csGlr	("Gallery");
static string csGD	("GUIDData");
static string csMDPT	("MD Programm text");
static string csID	("Inplace description");
static string csTS	("TagStream");
static string csPg	("Page.");
static string csPic	("__Picture.");

/// 3.2. Storage names
static string csIF	("/UserDef/Page.1/Page.");
static string csPg1	("Page.1");
static string csPg2	("Page.2");
static string csRights	("/UserDef/Page.2");
static string csSUIT	("SubUsersInterfaceType");

/// 3.3. Dirs
static string dPathSep	("/");
static string dGlr	("Picture");	// 5523; was .; was Gallery
static string dMDPT	("Text");	// was MD_Programm_text
static string dID	("Text");	// 5523; was .; was Inplace_Description
static string dTS	("Picture");	// 5523; was .; was TagStream
static string dPic	("Picture");	// ????; pictures
static string dMXL	("MXL");	// ???? - unparsed MXLs
static string dBulk	("Bulk");	// 5617 - for MXL objects
static string dPnl	("Picture");	// 5523; was Panel
static string dDialog	("Dialog");	// 5C11 - Dialogs
static string dTable	("Table");	// 5C11 - Tables

static string fTSlogo	("Logo.bmp");
static string fTSsplash	("Splash.bmp");
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
#ifdef __BORLANDC__	// Windows
		POLE::Storage	*storage;			// CIF handler
#else
		MsOle	*ole;					// CIF handler
#endif
};

/// tree
class treebranch;
struct	treenode {
	bool	isfolder;
	union {
		string * file;
		treebranch * folder;
	} val;
};
class	treebranch {
	public:
		treebranch(void) {};
		~treebranch();
		string *	AddFile(const string &);
		treebranch *	AddFolder(void);
		int		GetSize(void);
		bool		IsFolder(DWORD);
		string *	GetFile(DWORD);
		treebranch *	GetFolder(DWORD);
		//treenode & GetNode(int);
	private:
		vector <treenode> val;
		bool		ChkIdx(DWORD, const char *);
};
void	printtree (const string &, treebranch *);

treebranch	* bq2tree(Pdata &);

/// 5. Func decls
void		Decode1C(Pdata &);
string		hex02(BYTE);
string		hex04(WORD);
string		hex08(DWORD);
const WORD	GetW(BYTE *);
const DWORD	GetDW(BYTE *);
string		i2s(int);
string		i2s(WORD);
string		i2s(DWORD);
string		out_uid(string);
string		out_uref(DWORD, char *pfx = "");
string		out_uref(string, char *pfx = "");
void		oTag (const char * s = NULL, bool close = false);
void		oTag (const string &, bool close = false);
void		eTag (void);
void		cTag (const char * s = NULL);
void		cTag (const string &);
DWORD		getsize (Pdata &);					// get Pascal-like string size
DWORD		getsize (BYTE *&);
string *	tune_str(string *);					// replace non-xml chars into entities
bool		recrmdir(const char *);
string		b2s(Pdata &);
void		do_dir (MDOLE &, string &);				// process storage recursively
void		do_stream (MDOLE &, SVector &, string &, string &);	// process stream
int		data_inflate(BYTE *, DWORD, BYTE *, DWORD *);		// inflat one buffer into another
int		unpack_data(Pdata &, Pdata &);
void		print_str(char *);
void		print_data(Pdata &);					// print text stream
//void		print_sized_data(Pdata &);				// print text stream checking forward len bytes
void		print_packed_data (Pdata &, string &, string &, bool);	// print or dump packed data
void		print_bq(Pdata &);					// print "bracketed-quoted" text
void		dump_data(Pdata &, string &, string &, int mode = O_CREAT|O_RDWR|O_TRUNC);	// write bulk data into file
void		dump_fpdata(Pdata &, string &, string &);		// write bulk data into file w/ "full path"
string		catdir (string &, string &);
//void		prnPstring(BYTE, string &);				///< out n chars
void		do_CC(Pdata &, const string &);				///< process Container.Contents stream
void		do_CP(Pdata &, const string &);				///< process Container.Profile stream
void		do_Dialog(Pdata &, const string &);			///< process Dialog stream
void		do_MMS(Pdata &, const string &);			///< process Main Metadata Stream stream
void		do_GD(Pdata &, const string &);				///< process GUIDData stream
void		do_TS(Pdata &, const string &);				///< process TagStream stream
void		do_Pic(Pdata &, string &, const string &);		///< process Picture
void		do_Glr(Pdata &, const string &);			///< process Gallery
void		do_Rights(Pdata &, const string &);			///< process Rights
void		do_Menu(Pdata &, const string &);			///< process Menu
void		do_Panel(Pdata &, string &, const string &);		///< process Panel
void		do_Commands (Pdata &, bool, const string &);		///< process Commands
DSVector	do_cc(string &);					///< process Container.Contents
SVector		FindCC(DSVector &, string &);
bool		mxl_try (char *);					///< try process mxl-file
void		do_Mxl (Pdata &, string &, const string &);
bool		MXL_Decode (Pdata &, MXL &);
void		MXL_Out (MXL &, string &, string &);

#endif	// _CATMD_H
