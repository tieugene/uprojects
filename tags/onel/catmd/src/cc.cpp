// cc.cpp
// parse Container.Contents (C.C) strings into 2D-vector of string
// info: C.C cosists of {"Container.Contents",({"string0","string1","string2","string3"})}

#include "catmd.h"

extern fstream ofile;

const char	cQ = '"';
const char	cPl = '{';
const char	cPr = '}';

/*void	outbulk(DSVector &bulk) {
	DWORD	i, j;

	for (i = 0; i < bulk.size(); i++) {
		cerr << bulk[i].size() << ": ";
		for (j = 0; j < bulk[i].size(); j++)
			cerr << "\"" << bulk[i][j] << "\" ";
		cerr << endl;
	}
}*/

// parse group of quouted strings
// in: string like "...","...",...
// returns vector of strings w/o quots
SVector	parsegroup(string &s) {
	SVector		item;
	uint		iStart = 0, iEnd = 0, iMax = s.rfind(cQ);

	while (iStart < iMax) {
		iStart = s.find(cQ, iStart);					// find 1st "
		iEnd   = s.find(cQ, iStart + 1);				// find 2nd "
		item.push_back(s.substr(iStart + 1, iEnd - iStart - 1));	// inner of "..."
		iStart = iEnd + 1;						// out of 2nd "
	}
	return item;
}

DSVector	do_cc(string &data)	{	// data - C.C string
	string		s;
	DSVector	bulk;
	SVector		bulkitem;
	uint		iStart, iEnd, iQ, iP, iMax;

	iMax = data.rfind(cPr);						// right margin = right }
	iStart = 1;
	// 2. parse a line
	while (iStart < iMax) {
		bulkitem.clear();
		iQ = data.find(cQ, iStart);				// find first "
		iP = data.find(cPl, iStart);				// find first {
		iStart = min(iQ, iP);					// who lefter ?
		if (iStart < iMax) {					// we're not out of last } ?
			if (data[iStart] == cQ) {			// this is simple "string"
				iEnd = data.find(cQ, iStart + 1);	// next "
				bulkitem.push_back(data.substr(iStart + 1, iEnd - iStart - 1));	// inner of "..."
			} else {					// this is {block}
				iEnd = data.find(cPr, iStart + 1);	// next "
				s = data.substr(iStart + 1, iEnd - iStart - 1);
				bulkitem = parsegroup(s);		// inner of {...}
			}
			bulk.push_back(bulkitem);
			iStart = iEnd + 1;				// out of 2nd "
		}
	}
// *. the end
	return (bulk);
}

SVector	FindCC(DSVector &bulk, string &data) {
	DWORD i;
	SVector	bulkitem, tmpbulkitem;
	bulkitem.empty();
	for (i = 0; i < bulk.size(); i++) {
		tmpbulkitem = bulk[i];
		if ((tmpbulkitem.size() == 4) && (tmpbulkitem[1] == data)) {
			bulkitem = tmpbulkitem;
			break;
		}
	}
	return (bulkitem);
}

void	do_CC(Pdata & buffer, const string & ccstr) {
	// process CC bq
	int	i, imax, j, jmax;
	treebranch *t, *p;
return;	// 5605
	t = bq2tree(buffer)->GetFolder(0);
	ofile << "<cc" << ccstr << " v=\"" << *t->GetFile(0) << "\">" << endl;
	imax = t->GetSize();
	if (imax > 1)
		for (i = 1; i < imax; i++) {
			ofile << "<ccn";
			p = t->GetFolder(i);
			jmax = p->GetSize();
			for (j = 0; j < jmax; j++)
				ofile << " v_" << j << "=\"" << *p->GetFile(j) << "\"";
			ofile << "/>" << endl;
		}
	cTag("cc");
	delete t;
}

void	do_CP(Pdata & buffer, const string & ccstr) {
	// process CP bq
	int	i, imax;
	treebranch *t, *p;
	string	nm;

	t = bq2tree(buffer)->GetFolder(0);
	ofile << "<cp" << ccstr << ">" << endl;
	imax = t->GetSize();
	for (i = 0; i < imax; i++) {
		p = t->GetFolder(i);
		if (p->GetSize() != 3)
			cerr << "Bad cpn size:" << p->GetSize() << endl;
		else {
			nm = *p->GetFile(1);
			if (nm == "\01Blank")	// hack - changing \01Blank to "" w/ adding 'blank' attribute
				nm = "\" blank=\"1";
			ofile << "<" << *p->GetFile(0) << " nm=\"" << nm << "\" u0=\"" << *p->GetFile(2) << "\"/>" << endl;
		}
	}
	cTag("cp");
	delete t;
}
