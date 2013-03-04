// mms.cpp
// parse Main Metadata Stream

#include "catmd.h"

extern fstream ofile;

// local tmp vars
string		name;
treebranch	*p, *q, *r;
DWORD		i, imax, j, jmax;

bool	out_refers(treebranch *p, char * s = "refer") {
	DWORD	m, mmax;
	treebranch *x;

	mmax = p->GetSize();
	if ((mmax < 1) || (*p->GetFile(0) != "Refers")) {
		cerr << "Refers: zero size or wrong name." << endl;
		return false;
	}
	for (m = 1; m < mmax; m++) {
		x = p->GetFolder(m);
		if (x->GetSize() != 1)
			cerr << "Refer: size > 1." << endl;
		else
			ofile << "<" << s << " no=\"" << m-1 << "\"" << out_uref(*x->GetFile(0)) << "/>" << endl;
	}
	return true;
}

string	out_druler(treebranch *p) {
	string	retvalue;

	if (p->GetSize() != 4)
		cerr << "E: bad druler size: " << p->GetSize() << endl;
	else {
		if (*p->GetFile(0) != "Distribution ruler")
			cerr << "E: this is not Druler: " << *p->GetFile(0) << endl;
		else
			retvalue = "<druler"
				" u1=\"" + *p->GetFile(1) + "\""
				" u2=\"" + *p->GetFile(2) + "\""
				" u3=\"" + *p->GetFile(3) + "\""
			"/>";
	}
	return (retvalue);
}

bool	do_MainDataContDef (treebranch *t) {
	ofile << "<" << *t->GetFile(0);
	imax = t->GetSize();
	for (i = 1; i < imax; i++)
		ofile << " u" << i-1 << "=\"" << *t->GetFile(i) << "\"";
	ofile << "/>" << endl;
	return true;
}
bool	do_TaskItem (treebranch *t) {
	if ((t->GetSize() != 2) || (!t->IsFolder(1))) {
		cerr << "TaskItem: bad structure" << endl;
		return false;
	}
	name = *t->GetFile(0);
	t = t->GetFolder(1);
	if (t->GetSize() != 10)
		cerr << "TaskItem: bad structure size." << endl;
	else
		ofile << "<" << name
			<< out_uid(*t->GetFile(0)) <<
			" id=\""   << *tune_str(t->GetFile( 1)) << "\""
			" com=\""  << *tune_str(t->GetFile( 2)) << "\""
			" syn=\""  << *tune_str(t->GetFile( 3)) << "\""
			" u0=\""   << *t->GetFile( 4) << "\""
			" lng=\""  << *t->GetFile( 5) << "\""
			" u1=\""   << *t->GetFile( 6) << "\""
			" ddel=\"" << *t->GetFile( 7) << "\""
			" rnd=\""  << *t->GetFile( 8) << "\""
			" u2=\""   << *t->GetFile( 9) << "\"/>" << endl;
	return true;
}
bool	do_GenJrnlFldDef (treebranch *t) {	// optimize: none if empty
	if (!(t->GetSize())) {
		cerr << "GenJrnlFldDef: bad structure" << endl;
		return false;
	}
	name = *t->GetFile(0);
	ofile << "<" << name << ">" << endl;
	imax = t->GetSize();
	for (i = 1; i < imax; i++) {
		p = t->GetFolder(i);
		if (p->GetSize() != 11)
			cerr << "gjfd: bad structure" << endl;
		else
			ofile << "<gjfd no=\"" << i-1 << "\""
				<< out_uid(*p->GetFile( 0)) <<
				" id=\""   << *p->GetFile( 1) << "\""
				" com=\""  << *tune_str(p->GetFile( 2)) << "\""
				" syn=\""  << *tune_str(p->GetFile( 3)) << "\""
				" typ=\""  << *p->GetFile( 4) << "\""
				" len=\""  << *p->GetFile( 5) << "\""
				" prc=\""  << *p->GetFile( 6) << "\""
				<< out_uref(*p->GetFile( 7)) <<
				" tri=\""  << *p->GetFile( 8) << "\""
				" pos=\""  << *p->GetFile( 9) << "\""
				" sel=\""  << *p->GetFile(10) << "\"/>" << endl;
	}
	ofile << "</" << name << ">" << endl;
	return true;
}

bool	do_DocSelRefObj (treebranch *t) {
	if (!(t->GetSize())) {
		cerr << "DocSelRefObj: bad structure" << endl;
		return false;
	}
	// 1. root
	name = *t->GetFile(0);
	ofile << "<" << name << ">" << endl;	// root
	// 2. each dsro
	imax = t->GetSize();
	for (i = 1; i < imax; i++) {		// each dsro
		p = t->GetFolder(i);
		if (p->GetSize() != 8) {
			cerr << "dsro: bad structure" << endl;
			continue;
		}
		// 3. const fields
		ofile << "<dsro no=\"" << i << "\""
			<< out_uid(*p->GetFile(0)) <<
			" id=\""   << *p->GetFile(1) << "\""
			" com=\""  << *tune_str(p->GetFile(2)) << "\""
			" syn=\""  << *tune_str(p->GetFile(3)) << "\""
			" semp=\"" << *p->GetFile(4) << "\""
			" typ=\""  << *p->GetFile(5) << "\""
			<< out_uref(*p->GetFile( 6)) << ">" << endl;
		// 4. goto Refs subfolder
 		out_refers(p->GetFolder(7));
		ofile << "</dsro>" << endl;
	}
	ofile << "</" << name << ">" << endl;
	return true;
}
bool	do_DocNumDef (treebranch *t) {
	if (!(t->GetSize())) {
		cerr << "DocBumDef: bad structure" << endl;
		return false;
	}
	name = *t->GetFile(0);
	ofile << "<" << name << ">" << endl;
	imax = t->GetSize();
	for (i = 1; i < imax; i++) {
		p = t->GetFolder(i);
		if (p->GetSize() != 9)
			cerr << "dnd: bad structure" << endl;
		else
			ofile << "<dnd no=\"" << i-1 << "\""
			<< out_uid(*p->GetFile(0)) <<
			" id=\""   << *p->GetFile( 1) << "\""
			" com=\""  << *tune_str(p->GetFile( 2)) << "\""
			" syn=\""  << *tune_str(p->GetFile( 3)) << "\""
			" len=\""  << *p->GetFile( 4) << "\""
			" per=\""  << *p->GetFile( 5) << "\""
			" ctyp=\"" << *p->GetFile( 6) << "\""
			" u0=\""   << *p->GetFile( 7) << "\""
			" uniq=\"" << *p->GetFile( 8) << "\"/>" << endl;
	}
	ofile << "</" << name << ">" << endl;
	return true;
}
bool	do_Consts (treebranch *t) {
	if (!(t->GetSize())) {
		cerr << "Consts: bad structure" << endl;
		return false;
	}
	name = *t->GetFile(0);
	ofile << "<" << name << ">" << endl;
	imax = t->GetSize();
	for (i = 1; i < imax; i++) {
		p = t->GetFolder(i);
		jmax = p->GetSize();
		if ((jmax < 11) || (jmax > 12)) {
			cerr << "const: bad structure size: " << jmax << endl;
			continue;
		} else {
			ofile << "<const no=\"" << i-1 << "\""
				<< out_uid(*p->GetFile(0)) <<
				" id=\""   << *p->GetFile( 1) << "\""
				" com=\""  << *tune_str(p->GetFile( 2)) << "\""
				" syn=\""  << *tune_str(p->GetFile( 3)) << "\""
				" typ=\""  << *p->GetFile( 4) << "\""
				" len=\""  << *p->GetFile( 5) << "\""
				" prc=\""  << *p->GetFile( 6) << "\""
				<< out_uref(*p->GetFile( 7)) <<
				" pos=\""  << *p->GetFile( 8) << "\""
				" tri=\""  << *p->GetFile( 9) << "\""
				" per=\""  << *p->GetFile(10) << "\"";
			if (jmax == 12)	// Distribution
				ofile << ">" << endl << out_druler(p->GetFolder(11)) << endl << "</const>" << endl;
			else
				ofile << "/>" << endl;
		}
	}
	ofile << "</" << name << ">" << endl;
	return true;
}
bool	do_SbCnts (treebranch *t) {
	DWORD	size;
	if (!(t->GetSize())) {
		cerr << "SbCnts: bad structure" << endl;
		return false;
	}
	// 1. root
	name = *t->GetFile(0);
	ofile << "<" << name << ">" << endl;	// root
	// 2. each sbcnt
	imax = t->GetSize();
	for (i = 1; i < imax; i++) {		// each dsro
		p = t->GetFolder(i);
		size = p->GetSize();
		if ((size < 20) || (size > 21)) {
			cerr << "const: bad structure size: " << size << endl;
			continue;
		}
		// 3. sbcnt fields
		ofile << "<sbcnt no=\"" << i-1 << "\""
			<< out_uid(*p->GetFile(0)) <<
			" id=\""   << *p->GetFile( 1) << "\""
			" com=\""  << *tune_str(p->GetFile( 2)) << "\""
			" syn=\""  << *tune_str(p->GetFile( 3)) << "\""
			<< out_uref(*p->GetFile( 4), "p") <<
			" clen=\"" << *p->GetFile( 5) << "\""
			" cser=\"" << *p->GetFile( 6) << "\""
			" ctyp=\"" << *p->GetFile( 7) << "\""
			" anum=\"" << *p->GetFile( 8) << "\""
			" nlen=\"" << *p->GetFile( 9) << "\""
			" mpre=\"" << *p->GetFile(10) << "\""
			" toed=\"" << *p->GetFile(11) << "\""
			" lvls=\"" << *p->GetFile(12) << "\""
			<< out_uref(*p->GetFile(13), "fs")
			<< out_uref(*p->GetFile(14), "fm") <<
			" uf=\""   << *p->GetFile(15) << "\""
			" uniq=\"" << *p->GetFile(16) << "\""
			" gup=\""  << *p->GetFile(17) << "\">" << endl;
		// 4. goto params subfolder
 		q = p->GetFolder(18);
		jmax = q->GetSize();
		if ((jmax < 1) || (*q->GetFile(0) != "Params")) {
			cerr << "Params: bad structure" << endl;
			continue;
		}
		// 5. each param
		for (j = 1; j < jmax; j++) {
			// 6. check ref size
			r = q->GetFolder(j);
			if (r->GetSize() != 17)
				cerr << "Param: bad structure size" << endl;
			else
				ofile << "<param no=\"" << j-1 << "\""
				<< out_uid(*r->GetFile(0)) <<
				" id=\""   << *r->GetFile( 1) << "\""
				" com=\""  << *tune_str(r->GetFile( 2)) << "\""
				" syn=\""  << *tune_str(r->GetFile( 3)) << "\""
				" typ=\""  << *r->GetFile( 4) << "\""
				" len=\""  << *r->GetFile( 5) << "\""
				" prc=\""  << *r->GetFile( 6) << "\""
				<< out_uref(*r->GetFile( 7)) <<
				" pos=\""  << *r->GetFile( 8) << "\""
				" tri=\""  << *r->GetFile( 9) << "\""
				" per=\""  << *r->GetFile(10) << "\""
				" ufi=\""  << *r->GetFile(11) << "\""
				" ufg=\""  << *r->GetFile(12) << "\""
				" srt=\""  << *r->GetFile(13) << "\""
				" hchg=\"" << *r->GetFile(14) << "\""
				" dchg=\"" << *r->GetFile(15) << "\""
				" cbr=\""  << *r->GetFile(16) << "\"/>" << endl;
		}
		// 6. goto Form subfolder
 		q = p->GetFolder(19);
		if (((jmax = q->GetSize()) < 1) || (*q->GetFile(0) != "Form")) {
			cerr << "Form: bad structure" << endl;
			continue;
		}
		for (j = 1; j < jmax; j++) {
			// 6. check ref size
			r = q->GetFolder(j);
			if (r->GetSize() != 4)
				cerr << "Form: bad structure size" << endl;
			else
				ofile << "<form no=\"" << j-1 << "\""
				<< out_uid(*r->GetFile(0)) <<
				" id=\""   << *r->GetFile( 1) << "\""
				" com=\""  << *tune_str(r->GetFile( 2)) << "\""
				" syn=\""   << *r->GetFile( 3) << "\"/>" << endl;
		}
		if (size == 21) {
			q = p->GetFolder(20);
			jmax = q->GetSize();
			ofile << "<sbcnt_u";
			for (j = 0; j < jmax; j++)
				ofile << " v_" << j << "=\"" << *q->GetFile(j) << "\"";
			ofile << "/>" << endl;
		}
		ofile << "</sbcnt>" << endl;
	}
	ofile << "</" << name << ">" << endl;
	return true;
}
bool	do_Registers (treebranch *t) {
	if (!(t->GetSize())) {
		cerr << "Registers: bad structure" << endl;
		return false;
	}
	// 1. root
	name = *t->GetFile(0);
	ofile << "<" << name << ">" << endl;	// root
	// 2. each register
	imax = t->GetSize();
	for (i = 1; i < imax; i++) {		// each dsro
		p = t->GetFolder(i);
		if (p->GetSize() != 11) {
			cerr << "rgstr: bad structure" << endl;
			continue;
		}
		// 3. rgstr fields
		ofile << "<rgstr no=\"" << i-1 << "\""
			<< out_uid(*p->GetFile(0)) <<
			" id=\""   << *p->GetFile( 1) << "\""
			" com=\""  << *tune_str(p->GetFile( 2)) << "\""
			" syn=\""  << *tune_str(p->GetFile( 3)) << "\""
			" rtyp=\"" << *p->GetFile( 4) << "\""
			" rper=\"" << *p->GetFile( 5) << "\""
			" spid=\"" << *p->GetFile( 6) << "\""
			" u0=\""   << *p->GetFile( 7) << "\">" << endl;
		// 4. Props subfolder
 		q = p->GetFolder(8);
		jmax = q->GetSize();
		if ((jmax < 1) || (*q->GetFile(0) != "Props")) {
			cerr << "Props: bad structure" << endl;
			continue;
		}
		for (j = 1; j < jmax; j++) {
			r = q->GetFolder(j);
			if (r->GetSize() != 12)
				cerr << "Prop: bad structure size" << endl;
			else
				ofile << "<prop no=\"" << j-1 << "\""
					<< out_uid(*r->GetFile(0)) <<
					" id=\""   << *r->GetFile( 1) << "\""
					" com=\""  << *tune_str(r->GetFile( 2)) << "\""
					" syn=\""  << *tune_str(r->GetFile( 3)) << "\""
					" typ=\""  << *r->GetFile( 4) << "\""
					" len=\""  << *r->GetFile( 5) << "\""
					" prc=\""  << *r->GetFile( 6) << "\""
					<< out_uref(*r->GetFile( 7)) <<
					" u0=\""   << *r->GetFile( 8) << "\""
					" tri=\""  << *r->GetFile( 9) << "\""
					" smov=\""  << *r->GetFile(10) << "\""
					" ssum=\""  << *r->GetFile(11) << "\"/>" << endl;
		}
		// 5. Figures subfolder
 		q = p->GetFolder(9);
		if (((jmax = q->GetSize()) < 1) || (*q->GetFile(0) != "Figures")) {
			cerr << "Figures: bad structure" << endl;
			continue;
		}
		for (j = 1; j < jmax; j++) {
			r = q->GetFolder(j);
			if (r->GetSize() != 10)
				cerr << "Figure: bad structure size" << endl;
			else
				ofile << "<fig no=\"" << j-1 << "\""
					<< out_uid(*r->GetFile(0)) <<
					" id=\""   << *r->GetFile( 1) << "\""
					" com=\""  << *tune_str(r->GetFile( 2)) << "\""
					" syn=\""  << *tune_str(r->GetFile( 3)) << "\""
					" typ=\""  << *r->GetFile( 4) << "\""
					" len=\""  << *r->GetFile( 5) << "\""
					" prc=\""  << *r->GetFile( 6) << "\""
					" u0=\""   << *r->GetFile( 7) << "\""
					" u1=\""   << *r->GetFile( 8) << "\""
					" tri=\""  << *r->GetFile( 9) << "\"/>" << endl;
		}
		// Flds. Figures subfolder
 		q = p->GetFolder(10);
		if (((jmax = q->GetSize()) < 1) || (*q->GetFile(0) != "Flds")) {
			cerr << "Flds: bad structure" << endl;
			continue;
		}
		for (j = 1; j < jmax; j++) {
			r = q->GetFolder(j);
			if (r->GetSize() != 11)
				cerr << "Flds: bad structure size" << endl;
			else
				ofile << "<rfld no=\"" << j-1 << "\""
					<< out_uid(*r->GetFile(0)) <<
					" id=\""   << *r->GetFile( 1) << "\""
					" com=\""  << *tune_str(r->GetFile( 2)) << "\""
					" syn=\""  << *tune_str(r->GetFile( 3)) << "\""
					" typ=\""  << *r->GetFile( 4) << "\""
					" len=\""  << *r->GetFile( 5) << "\""
					" prc=\""  << *r->GetFile( 6) << "\""
					<< out_uref(*r->GetFile( 7)) <<
					" pos=\""  << *r->GetFile( 8) << "\""
					" tri=\""  << *r->GetFile( 9) << "\""
					" per=\""  << *r->GetFile(10) << "\"/>" << endl;
		}
		ofile << "</rgstr>" << endl;
	}
	ofile << "</" << name << ">" << endl;
	return true;
}
bool	do_Documents (treebranch *t) {
	if (!(t->GetSize())) {
		cerr << "Documents: bad structure" << endl;
		return false;
	}
	// 1. root
	name = "m" + *t->GetFile(0);	// 5605 - against storage
	ofile << "<" << name << ">" << endl;	// root
	// 2. each doc
	imax = t->GetSize();
	for (i = 1; i < imax; i++) {		// each dsro
		p = t->GetFolder(i);
		jmax = p->GetSize();
		if ((jmax < 24) || (jmax > 25)) {
			cerr << "doc: bad structure size: " << jmax << endl;
			printtree("", p);
			continue;
		}
		// 3. doc fields
		ofile << "<doc no=\"" << i-1 << "\""
			<< out_uid(*p->GetFile(0)) <<
			" id=\""   << *p->GetFile( 1) << "\""
			" com=\""  << *tune_str(p->GetFile( 2)) << "\""
			" syn=\""  << *tune_str(p->GetFile( 3)) << "\""
			" clen=\"" << *p->GetFile( 4) << "\""
			" per=\""  << *p->GetFile( 5) << "\""
			" ctyp=\"" << *p->GetFile( 6) << "\""
			" anum=\"" << *p->GetFile( 7) << "\""
			<< out_uref(*p->GetFile( 8), "j") <<
			" u0=\""   << *p->GetFile( 9) << "\""
			" uniq=\"" << *p->GetFile(10) << "\""
			<< out_uref(*p->GetFile(11), "n") <<
			" trad=\"" << *p->GetFile(12) << "\""
			" clc=\""  << *p->GetFile(13) << "\""
			" acc=\""  << *p->GetFile(14) << "\""
			" ffa=\""  << *p->GetFile(16) << "\""
			" crop=\"" << *p->GetFile(17) << "\""
			" aln=\""  << *p->GetFile(18) << "\""
			" amd=\""  << *p->GetFile(19) << "\""
			" u5=\""   << *p->GetFile(20) << "\""
			" eprv=\"" << *p->GetFile(21) << "\"";
		q = p->GetFolder(15);
		if (q->GetSize() != 5) {
			cerr << "Doc: bad refer folder" << endl;
			return false;
		}
		ofile <<
			" u1=\""  << *q->GetFile( 0) << "\""
			" u2=\""  << *q->GetFile( 1) << "\""
			" u3=\""  << *q->GetFile( 2) << "\""
			" u4=\""  << *q->GetFile( 3) << "\">" << endl;
		// 4. Refers subfolder
		out_refers(q->GetFolder(4));
		// 5. Head Fields
 		q = p->GetFolder(22);
		if (((jmax = q->GetSize()) < 1) || (*q->GetFile(0) != "Head Fields")) {
			cerr << "Head Fields: bad structure" << endl;
			continue;
		}
		for (j = 1; j < jmax; j++) {
			r = q->GetFolder(j);
			if (r->GetSize() != 10)
				cerr << "HeadField: bad structure size" << endl;
			else
				ofile << "<hfld no=\"" << j-1 << "\""
				<< out_uid(*r->GetFile(0)) <<
				" id=\""   << *r->GetFile( 1) << "\""
				" com=\""  << *tune_str(r->GetFile( 2)) << "\""
				" syn=\""  << *tune_str(r->GetFile( 3)) << "\""
				" typ=\""  << *r->GetFile( 4) << "\""
				" len=\""  << *r->GetFile( 5) << "\""
				" prc=\""  << *r->GetFile( 6) << "\""
				<< out_uref(*r->GetFile( 7)) <<
				" pos=\""  << *r->GetFile( 8) << "\""
				" tri=\""  << *r->GetFile( 9) << "\"/>" << endl;
		}
		// 6. Table Fields
 		q = p->GetFolder(23);
		if (((jmax = q->GetSize()) < 1) || (*q->GetFile(0) != "Table Fields")) {
			cerr << "Table Fields: bad structure" << endl;
			continue;
		}
		for (j = 1; j < jmax; j++) {
			r = q->GetFolder(j);
			if (r->GetSize() != 11)
				cerr << "Table Field: bad structure size" << endl;
			else
				ofile << "<tfld no=\"" << j-1 << "\""
				<< out_uid(*r->GetFile(0)) <<
				" id=\""   << *r->GetFile( 1) << "\""
				" com=\""  << *tune_str(r->GetFile( 2)) << "\""
				" syn=\""  << *tune_str(r->GetFile( 3)) << "\""
				" typ=\""  << *r->GetFile( 4) << "\""
				" len=\""  << *r->GetFile( 5) << "\""
				" prc=\""  << *r->GetFile( 6) << "\""
				<< out_uref(*r->GetFile( 7)) <<
				" pos=\""  << *r->GetFile( 8) << "\""
				" tri=\""  << *r->GetFile( 9) << "\""
				" csum=\"" << *r->GetFile(10) << "\"/>" << endl;
		}
		// 7. Distribution
		if (p->GetSize() > 24)
			ofile << out_druler(p->GetFolder(24)) << endl;
		ofile << "</doc>" << endl;
	}
	ofile << "</" << name << ">" << endl;
	return true;
}
bool	do_Journalisters (treebranch *t, const string & s) {
	string	jname;

	if (!(t->GetSize())) {
		cerr << s << ": zero size" << endl;
		return false;
	}
	// 1. root
	jname = *t->GetFile(0);
	ofile << "<" << jname << ">" << endl;	// root
	// 2. each journ
	imax = t->GetSize();
	for (i = 1; i < imax; i++) {		// each dsro
		p = t->GetFolder(i);
		if (p->GetSize() != 12) {
			cerr << "journ: bad size:" << p->GetSize() << endl;
			continue;
		}
		// 3. journ fields
		ofile << "<journ no=\"" << i-1 << "\""
			<< out_uid(*p->GetFile(0)) <<
			" id=\""   << *p->GetFile( 1) << "\""
			" com=\""  << *tune_str(p->GetFile( 2)) << "\""
			" syn=\""  << *tune_str(p->GetFile( 3)) << "\""
			" u0=\"" << *p->GetFile( 4) << "\""
			" jtyp=\""  << *p->GetFile( 5) << "\""
			<< out_uref(*p->GetFile( 6), "fs")
			<< out_uref(*p->GetFile( 7), "fm") <<
			" cmn=\"" << *p->GetFile( 8) << "\"";
		q = p->GetFolder(9);
		if (q->GetSize() != 5) {
			cerr << "journ: bad refer folder" << endl;
			ofile << "/>" << endl;
			continue;
		}
		ofile <<
			" u1=\""  << *q->GetFile( 0) << "\""
			" u2=\""  << *q->GetFile( 1) << "\""
			" u3=\""  << *q->GetFile( 2) << "\""
			" u4=\""  << *q->GetFile( 3) << "\">" << endl;
		// 4. Refers subfolder
		out_refers(q->GetFolder(4));
		// 5. JournalFld
 		q = p->GetFolder(10);
		if (((jmax = q->GetSize()) < 1) || (*q->GetFile(0) != "JournalFld")) {
			cerr << "JournalFld: zero size or bad name." << endl;
			continue;
		}
		for (j = 1; j < jmax; j++) {
			r = q->GetFolder(j);
			if (r->GetSize() != 5)
				cerr << "JournalFld: bad structure size" << endl;
			else {
				ofile << "<jfld no=\"" << j-1 << "\""
				<< out_uid(*r->GetFile(0)) <<
				" id=\""   << *r->GetFile( 1) << "\""
				" com=\""  << *tune_str(r->GetFile( 2)) << "\""
				" syn=\""  << *tune_str(r->GetFile( 3)) << "\">" << endl;
				out_refers(r->GetFolder(4));
				ofile << "</jfld>" << endl;
			}
		}
		// 6. Form
 		q = p->GetFolder(11);
		if (((jmax = q->GetSize()) < 1) || (*q->GetFile(0) != "Form")) {
			cerr << "Form: bad structure" << endl;
			continue;
		}
		for (j = 1; j < jmax; j++) {
			r = q->GetFolder(j);
			if (r->GetSize() != 4)
				cerr << "Form: bad structure size" << endl;
			else
				ofile << "<form no=\"" << j-1 << "\""
				<< out_uid(*r->GetFile(0)) <<
				" id=\""   << *r->GetFile( 1) << "\""
				" com=\""  << *tune_str(r->GetFile( 2)) << "\""
				" syn=\""  << *tune_str(r->GetFile( 3)) << "\"/>" << endl;
		}
		ofile << "</journ>" << endl;
	}
	ofile << "</" << jname << ">" << endl;
	return (true);
}
bool	do_EnumList (treebranch *t) {
	if (!(t->GetSize())) {
		cerr << "EnumList: bad structure" << endl;
		return false;
	}
	// 1. root
	name = *t->GetFile(0);
	ofile << "<" << name << ">" << endl;	// root
	// 2. each enumlist
	imax = t->GetSize();
	for (i = 1; i < imax; i++) {		// each dsro
		p = t->GetFolder(i);
		if (p->GetSize() != 5) {
			cerr << "enuml: bad structure size" << endl;
			continue;
		}
		// 3. rgstr fields
		ofile << "<enuml no=\"" << i-1 << "\""
			<< out_uid(*p->GetFile(0)) <<
			" id=\""   << *p->GetFile( 1) << "\""
			" com=\""  << *tune_str(p->GetFile( 2)) << "\""
			" syn=\""  << *tune_str(p->GetFile( 3)) << "\">" << endl;
		// 4. EnumValue
 		q = p->GetFolder(4);
		jmax = q->GetSize();
		if ((jmax < 1) || (*q->GetFile(0) != "EnumVal")) {
			cerr << "EnumVal: bad structure" << endl;
			continue;
		}
		for (j = 1; j < jmax; j++) {
			r = q->GetFolder(j);
			if (r->GetSize() != 5)
				cerr << "EnumVal: bad structure size" << endl;
			else
				ofile << "<enumv no=\"" << j-1 << "\""
					<< out_uid(*r->GetFile(0)) <<
					" id=\""   << *r->GetFile( 1) << "\""
					" com=\""  << *tune_str(r->GetFile( 2)) << "\""
					" syn=\""  << *tune_str(r->GetFile( 3)) << "\""
					" prs=\""  << *tune_str(r->GetFile( 4)) << "\"/>" << endl;
		}
		ofile << "</enuml>" << endl;
	}
	ofile << "</" << name << ">" << endl;
	return true;
}
bool	do_ReportList (treebranch *t) {
	if (!(t->GetSize())) {
		cerr << "ReportList: bad structure" << endl;
		return false;
	}
	name = *t->GetFile(0);
	ofile << "<" << name << ">" << endl;
	imax = t->GetSize();
	for (i = 1; i < imax; i++) {
		p = t->GetFolder(i);
		if (p->GetSize() != 4)
			cerr << "rprt: bad structure" << endl;
		else
			ofile << "<rprt no=\"" << i-1 << "\""
			<< out_uid(*p->GetFile(0)) <<
			" id=\""   << *p->GetFile( 1) << "\""
			" com=\""  << *tune_str(p->GetFile( 2)) << "\""
			" syn=\""  << *tune_str(p->GetFile( 3)) << "\"/>" << endl;
	}
	ofile << "</" << name << ">" << endl;
	return true;
}
bool	do_CJ (treebranch *t) {
	if (!(t->GetSize())) {
		cerr << "CJ: bad structure" << endl;
		return false;
	}
	name = *t->GetFile(0);
	ofile << "<" << name << ">" << endl;	// root
	// 2. each cjey
	imax = t->GetSize();
	for (i = 1; i < imax; i++) {		// each dsro
		p = t->GetFolder(i);
		if (p->GetSize() < 13) {
			cerr << "cjey: bad structure size: " << p->GetSize() << endl;
			continue;
		}
		// 3. cjey fields
		ofile << "<cjey no=\"" << i-1 << "\""
			<< out_uid(*p->GetFile(0)) <<
			" id=\""   << *p->GetFile( 1) << "\""
			" com=\""  << *tune_str(p->GetFile( 2)) << "\""
			" syn=\""  << *tune_str(p->GetFile( 3)) << "\""
			<< out_uref(*p->GetFile( 4)) <<
			" per=\""  << *p->GetFile( 5) << "\""
			" cdat=\"" << *p->GetFile( 6) << "\""
			" len=\""  << *p->GetFile( 8) << "\""
			" prc=\""  << *p->GetFile( 9) << "\""
			" tow=\""  << *p->GetFile(10) << "\""
			<< out_uref(*p->GetFile(13), "fs")
			<< out_uref(*p->GetFile(14), "fm") <<
			" u0=\""   << *p->GetFolder(11)->GetFile(0) << "\">" << endl;
		// 4. goto CJParms subfolder
 		q = p->GetFolder(7);
		jmax = q->GetSize();
		if ((jmax < 1) || (*q->GetFile(0) != "CJParams")) {
			cerr << "CJParms: bad structure: " << *q->GetFile(0) << endl;
			continue;
		}
		// 5. each parm
		for (j = 1; j < jmax; j++) {
			// 6. check parm size
			r = q->GetFolder(j);
			if (r->GetSize() != 10)
				cerr << "Param: bad structure size" << endl;
			else
				ofile << "<cjprm no=\"" << j-1 << "\""
				<< out_uid(*r->GetFile(0)) <<
				" id=\""   << *r->GetFile( 1) << "\""
				" com=\""  << *tune_str(r->GetFile( 2)) << "\""
				" syn=\""  << *tune_str(r->GetFile( 3)) << "\""
				" typ=\""  << *r->GetFile( 4) << "\""
				" len=\""  << *r->GetFile( 5) << "\""
				" prc=\""  << *r->GetFile( 6) << "\""
				<< out_uref(*r->GetFile( 7)) <<
				" pos=\""  << *r->GetFile( 8) << "\""
				" tri=\""  << *r->GetFile( 9) << "\"/>" << endl;
		}
		// 6. goto cjfld
		q = p->GetFolder(11);
		if ((jmax = q->GetSize()) < 1) {
			cerr << "cjfld: bad structure" << endl;
			continue;
		}
		for (j = 1; j < jmax; j++) {
			ofile << "<cjfld no=\"" << j-1 << "\""
				<< out_uref(*q->GetFile(j)) << "/>" << endl;
		}
		// 7. goto Form subfolder
 		q = p->GetFolder(12);
		if (((jmax = q->GetSize()) < 1) || (*q->GetFile(0) != "Form")) {
			cerr << "Form: bad structure" << endl;
			continue;
		}
		for (j = 1; j < jmax; j++) {
			// 6. check form size
			r = q->GetFolder(j);
			if (r->GetSize() != 4)
				cerr << "Form: bad structure size" << endl;
			else
				ofile << "<form no=\"" << j-1 << "\""
				<< out_uid(*r->GetFile(0)) <<
				" id=\""   << *r->GetFile( 1) << "\""
				" com=\""  << *tune_str(r->GetFile( 2)) << "\""
				" syn=\""   << *r->GetFile( 3) << "\"/>" << endl;
		}
		ofile << "</cjey>" << endl;
	}
	ofile << "</" << name << ">" << endl;
	return (true);
}
bool	do_Calendars (treebranch *t) {
	if (!(t->GetSize())) {
		cerr << "Calendars: bad structure" << endl;
		return false;
	}
	// 1. root
	name = *t->GetFile(0);
	ofile << "<" << name << ">" << endl;	// root
	// 2. each clndr
	imax = t->GetSize();
	for (i = 1; i < (imax-1); i++) {		// each dsro
		p = t->GetFolder(i);
		if (p->GetSize() != 6) {
			cerr << "clndr: bad structure size:" << p->GetSize() << endl;
			for (j = 0; j < p->GetSize(); j++) {
				if (p->IsFolder(j))
					cerr << "\t" << j << ":[" << p->GetFolder(j)->GetSize() << "]" << endl;
				else
					cerr << "\t" << j << ":" << *p->GetFile(j) << endl;
			}
			continue;
		}
		// 3. clndr fields
		ofile << "<clndr no=\"" << i-1 << "\""
			<< out_uid(*p->GetFile(0)) <<
			" id=\""   << *p->GetFile( 1) << "\""
			" com=\""  << *tune_str(p->GetFile( 2)) << "\""
			" syn=\""  << *tune_str(p->GetFile( 3)) << "\""
			" strt=\""  << *p->GetFile( 4) << "\">" << endl;
		// 4. days
 		q = p->GetFolder(5);
		jmax = q->GetSize();
		if ((jmax < 1) || (*q->GetFile(0) != "Days")) {
			cerr << "Days: zero len or bad name." << endl;
			continue;
		}
		for (j = 1; j < jmax; j++)
			ofile << "<day no=\"" << j-1 << "\""
				" v=\""  << *q->GetFile(j) << "\"/>" << endl;
		ofile << "</clndr>" << endl;
	}
	// 3. Holidays
	p = t->GetFolder(imax - 1);
	if ((p->GetSize() != 2) || (*p->GetFile(0) != "HolidaysDef"))
		cerr << "Can't get holidays." << endl;
	else {
		p = p->GetFolder(1);
		jmax = p->GetSize();
		if ((jmax < 4) && (jmax > 5)) {
			cerr << "Bad holidays subfolder size: " << jmax << endl;
			printtree("", p);
		}
		else
			ofile << "<holi"
				" v0=\""  << *p->GetFile( 0) << "\""
				" v1=\""   << *p->GetFile( 1) << "\""
				" v2=\""  << *tune_str(p->GetFile( 2)) << "\""
				" v3=\""  << *tune_str(p->GetFile( 3)) << "\"";
			if (jmax == 5)	// Distribution
				ofile << ">" << endl << out_druler(p->GetFolder(4)) << endl << "</holi>" << endl;
			else
				ofile << "/>" << endl;
	}
	ofile << "</" << name << ">" << endl;
	return (true);
}
bool	do_Algorithms (treebranch *t) {
	if (!(t->GetSize())) {
		cerr << "Algorithms: bad structure" << endl;
		return false;
	}
	name = *t->GetFile(0);
	ofile << "<" << name << ">" << endl;	// root
	// 2. each algo
	imax = t->GetSize();
	for (i = 1; i < imax; i++) {		// each dsro
		p = t->GetFolder(i);
		if (p->GetSize() != 9) {
			cerr << "algo: bad size:" << p->GetSize() << endl;
			continue;
		}
		// 3. algo fields
		ofile << "<algo no=\"" << i-1 << "\""
			<< out_uid(*p->GetFile(0)) <<
			" id=\""   << *p->GetFile( 1) << "\""
			" com=\""  << *tune_str(p->GetFile( 2)) << "\""
			" syn=\""  << *tune_str(p->GetFile( 3)) << "\""
			" pri=\""  << *p->GetFile( 4) << "\""
			" u0=\""  << *p->GetFile( 5) << "\""
			" u1=\""  << *p->GetFile( 6) << "\"";
		// 4. 1st subfileds
		q = p->GetFolder(7);
		if (q->GetSize() != 5) {
			cerr << "algo: bad refer folder" << endl;
			ofile << "/>" << endl;
			continue;
		}
		ofile <<
			" u2=\""  << *q->GetFile( 0) << "\""
			" u3=\""  << *q->GetFile( 1) << "\""
			" u4=\""  << *q->GetFile( 2) << "\""
			" u5=\""  << *q->GetFile( 3) << "\">" << endl;
		// 5. Refers subfolders
		out_refers(p->GetFolder(7)->GetFolder(4));
		// 6. Algs
 		q = p->GetFolder(8);
		jmax = q->GetSize();
		if ((jmax < 1) || (*q->GetFile(0) != "InGroups")) {
			cerr << "InGroups: zero len or bad nameb." << endl;
			continue;
		}
		for (j = 1; j < jmax; j++)
			ofile << "<ingrp no=\"" << j-1 << "\""
				<< out_uref(*q->GetFile(j)) << "/>" << endl;
		// 7. the end
		ofile << "</algo>" << endl;
	}
	ofile << "</" << name << ">" << endl;
	return (true);
}
bool	do_RecalcRules (treebranch *t) {
	if (!(t->GetSize())) {
		cerr << "RecalcRules: zero size" << endl;
		return false;
	}
	// 1. root
	name = *t->GetFile(0);
	ofile << "<" << name << ">" << endl;	// root
	// 2. each rrul
	imax = t->GetSize();
	for (i = 1; i < imax; i++) {		// each dsro
		p = t->GetFolder(i);
		if (p->GetSize() != 8) {
			cerr << "rrul: bad size:" << p->GetSize() << endl;
			continue;
		}
		// 3. rrul fields
		ofile << "<rrul no=\"" << i-1 << "\""
			<< out_uid(*p->GetFile(0)) <<
			" id=\""   << *p->GetFile( 1) << "\""
			" com=\""  << *tune_str(p->GetFile( 2)) << "\""
			" syn=\""  << *tune_str(p->GetFile( 3)) << "\""
			" rtyp=\"" << *p->GetFile( 4) << "\""
			" inp=\""  << *p->GetFile( 5) << "\"";
		// 4. 1st subfileds
		q = p->GetFolder(6);
		if (q->GetSize() != 5) {
			cerr << "Doc: bad refer folder" << endl;
			ofile << "/>" << endl;
			continue;
		}
		ofile <<
			" u0=\""  << *q->GetFile( 0) << "\""
			" u1=\""  << *q->GetFile( 1) << "\""
			" u2=\""  << *q->GetFile( 2) << "\""
			" u3=\""  << *q->GetFile( 3) << "\"";
		// 5. 2nd subfileds
		q = p->GetFolder(7);
		if (q->GetSize() != 5) {
			cerr << "Doc: bad refer1 folder" << endl;
			ofile << "/>" << endl;
			continue;
		}
		ofile <<
			" u4=\""  << *q->GetFile( 0) << "\""
			" u5=\""  << *q->GetFile( 1) << "\""
			" u6=\""  << *q->GetFile( 2) << "\""
			" u7=\""  << *q->GetFile( 3) << "\">" << endl;
		// 6. Refers subfolders
		out_refers(p->GetFolder(6)->GetFolder(4));
		out_refers(p->GetFolder(7)->GetFolder(4), "refer1");
		ofile << "</rrul>" << endl;
	}
	ofile << "</" << name << ">" << endl;
	return (true);
}
bool	do_CalcVars (treebranch *t) {
	if (!(t->GetSize())) {
		cerr << "CalcVars: bad structure" << endl;
		return false;
	}
	name = "m" + *t->GetFile(0);	// 5605 - against storage
	ofile << "<" << name << ">" << endl;
	imax = t->GetSize();
	for (i = 1; i < imax; i++) {
		p = t->GetFolder(i);
		if (p->GetSize() != 4)
			cerr << "clcv: bad structure" << endl;
		else
			ofile << "<clcv no=\"" << i-1 << "\""
			<< out_uid(*p->GetFile(0)) <<
			" id=\""   << *p->GetFile( 1) << "\""
			" com=\""  << *tune_str(p->GetFile( 2)) << "\""
			" syn=\""  << *tune_str(p->GetFile( 3)) << "\"/>" << endl;
	}
	ofile << "</" << name << ">" << endl;
	return true;
}
bool	do_Groups (treebranch *t) {
	if (!(t->GetSize())) {
		cerr << "Groups: bad structure" << endl;
		return false;
	}
	// 1. root
	name = *t->GetFile(0);
	ofile << "<" << name << ">" << endl;	// root
	// 2. each group
	imax = t->GetSize();
	for (i = 1; i < imax; i++) {		// each dsro
		p = t->GetFolder(i);
		if (p->GetSize() != 5) {
			cerr << "group: bad structure size" << endl;
			continue;
		}
		// 3. group fields
		ofile << "<group no=\"" << i-1 << "\""
			<< out_uid(*p->GetFile(0)) <<
			" id=\""   << *p->GetFile( 1) << "\""
			" com=\""  << *tune_str(p->GetFile( 2)) << "\""
			" syn=\""  << *tune_str(p->GetFile( 3)) << "\">" << endl;
		// 4. Algs
 		q = p->GetFolder(4);
		jmax = q->GetSize();
		if ((jmax < 1) || (*q->GetFile(0) != "Algs")) {
			cerr << "Algs: zero len or bad nameb." << endl;
			continue;
		}
		for (j = 1; j < jmax; j++)
			ofile << "<alg no=\"" << j-1 << "\""
				<< out_uref(*q->GetFile(j)) << "/>" << endl;
		ofile << "</group>" << endl;
	}
	ofile << "</" << name << ">" << endl;
	return (true);
}
bool	do_Document_Streams (treebranch *t) {
	if (!(t->GetSize())) {
		cerr << "Document Streams: bad structure" << endl;
		return false;
	}
	name = *t->GetFile(0);
	if (name != "Document Streams") {
		cerr << "This is not Document Streams." << endl;
		return false;
	}
	name = "DocumentStreams";
	ofile << "<" << name << ">" << endl;	// root
	// 2. each dstrm
	imax = t->GetSize();
	for (i = 1; i < imax; i++) {		// each dsro
		p = t->GetFolder(i);
		if (p->GetSize() != 8) {
			cerr << "dstrm: bad structure size" << endl;
			continue;
		}
		// 3. dstrm fields
		ofile << "<dstrm no=\"" << i-1 << "\""
			<< out_uid(*p->GetFile(0)) <<
			" id=\""   << *p->GetFile( 1) << "\""
			" com=\""  << *tune_str(p->GetFile( 2)) << "\""
			" syn=\""  << *p->GetFile( 3) << "\""
			" u0=\""  << *p->GetFile( 4) << "\""
			" u1=\""  << *tune_str(p->GetFile( 5)) << "\">" << endl;
		// 4. Registers
 		q = p->GetFolder(6);
		jmax = q->GetSize();
		if ((jmax < 1) || (*q->GetFile(0) != "Registers")) {
			cerr << "Registers: zero len or bad nameb." << endl;
			continue;
		}
		for (j = 1; j < jmax; j++)
			ofile << "<dsreg no=\"" << j-1 << "\""
				<< out_uref(*q->GetFile(j)) << "/>" << endl;
		// 5. Documents
 		q = p->GetFolder(7);
		jmax = q->GetSize();
		if ((jmax < 1) || (*q->GetFile(0) != "Documents")) {
			cerr << "Documents: zero len or bad nameb." << endl;
			continue;
		}
		for (j = 1; j < jmax; j++)
			ofile << "<dsdoc no=\"" << j-1 << "\""
				<< out_uref(*q->GetFile(j)) << "/>" << endl;
		ofile << "</dstrm>" << endl;
	}
	ofile << "</" << name << ">" << endl;
	return (true);
}
bool	do_Buh (treebranch *t) {
	DWORD	bmax, k, kmax, itmp = 52;
	treebranch *s, *u, *v;

	if (t->GetSize() != 2) {
		cerr << "Buh: bad structure size." << endl;
		return false;
	}
	name = *t->GetFile(0);
	// 1. goto Buh subfolders
	t = t->GetFolder(1);
	bmax = t->GetSize();
	if (bmax < 62) {
		cerr << "Buh: bad main subfolder size:" << t->GetSize() << endl;
		return false;
	}
	// 2. main fields
//printtree("", t);
	ofile << "<" << name
		<< out_uid(*t->GetFile(0)) <<
		" u01=\""  << *t->GetFile( 1) << "\""
		" u02=\""  << *t->GetFile( 2) << "\""
		" u03=\""  << *t->GetFile( 3) << "\""
		" toed=\"" << *t->GetFile( 4) << "\""
		<< out_uref(  *t->GetFile( 5), "fs")
		<< out_uref(  *t->GetFile( 6), "fm") <<
		" anl=\""  << *t->GetFile( 7) << "\""
		" acl=\""  << *t->GetFile( 8) << "\""
		" msq=\""  << *t->GetFile( 9) << "\""
		" odl=\""  << *t->GetFile(10) << "\""
		" osl=\""  << *t->GetFile(11) << "\""
		" osp=\""  << *t->GetFile(12) << "\""
		" psl=\""  << *t->GetFile(13) << "\""
		" psp=\""  << *t->GetFile(14) << "\""
		" pvsl=\"" << *t->GetFile(15) << "\""
		" pvsp=\"" << *t->GetFile(16) << "\""
		" pql=\""  << *t->GetFile(17) << "\""
		" pqp=\""  << *t->GetFile(18) << "\""
		" u04=\""  << *t->GetFile(19) << "\""
		" u05=\""  << *t->GetFile(20) << "\""
		<< out_uref(  *t->GetFile(21), "v1")
		<< out_uref(  *t->GetFile(22), "v2")
		<< out_uref(  *t->GetFile(23), "v")
		<< out_uref(  *t->GetFile(24), "c") <<
		" u08=\""  << *t->GetFile(25) << "\""
		" coom=\"" << *t->GetFile(26) << "\""
		" cooj=\"" << *t->GetFile(27) << "\""
		" osc=\""  << *t->GetFile(28) << "\""
		" epc=\""  << *t->GetFile(29) << "\""
		" pcl=\""  << *t->GetFile(30) << "\""
		" otri=\"" << *t->GetFile(31) << "\""
		" pst=\""  << *t->GetFile(32) << "\""
		" pvst=\"" << *t->GetFile(33) << "\""
		" pqt=\""  << *t->GetFile(34) << "\""
		" cps=\""  << *t->GetFile(35) << "\""
		" cpv=\""  << *t->GetFile(36) << "\""
		" cpvs=\"" << *t->GetFile(37) << "\""
		" cpq=\""  << *t->GetFile(38) << "\""
		<< out_uref(  *t->GetFile(39), "a") <<
		" cxp=\""  << *t->GetFile(40) << "\""
		" scm=\""  << *t->GetFile(41) << "\""
		" cpod=\"" << *t->GetFile(42) << "\""
		" edo=\""  << *t->GetFile(43) << "\""
		" copa=\"" << *t->GetFile(44) << "\""
		" aoq=\""  << *t->GetFile(45) << "\""
		<< out_uref(  *t->GetFile(46), "s")
		<< out_uref(  *t->GetFile(47), "p") <<
		" u09=\""  << *t->GetFile(48) << "\""
		" u10=\""  << *t->GetFile(50) << "\"";
	if (t->IsFolder(51))	// AccParms
		itmp--;		// skip u11; decrease start of AccParms
	else
		ofile << " u11=\""  << *t->GetFile(51) << "\"";
	ofile << ">" << endl;
	// 3. now - subfolders. buh_u:
	p = t->GetFolder(49);
	imax = p->GetSize();
	for (i = 0; i < imax; i++) {
		q = p->GetFolder(i);
		if (q->GetSize() != 3)
			cerr << "buh_u: bad structure size:" << q->GetSize() << endl;
		else
			ofile << "<buh_u no=\"" << i << "\""
				" u0=\""  << *q->GetFile( 0) << "\""
				" u1=\""  << *q->GetFile( 1) << "\""
				" u2=\""  << *q->GetFile( 2) << "\""
			"/>" << endl;
 	}
	// 4. AccParams
	p = t->GetFolder(itmp + 0);	// 51|52
	if (((imax = p->GetSize()) < 1) || (*p->GetFile(0) != "AccParams"))
		cerr << "AccParams: bad structure" << endl;
	else
		for (i = 1; i < imax; i++) {
			q = p->GetFolder(i);
			if (q->GetSize() != 12)
				cerr << "AccParams: bad structure size" << endl;
			else
				ofile << "<aprm no=\"" << i-1 << "\""
					<< out_uid(*q->GetFile(0)) <<
					" id=\""   << *q->GetFile( 1) << "\""
					" com=\""  << *tune_str(q->GetFile( 2)) << "\""
					" syn=\""  << *tune_str(q->GetFile( 3)) << "\""
					" typ=\""  << *q->GetFile( 4) << "\""
					" len=\""  << *q->GetFile( 5) << "\""
					" prc=\""  << *q->GetFile( 6) << "\""
					<< out_uref(*q->GetFile( 7)) <<
					" pos=\""  << *q->GetFile( 8) << "\""
					" tri=\""  << *q->GetFile( 9) << "\""
					" u0=\""   << *q->GetFile(10) << "\""
					" per=\""  << *q->GetFile(11) << "\""
				"/>" << endl;
		}
	// 5. Plans
	p = t->GetFolder(itmp + 1);	// 52|53
	if (((imax = p->GetSize()) < 1) || (*p->GetFile(0) != "Plans"))
		cerr << "Plans: bad structure" << endl;
	else
		for (i = 1; i < imax; i++) {
			q = p->GetFolder(i);
			jmax = q->GetSize();
			if ((jmax < 6) || (jmax > 7))
				cerr << "Plans: bad structure size: " << jmax << endl;
			else {
				ofile << "<plan no=\"" << i-1 << "\""
					<< out_uid(*q->GetFile(0)) <<
					" id=\""   << *q->GetFile( 1) << "\""
					" com=\""  << *tune_str(q->GetFile( 2)) << "\""
					" syn=\""  << *tune_str(q->GetFile( 3)) << "\""
					" ct1=\""  << *q->GetFile( 4) << "\"";
					if (jmax > 6)
						ofile << " ct2=\""  << *q->GetFile( 5) << "\"";
				ofile << ">" << endl;
				r = q->GetFolder(jmax - 1);
				jmax = r->GetSize();
				for (j = 1; j < jmax; j++) {
					s = r->GetFolder(j);
					if (s->GetSize() != 11)
						cerr << "accnt: bad structure size:" << s->GetSize() << endl;
					else {
						ofile << "<accnt no=\"" << j-1 << "\""
							<< out_uid(*s->GetFile(0)) <<
							" iid=\""   << *s->GetFile( 1) << "\""
							" nam=\""   << *tune_str(s->GetFile( 2)) << "\""
							" u0=\""    << *s->GetFile( 3) << "\""
							" acc=\""   << *s->GetFile( 4) << "\""
							" isv=\""   << *s->GetFile( 5) << "\""
							" isq=\""   << *s->GetFile( 6) << "\""
							" isob=\""  << *s->GetFile( 7) << "\""
							" isg=\""   << *s->GetFile( 8) << "\""
							" aat=\""   << *s->GetFile( 9) << "\""
						">" << endl;
						v = s->GetFolder(10);
						kmax = v->GetSize();
						for (k = 1; k < kmax; k++) {
							u = v->GetFolder(k);
							if (u->GetSize() != 15)
								cerr << "accsk: bad structure size:" << u->GetSize() << endl;
							else
								ofile << "<accsk no=\"" << k-1 << "\""
									" nid=\""  << *u->GetFile( 0) << "\""
									" id=\""   << *u->GetFile( 1) << "\""
									" u0=\""   << *u->GetFile( 2) << "\""
									" u1=\""   << *u->GetFile( 3) << "\""
									" u2=\""   << *u->GetFile( 4) << "\""
									" u3=\""   << *u->GetFile( 5) << "\""
									" u4=\""   << *u->GetFile( 6) << "\""
									" u5=\""   << *u->GetFile( 7) << "\""
									" u6=\""   << *u->GetFile( 8) << "\""
									" u7=\""   << *u->GetFile( 9) << "\""
									<< out_uref(*u->GetFile(10), "s") <<
									" oo=\""   << *u->GetFile(11) << "\""
									" uos=\""  << *u->GetFile(12) << "\""
									" uovs=\"" << *u->GetFile(13) << "\""
									" uoq=\""  << *u->GetFile(14) << "\""
								"/>" << endl;
						}
						ofile << "</accnt>" << endl;
					}
				}
				ofile << "</plan>" << endl;
			}
		}
	// 6. ProvParams
	p = t->GetFolder(itmp + 2);	// 53|54
	if (((imax = p->GetSize()) < 1) || (*p->GetFile(0) != "ProvParams"))
		cerr << "ProvParams: bad structure" << endl;
	else
		for (i = 1; i < imax; i++) {
			q = p->GetFolder(i);
			if (q->GetSize() != 11)
				cerr << "ProvParams: bad structure size" << endl;
			else
				ofile << "<pprm no=\"" << i-1 << "\""
					<< out_uid(*q->GetFile(0)) <<
					" id=\""   << *q->GetFile( 1) << "\""
					" com=\""  << *tune_str(q->GetFile( 2)) << "\""
					" syn=\""  << *tune_str(q->GetFile( 3)) << "\""
					" typ=\""  << *q->GetFile( 4) << "\""
					" len=\""  << *q->GetFile( 5) << "\""
					" prc=\""  << *q->GetFile( 6) << "\""
					<< out_uref(*q->GetFile( 7)) <<
					" tri=\""  << *q->GetFile( 8) << "\""
					" pos=\""  << *q->GetFile( 9) << "\""
					" chce=\"" << *q->GetFile(10) << "\""
				"/>" << endl;
		}
	// 7. OperParams
	p = t->GetFolder(itmp + 3);	// 54|55
	if (((imax = p->GetSize()) < 1) || (*p->GetFile(0) != "OperParams"))
		cerr << "OperParams: bad structure" << endl;
	else
		for (i = 1; i < imax; i++) {
			q = p->GetFolder(i);
			if (q->GetSize() != 11)
				cerr << "OperParams: bad structure size" << endl;
			else
				ofile << "<oprm no=\"" << i-1 << "\""
					<< out_uid(*q->GetFile(0)) <<
					" id=\""   << *q->GetFile( 1) << "\""
					" com=\""  << *tune_str(q->GetFile( 2)) << "\""
					" syn=\""  << *tune_str(q->GetFile( 3)) << "\""
					" typ=\""  << *q->GetFile( 4) << "\""
					" len=\""  << *q->GetFile( 5) << "\""
					" prc=\""  << *q->GetFile( 6) << "\""
					<< out_uref(*q->GetFile( 7)) <<
					" tri=\""  << *q->GetFile( 8) << "\""
					" pos=\""  << *q->GetFile( 9) << "\""
					" chce=\"" << *q->GetFile(10) << "\""
				"/>" << endl;
		}
	// 8. Form(s)
	imax = bmax - 62;	// ??? itmp ???
	for (i = 0; i < imax; i++) {
		p = t->GetFolder(itmp + 4 + i);	// 56+
		if (((jmax = p->GetSize()) < 1) || (*p->GetFile(0) != "Form"))
			cerr << "Form: bad structure" << endl;
		else {
			ofile << "<bfrms no=\"" << i << "\">" << endl;
			for (j = 1; j < jmax; j++) {
				q = p->GetFolder(j);
				if (q->GetSize() != 4)
					cerr << "Form: bad structure size" << endl;
				else
					ofile << "<bfrm no=\"" << j-1 << "\""
						<< out_uid(*q->GetFile(0)) <<
						" id=\""   << *q->GetFile( 1) << "\""
						" com=\""  << *tune_str(q->GetFile( 2)) << "\""
						" syn=\""  << *tune_str(q->GetFile( 3)) << "\""
					"/>" << endl;
			}
			ofile << "</bfrms>" << endl;
		}
	}
	// 9. SbKind
	p = t->GetFolder(bmax - 5);	// 57
	if (((imax = p->GetSize()) < 1) || (*p->GetFile(0) != "SbKind"))
		cerr << "SbKind: bad structure size (" << imax << ") or name (" << *p->GetFile(0) << ")" << endl;
	else
		for (i = 1; i < imax; i++) {
			q = p->GetFolder(i);
			if (q->GetSize() != 16)
				cerr << "SbKind: bad structure size:" << q->GetSize() << endl;
			else {
				ofile << "<sbknd no=\"" << i-1 << "\""
					<< out_uid(*q->GetFile(0)) <<
					" id=\""   << *q->GetFile( 1) << "\""
					" com=\""  << *tune_str(q->GetFile( 2)) << "\""
					" syn=\""  << *tune_str(q->GetFile( 3)) << "\""
					" typ=\""  << *q->GetFile( 4) << "\""
					" len=\""  << *q->GetFile( 5) << "\""
					" prc=\""  << *q->GetFile( 6) << "\""
					<< out_uref(  *q->GetFile( 7)) <<
					" tri=\""  << *q->GetFile( 8) << "\""
					" pos=\""  << *q->GetFile( 9) << "\""
					" chce=\"" << *q->GetFile(10) << "\""
					<< out_uref(  *q->GetFile(11), "p")
					<< out_uref(  *q->GetFile(12), "v") <<
					" u0=\""   << *q->GetFile(14) << "\""
					" u1=\""   << *q->GetFile(15) << "\""
				">" << endl;

				r = q->GetFolder(13);
				jmax = r->GetSize();
				for (j = 1; j < jmax; j++) {
					s = r->GetFolder(j);
					if (s->GetSize() != 3)
						cerr << "sbcnt_u: bad structure size:" << s->GetSize() << endl;
					else
						ofile << "<sbknd_u no=\"" << j-1 << "\""
							" u0=\""   << *s->GetFile( 0) << "\""
							" u1=\""   << *s->GetFile( 1) << "\""
							" u2=\""   << *s->GetFile( 2) << "\""
						"/>" << endl;
				}
				ofile << "</sbknd>" << endl;
			}
		}
	// 10. TypOpersDef
	p = t->GetFolder(bmax - 4);	// 58
	if (((imax = p->GetSize()) < 1) || (*p->GetFile(0) != "TypOpersDef"))
		cerr << "TypOpersDef: bad structure size (" << imax << ") or name (" << *p->GetFile(0) << ")" << endl;
	else
		for (i = 1; i < imax; i++) {
			q = p->GetFolder(i);
			jmax = q->GetSize();
			if ((jmax < 4) || (jmax > 5))
				cerr << "TypOpersDef: bad structure size:" << q->GetSize() << endl;
			else
				ofile << "<todef no=\"" << i-1 << "\""
					<< out_uid(*q->GetFile(0)) <<
					" u1=\""  << *q->GetFile(1) << "\""	// ""
					" u2=\""  << *q->GetFile(2) << "\""	// ""
					" u3=\""  << *q->GetFile(3) << "\"";	// ""
				if (jmax == 4)
					ofile << "/>" << endl;
				else {	// Disribution
					q = q->GetFolder(4);
					jmax = q->GetSize();
					ofile << ">" << endl << "<todef_u";
					for (j = 0; j < jmax; j++)
						ofile << " u" << j << "=\"" << *q->GetFile(j) << "\"";
					ofile << "/>" << endl <<
					"</todef>" << endl;
				}
		}
	// 11. CorrProvsDef
	p = t->GetFolder(bmax - 3);	// 59
	if (((imax = p->GetSize()) < 1) || (*p->GetFile(0) != "CorrProvsDef"))
		cerr << "CorrProvsDef: bad structure size (" << imax << ") or name (" << *p->GetFile(0) << ")" << endl;
	else
		for (i = 1; i < imax; i++) {
			q = p->GetFolder(i);
			if (q->GetSize() != 4)
				cerr << "CorrProvsDef: bad structure size" << endl;
			else
				ofile << "<cpdef no=\"" << i-1 << "\""
					<< out_uid(*q->GetFile(0)) <<
					" u1=\""  << *q->GetFile(1) << "\""	// ""
					" u2=\""  << *q->GetFile(2) << "\""	// ""
					" u3=\""  << *q->GetFile(3) << "\""	// ""
				"/>" << endl;
		}
	// 12. ProvHardFldDef
	p = t->GetFolder(bmax - 2);	// 60
	if (((imax = p->GetSize()) < 1) || (*p->GetFile(0) != "ProvHardFldDef"))
		cerr << "ProvHardFldDef: bad structure size (" << imax << ") or name (" << *p->GetFile(0) << ")" << endl;
	else
		for (i = 1; i < imax; i++) {
			q = p->GetFolder(i);
			if (q->GetSize() != 11)
				cerr << "ProvHardFldDef: bad structure size" << endl;
			else
				ofile << "<phfd no=\"" << i-1 << "\""
					<< out_uid(*q->GetFile(0)) <<
					" u01=\""  << *q->GetFile( 1) << "\""	// a
					" u02=\""  << *q->GetFile( 2) << "\""	// ""
					" u03=\""  << *q->GetFile( 3) << "\""	// ""
					" u04=\""  << *q->GetFile( 4) << "\""	// c
					" u05=\""  << *q->GetFile( 5) << "\""	// #
					" u06=\""  << *q->GetFile( 6) << "\""	// #
					" u07=\""  << *q->GetFile( 7) << "\""	// #
					" u08=\""  << *q->GetFile( 8) << "\""	// #
					" u09=\""  << *q->GetFile( 9) << "\""	// #
					" u10=\""  << *q->GetFile(10) << "\""	// #
				"/>" << endl;
		}
	// 13. OperJournal
	do_Journalisters(t->GetFolder(bmax - 1), "OperJournal");	// 61 - the end
	// The End
	ofile << "</" << name << ">" << endl;
	return (true);
}
bool	do_CRC (treebranch *t) {
	if (!(t->GetSize())) {
		cerr << "CRC: bad structure" << endl;
		return false;
	}
	// 1. root
	name = *t->GetFile(0);
	ofile << "<" << name << " v=\"" << *t->GetFile(1) << "\"/>"<< endl;
	return (true);
}

#define CHK /*cerr << counter++ << endl;*/
void	do_MMS(Pdata & buffer, const string & ccstr) {
	//	print_bq (buffer);
	//	printtree("", bq2tree(buffer)->GetFolder(0));
	treebranch *t;

	t = bq2tree(buffer)->GetFolder(0);
	ofile << "<mms" << ccstr << ">" << endl;
//cerr <<"MMS start" << endl;
//static int counter = 0;
CHK
	do_MainDataContDef	(t->GetFolder( 0));
CHK
	do_TaskItem		(t->GetFolder( 1));
CHK
	do_GenJrnlFldDef	(t->GetFolder( 2));
CHK
	do_DocSelRefObj		(t->GetFolder( 3));
CHK
	do_DocNumDef		(t->GetFolder( 4));
CHK
	do_Consts		(t->GetFolder( 5));
CHK
	do_SbCnts		(t->GetFolder( 6));
CHK
	do_Registers		(t->GetFolder( 7));
CHK
	do_Documents		(t->GetFolder( 8));
CHK
	do_Journalisters	(t->GetFolder( 9), "Journalisters");
CHK
	do_EnumList		(t->GetFolder(10));
CHK
	do_ReportList		(t->GetFolder(11));
CHK
	do_CJ			(t->GetFolder(12));
CHK
	do_Calendars		(t->GetFolder(13));
CHK
	do_Algorithms		(t->GetFolder(14));
CHK
	do_RecalcRules		(t->GetFolder(15));
CHK
	do_CalcVars		(t->GetFolder(16));
CHK
	do_Groups		(t->GetFolder(17));
CHK
	do_Document_Streams	(t->GetFolder(18));
CHK
	do_Buh			(t->GetFolder(19));
CHK
	if (t->GetSize() >= 21) {
		do_CRC			(t->GetFolder(20));
	}
//cerr <<"MMS end" << endl;
	cTag("mms");
}
