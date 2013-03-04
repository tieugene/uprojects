#include "catmd.h"

extern fstream ofile;

static bool subflag = false;

void	do_storage (MDOLE &, SVector &, string &, string &);

void do_dir (MDOLE & ole, string & dir)
{
	// process storage
	// @param ole - OLE storage handler
	// @param dir - corrent processed storage (starting - "/")
	SVector name, thiscc;
	DWORD     i;
	string  tmp;
	DSVector cc;
	Pdata   Pcc;

	// iLevel++;
	if (!ole.ls (name, dir))
		cerr << "Failed ls dir " << dir << endl;
	else {
		if (name.empty ())
			cerr << "Empty directory " << dir << endl;
		// load C.C
		if (ole.LoadStream (Pcc, dir, csCC))
			cerr << "Can't load Container.Contents @ " << dir << endl;
		else {		// C.C loaded
			tmp = b2s (Pcc);
			cc = do_cc (tmp);	// convert into DSvector
			// cont (w/o C.C)
			for (i = 0; i < name.size (); i++) {
				thiscc = FindCC (cc, name[i]);
				if (ole.IsStream (dir, name[i]))	// stream
					do_stream (ole, thiscc, dir, name[i]);
				else					// storage
					do_storage(ole, thiscc, dir, name[i]);
			}
		}
	}
	// iLevel--;
}

void do_stream (MDOLE & ole, SVector & cc, string & dir, string & name)
{
	static	long MDPTcounter = 0l;
	Pdata   buffer;
	string  stmp, ccstr;
	DWORD   dwtmp;

	if (ole.LoadStream (buffer, dir, name))
		cerr << "Can't load buffer from " << dir << name << endl;
	else {
		// prepare common string: name, CCx, size
		ccstr = " nm=\"" + name + "\"";
		if (cc.size () == 4)
			ccstr = ccstr + " c0=\"" + cc[0] + "\" c2=\"" + cc[2] + "\" c3=\"" + cc[3] + "\"";
		ccstr = ccstr + " sz=\"" + i2s(buffer.size) + "\"";
		// lets go
		if (name == csCC) {		// Container.Contents: t, nonpacked, nonsized
			do_CC(buffer, ccstr);
		} else if (name == csCP) {	// Container.Profile: t, nonpacked, nonsized
			do_CP(buffer, ccstr);
		} else if (name == csDS) {	// Dialog Stream: t, nonpacked, sized
			dwtmp = getsize (buffer);
			if (dwtmp != buffer.size)
				cerr << "Bad size in Dialog Stream @ " << dir << endl;
			else
				//print_bq (buffer);
				do_Dialog(buffer, ccstr);
		} else if (name == csMMS) {	// Main Metadata Stream: t, nonpacked, sized
			BYTE *tmpptr = buffer.data;	// tmp store of buffer begin
			// 1st weather it's normal stream
			dwtmp = getsize (buffer);
			if (dwtmp != buffer.size) {
				buffer.data = tmpptr;	// restore size
				Decode1C(buffer);
				// try 2
				dwtmp = getsize (buffer) - 1;
				if (dwtmp != buffer.size) {
					stmp = "MMS";
					cerr << "W: bad size in MMS @ " << dir << ": real size = " << buffer.size << ", declared size = " << dwtmp << "; dumped as " << dBulk << dPathSep << stmp << endl;
					dump_data(buffer, dBulk, stmp);
				} else {
					cerr << "I: MMS was encoded. Decoded OK." << endl;
					do_MMS(buffer, ccstr);
				}
			} else	// not coded stream
				do_MMS(buffer, ccstr);
		} else if (name == csCmd) {	// Commands: bin, nonpacked
			do_Commands (buffer, subflag, ccstr);
		} else if (name == csGlr) {	// Gallery: bin, nonpacked
			do_Glr (buffer, ccstr);
		} else if (name == csGD) {	// GUIDData: bin, nonpacked
			do_GD (buffer, ccstr);
		} else if (name == csMDPT) {	// MD Programm Text: t, packed, nonsized
			//stmp = catdir (dir, name);
			//print_packed_data (buffer, dMDPT, stmp, false);
			if (buffer.size != 2) {
				stmp = hex08(MDPTcounter++);
				ofile << "<mdpt" << ccstr << " file=\"" << dMDPT + dPathSep + stmp << "\"/>" << endl;
				print_packed_data (buffer, dMDPT, stmp, true);		// 0.3.0
			}
		} else if (name == csID) {	// Inplace description: t, packed, nonsized
			ofile << "<idesc" << ccstr << ">" << endl;
			stmp = catdir (dir, name);
			print_packed_data (buffer, dID, stmp, false);
			cTag("idesc");
		} else if (name == csTS) {	// TagStream: bin, nonsized | decode | bq sized, nonpacked
			do_TS (buffer, ccstr);
		} else if (name.find (csPg) == 0) {		// MXL|Rights|Menu|Panel: bin, nonpacked, ?
			if (strncmp (dir.c_str (), csIF.c_str (), csIF.length ()) == 0) {	// Interface
				if (name == csPg1)		// Menu > XML
					do_Menu (buffer, ccstr);
				else				// Panel > XML+file
					do_Panel (buffer, dir, ccstr);
			} else if (dir == csRights) {
				if (cc.size() == 4)
					do_Rights (buffer, ccstr);	// Rights > XML
				else	{
					stmp = dir + dPathSep + name;
					cerr << "W: unknown block in Rights storage. Dumped as " << dBulk << dPathSep << stmp << endl;
					dump_fpdata(buffer, dBulk, stmp);
				}
			} else {
				stmp = catdir (dir, name);
				do_Mxl (buffer, stmp, ccstr);	// Moxcel > XML + files
			}
		} else if (name.find (csPic) == 0) {	// Picture: bin, packed, sized ?
			do_Pic (buffer, name, ccstr);
		} else {
			cerr << catdir (dir, name) << ": Unknown stream" << endl;
		}
		//ofile << "</f>" << endl;
	}
	return;
}

void	do_storage (MDOLE & ole, SVector & cc, string & dir, string & name)	{
	int	i;
	bool	set_subflag = false;
	string	addon = " nm=\"" + name + "\"", tmp = catdir (dir, name), no;

	if (cc.size () == 4)
		addon = addon + " c0=\"" + cc[0] + "\" c2=\"" + cc[2] + "\" c3=\"" + cc[3] + "\"";
	if (						// add 's' and dump
		(name == "GlobalData") ||
		(name == "AccountChart") ||
		(name == "AccountChartList") ||
		(name == "CalcJournal") ||
		(name == "CalcVar") ||
		(name == "Document") ||
		(name == "Journal") ||
		(name == "Operation") ||
		(name == "OperationList") ||
		(name == "ProvList") ||
		(name == "Report") ||
		(name == "SubFolder") ||
		(name == "SubList") ||
		(name == "Subconto")
		)
			name += "s";
	else if (name.substr(0, 5) == "Page.")	{	// Page.*
		if (cc[0] == "UsersInterfaceType")
			addon = addon + " no=\"" + name.substr(5, name.size() - 5) + "\"";
		else if (cc[0] == "SubUsersInterfaceType")	{
			addon = addon + " no=\"" + name.substr(5, name.size() - 5) + "\"";
			set_subflag = true;
		}
		// else - "WorkPlaceType", "RigthType"
		name = cc[0];
	} else if ((i = name.find("_Number", 0)) > 0) {
		no = name.substr(i + 7, name.size() - i - 7);	// number
		name.erase(i, name.size() - i);			// clean name from '_NumberXXX'
		if (name == "ProvList")
			addon += out_uid(no);
		else
		//	--- was uid: addon += out_uid(no); ---
		//	"AccountChartList") ||
		//	"CalcJournal") ||
		//	"CalcVar") ||
		//	"Journal") ||
		//	"OperationList") ||
		//	"SubList")
		//	--- was uref: addon += out_uref(no); ---
		//	TypedText/CalcAlg
		//	TypedText/ModuleText
		//	TypedText/Transact
		//	TypedText/UserHelp
		//	AccountChart
		//	Document
		//	GlobalData
		//	Operation
		//	Report
		//	Subcontos
		//	SubFolder
			addon += out_uref(no);
	}
	//	"Metadata", "UserDef", "TypedText", "Picture", "WorkBook" - simply dump
	ofile << "<" << name << addon << ">" << endl;
	if (set_subflag) {
		subflag = true;
		do_dir (ole, tmp);
		subflag = false;
	} else
		do_dir (ole, tmp);
	cTag(name);
}
