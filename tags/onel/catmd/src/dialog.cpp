// dialog.cpp
// parse Dialog stream

#include "catmd.h"

extern fstream ofile;	// std out file
extern string dRoot;
static DWORD DCounter = 0;	// dialog files counter

bool	do_Ctrl(treebranch *t, DWORD i, fstream &outfile) {
	DWORD	j, sz;
	int	zpt;
	string	name, key;

	sz = t->GetSize();
	if ((sz < 42) || (sz > 47)) {
		cerr << "Control: bad size: " << sz << endl;
		//printtree("", t);
		return false;
	}
	name = "c_" + *t->GetFile( 1);
	outfile << "<" << name <<
		" no=\"" << i << "\""
		" cap=\"" << *tune_str(t->GetFile( 0)) << "\""
		" u00=\"" << *t->GetFile( 2) << "\""
		" x=\""   << *t->GetFile( 3) << "\""
		" y=\""   << *t->GetFile( 4) << "\""
		" w=\""   << *t->GetFile( 5) << "\""
		" h=\""   << *t->GetFile( 6) << "\""
		" rq=\""  << *t->GetFile( 7) << "\""
		" u01=\"" << *t->GetFile( 8) << "\""
		" tn=\""  << *t->GetFile( 9) << "\""
		" u02=\"" << *t->GetFile(10) << "\""
		" fm=\""  << *tune_str(t->GetFile(11)) << "\""
		" id=\""  << *t->GetFile(12) << "\""
		" rid=\"" << *t->GetFile(13) << "\""
		" vtp=\"" << *t->GetFile(14) << "\""
		" vln=\"" << *t->GetFile(15) << "\""
		" vpr=\"" << *t->GetFile(16) << "\""
		<< out_uref( *t->GetFile(17)) <<
		" pt=\""  << *t->GetFile(18) << "\""
		" flg=\"" << *t->GetFile(19) << "\""
		" msq=\"" << *t->GetFile(20) << "\""
		" stp=\"" << *tune_str(t->GetFile(22)) << "\""
		" fs=\""  << *t->GetFile(23) << "\""
		" u03=\"" << *t->GetFile(24) << "\""
		" u04=\"" << *t->GetFile(25) << "\""
		" u05=\"" << *t->GetFile(26) << "\""
		" u06=\"" << *t->GetFile(27) << "\""
		" fb=\""  << *t->GetFile(28) << "\""
		" fi=\""  << *t->GetFile(29) << "\""
		" fu=\""  << *t->GetFile(30) << "\""
		" u07=\"" << *t->GetFile(31) << "\""
		" u08=\"" << *t->GetFile(32) << "\""
		" u09=\"" << *t->GetFile(33) << "\""
		" u10=\"" << *t->GetFile(34) << "\""
		" u11=\"" << *t->GetFile(35) << "\""
		" u12=\"" << *t->GetFile(36) << "\""
		" fn=\""  << *t->GetFile(37) << "\""
		" fc=\""  << *t->GetFile(38) << "\""
		" u13=\"" << *t->GetFile(39) << "\""
		" pid=\"" << *t->GetFile(40) << "\""
		" lr=\""  << *t->GetFile(41) << "\"";
	if (sz > 42) {
		for (j = 42; j < sz; j++)
			key += *t->GetFile(j);
		// short parsing {"#","#"}
		if ((zpt = key.find(',')) == -1)
			cerr << "Bad hotkey." << endl;
		else
			outfile <<
			" hkm=\"" << atol(key.substr(2, 3).c_str()) << "\""
			" hks=\"" << atol(key.substr(zpt + 2, 3).c_str()) << "\"";
		// end short parsing
	}
	if (t->GetFile(21)->size())
		outfile << ">" << *tune_str(t->GetFile(21)) << "</" << name << ">" << endl;
	else
		outfile << "/>" << endl;
	return true;
}

bool	do_Frame (treebranch *t, fstream &outfile) {
	string		name;
	treebranch	*p;
	DWORD		i, imax;

	if ((t->GetSize() != 2) || (!t->IsFolder(1))) {
		cerr << "Frame: bad structure." << endl;
		return false;
	}
	name = *t->GetFile(0);
	// 1. main
	t = t->GetFolder(1);
	imax = t->GetSize();
	if ((imax != 29) && (imax != 31)) {
		cerr << name << ": bad substructure size: " << imax << endl;
		return false;
	}
	outfile << "<" << name <<
		" fs=\""   << *t->GetFile( 0) << "\""
		" u00=\""  << *t->GetFile( 1) << "\""
		" u01=\""  << *t->GetFile( 2) << "\""
		" u02=\""  << *t->GetFile( 3) << "\""
		" fb=\""   << *t->GetFile( 4) << "\""
		" fi=\""   << *t->GetFile( 5) << "\""
		" fu=\""   << *t->GetFile( 6) << "\""
		" u03=\""  << *t->GetFile( 7) << "\""
		" u04=\""  << *t->GetFile( 8) << "\""
		" u05=\""  << *t->GetFile( 9) << "\""
		" u06=\""  << *t->GetFile(10) << "\""
		" u07=\""  << *t->GetFile(11) << "\""
		" u08=\""  << *t->GetFile(12) << "\""
		" fn=\""   << *t->GetFile(13) << "\""
		" w=\""    << *t->GetFile(14) << "\""
		" h=\""    << *t->GetFile(15) << "\""
		" cap=\""  << *tune_str(t->GetFile(16)) << "\""
		" u09=\""  << *t->GetFile(17) << "\""
		" u10=\""  << *t->GetFile(18) << "\""
		" sm=\""   << *t->GetFile(19) << "\""
		" u11=\""  << *t->GetFile(20) << "\""
		" fd=\""   << *t->GetFile(21) << "\""
		" at=\""   << *t->GetFile(22) << "\""
		" u12=\""  << *t->GetFile(23) << "\""
		" u13=\""  << *t->GetFile(24) << "\""
		" bc=\""   << *t->GetFile(25) << "\""
		" pic=\""  << *t->GetFile(26) << "\""
		" sm1=\""  << *t->GetFile(27) << "\""
		" al=\""   << *t->GetFolder(28)->GetFile(0) << "\"";
		if (imax > 29)
		outfile <<
			" stb=\""  << *t->GetFile(29) << "\""
			" szbl=\"" << *t->GetFile(30) << "\"";
		outfile << ">" << endl;
	// 2. layers
	t = t->GetFolder(28);
	imax = t->GetSize();
	for (i = 1; i < imax; i++) {
		p = t->GetFolder(i);
		if (p->GetSize() != 2)
			cerr << "Layer: size != 2." << endl;
		else
			outfile << "<lr no=\"" << i-1 << "\""
				" id=\"" << *p->GetFile(0) << "\""
				" v=\""  << *p->GetFile(1) << "\""
				"/>" << endl;
	}
	// 3. the end
	outfile << "</" << name << ">" << endl;
	return true;
}

bool	do_Controls (treebranch *t, fstream &outfile) {
	string		name;
	//treebranch	*p, *q;
	DWORD		i, imax;

	if (t->GetSize() < 1) {
		cerr << "Controls: bad structure" << endl;
		return false;
	}
	name = *t->GetFile(0);
	outfile << "<" << name << ">" << endl;
	imax = t->GetSize();
	for (i = 1; i < imax; i++)
		do_Ctrl(t->GetFolder(i), i-1, outfile);
	outfile << "</" << name << ">" << endl;
	return true;
}

bool	do_Browser (treebranch *t, fstream &outfile) {
	string		name, f_name;
	treebranch	*p, *q;
	DWORD		i, imax, sz;

	sz = t->GetSize();
	if ((sz != 2) && (sz != 5)) {
		cerr << "Browser: bad size: " << t->GetSize() << endl;
		return false;
	}
	if (sz == 2) {
		if(!(
			(t->GetFolder(0)->GetSize() == 1) &&
			(t->GetFolder(0)->GetFolder(0)->GetSize() == 0) &&
			(t->GetFolder(1)->GetSize() == 0)
		)) {
			cerr << "Browser: empty is not empty:" << endl;
			cerr << "**** Browser ****" << endl; printtree("", t);
			return false;
		} else
			return true;
	}
	// 1. root
	name = *t->GetFile(0);
	outfile << "<" << name <<
		" u0=\"" << *t->GetFile(1) << "\""
		" u1=\"" << *t->GetFile(2) << "\""
		">" << endl;	// root
	// 2. Multicolumn
	p = t->GetFolder(3);
	imax = p->GetSize();
	if ((imax != 2) || (*p->GetFile(0) != "Multicolumn"))	{
		cerr << "Multicolumn: bad size or name." << endl;
		return false;
	}
	outfile << "<mcols>" << endl;
	for (i = 1; i < imax; i++)
		do_Ctrl(p->GetFolder(i), i-1, outfile);
	outfile << "</mcols>" << endl;
	// 3. Fixed
	p = t->GetFolder(4);
	imax = p->GetSize();
	if ((imax < 1) || (*p->GetFile(0) != "Fixed"))	{
		cerr << "Fixed: bad size or name." << endl;
		return false;
	}
	outfile << "<fcols>" << endl;
	for (i = 1; i < imax; i++) {
		q = p->GetFolder(i);
		sz = q->GetSize();
		if ((sz < 21) || (sz > 22))
			cerr << "fcols: bad size: "<< sz << endl;
		else {
			f_name = "f_" + *q->GetFile( 3);
			outfile << "<" << f_name <<
				" no=\"" << i-1 << "\""
				" typ=\"" << *q->GetFile( 0) << "\""
				" cap=\"" << *q->GetFile( 1) << "\""
				" w=\""   << *q->GetFile( 2) << "\""
				" tn=\""  << *q->GetFile( 4) << "\""
				" u0=\""  << *q->GetFile( 5) << "\""
				" fm=\""  << *tune_str(q->GetFile( 6)) << "\""
				" id=\""  << *q->GetFile( 7) << "\""
				" rid=\"" << *q->GetFile( 8) << "\""
				" vtp=\"" << *q->GetFile( 9) << "\""
				" vln=\"" << *q->GetFile(10) << "\""
				" vpr=\"" << *q->GetFile(11) << "\""
				<< out_uref( *q->GetFile(12)) <<
				" pt=\""  << *q->GetFile(13) << "\""
				" u1=\""  << *q->GetFile(14) << "\""
				" u2=\""  << *q->GetFile(15) << "\""
				" aln=\"" << *q->GetFile(16) << "\""
				" flg=\"" << *q->GetFile(17) << "\""
				" msq=\"" << *q->GetFile(18) << "\""
				" stp=\"" << *tune_str(q->GetFile(20)) << "\"";
				if (sz > 21)
					outfile << " u3=\""  << *q->GetFile(21) << "\"";
			if (q->GetFile(19)->size())
				outfile << ">" << *q->GetFile(19) << "</" << f_name << ">" << endl;
			else
				outfile << "/>" << endl;
		}
	}
	outfile << "</fcols>" << endl;
	// 4. the end
	outfile << "</" << name << ">" << endl;
	return true;
}

bool	do_Ver (treebranch *t, fstream &outfile) {
	if (t->GetSize() != 2) {
		cerr << "Cnt_Ver: bad size." << endl;
		return false;
	}
	outfile << "<" << *t->GetFile(0) << " v=\"" << *t->GetFile(1) << "\"/>"<< endl;
	return (true);
}

bool	do_Dummy (treebranch *t, fstream &outfile) {
	if (
		(t->GetSize() == 2) &&
		(t->IsFolder(0)) &&
		(t->GetFolder(0)->GetSize() == 1) &&
		(t->GetFolder(0)->IsFolder(0)) &&
		(t->GetFolder(0)->GetFolder(0)->GetSize() == 0) &&
		(t->IsFolder(1)) &&
		(t->GetFolder(1)->GetSize() == 0)
	)
		outfile << "<DiaDummy/>" << endl;
	else
		cerr << "XE3" << endl;
	return true;
}

void	do_Dialog (Pdata & buffer, const string & ccstr) {
	treebranch *t;
	DWORD	i, sz;
	string	curr, sfile;
	fstream outfile;

	t = bq2tree(buffer)->GetFolder(0);
	sz = t->GetSize();
	if (*t->GetFile(0) != "Dialogs") {
		cerr << "Bad dialog stream name." << endl;
		return;
	}
	// 5C11: prepare out file for dialog
	sfile = hex08(DCounter++) + ".xml";
	sfile = catdir(dDialog, sfile);
	ofile << "<ds" << ccstr << " file=\"" << sfile << "\"/>" << endl;
	sfile = dRoot + sfile;
	outfile.open(sfile.c_str(), ios::binary | ios::out);
	outfile << "<?xml version = '1.0' encoding = 'windows-1251'?>" << endl
	<< "<!DOCTYPE dml SYSTEM \"dml.dtd\">" << endl
	<< "<dml>" << endl;
	// end prepare
	for (i = 1; i < sz; i++) {
		if (t->GetFolder(i)->IsFolder(0))
			do_Dummy(t->GetFolder(i), outfile);
		else {
			curr = *t->GetFolder(i)->GetFile(0);
			if (curr == "Frame")
				do_Frame	(t->GetFolder(i), outfile);
			else if (curr == "Browser")
				do_Browser	(t->GetFolder(i), outfile);
			else if (curr == "Controls")
				do_Controls	(t->GetFolder(i), outfile);
			else if (curr == "Cnt_Ver")
				do_Ver		(t->GetFolder(i), outfile);
			else
				cerr << "Bad dialog part: " << curr;
		}
	}
	outfile << "</dml>";
	outfile.close();
}
//cout << "<?xml version = '1.0' encoding = 'windows-1251'?>" << endl << "<!DOCTYPE mms SYSTEM \"catmd.dtd\">" << endl;
//cout << "</" << dname << ">" << endl;
