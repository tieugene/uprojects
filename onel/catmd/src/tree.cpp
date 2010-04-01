#include "catmd.h"

treebranch::~treebranch () {
	DWORD i, imax = GetSize();
	for (i = 0; i < imax; i++) {
		if (IsFolder(i))
			delete val[i].val.folder;
		else
			delete val[i].val.file;
	}
}

bool	treebranch::ChkIdx (DWORD i, const char * s) {
	if ((i < 0) || (i >= GetSize())) {
		cerr << s << ": index [" << i << "] out of bounds." << endl;
		return (false);
	}
	return (true);
}

int	treebranch::GetSize (void) {
	return val.size();
}

bool	treebranch::IsFolder (DWORD i) {
	if (ChkIdx(i, "IsFolder"))
		return val[i].isfolder;
	return (false);
}

string * treebranch::AddFile (const string & s) {
	treenode t;
	t.isfolder = false;
	t.val.file = new string(s);
	val.push_back(t);
	return val[GetSize()-1].val.file;
}

treebranch * treebranch::AddFolder (void) {
	treenode t;
	t.isfolder = true;
	t.val.folder = new (treebranch);
	val.push_back(t);
	return val[GetSize()-1].val.folder;
}

string * treebranch::GetFile (DWORD i) {
	if (ChkIdx(i, "GetFile")) {
		if (IsFolder(i)) {
			cerr << "node [" << i << "] is not File." << endl;
			return (NULL);
		}
		else
			return val[i].val.file;
	}
	return (NULL);
}

treebranch * treebranch::GetFolder (DWORD i) {
	if (ChkIdx(i, "GetFolder")) {
		if (!IsFolder(i)) {
			cerr << "node [" << i << "] is not Folder." << endl;
			return (NULL);
		}
		else
			return val[i].val.folder;
	}
	return (NULL);
}

// for tests
void	printtree (const string & tab, treebranch * t) {
	DWORD	i, imax = t->GetSize();

	for (i = 0; i < imax; i++)	{
		if (t->IsFolder(i)) {
			cerr << tab << '{' << endl;
			printtree(tab + "-", t->GetFolder(i));
			cerr << tab << '}' << endl;
		} else
			cerr << tab << "\"" << *t->GetFile(i) << "\"" << endl;
	}
}

/* parse */
BYTE *	parse_quotes (BYTE * ptr, const BYTE * end, treebranch * tree) {
	BYTE	*start = ptr, *dest = ptr;

	while(ptr < end) {
		if (*ptr == '"') {
			if (ptr[1] == '"')	// doubled "; !!! - check EOF
				ptr++;		// skip 1st "
			else {			// the end
				*dest = '\0';
				ptr++;
				break;
			}
		}
		*dest++ = *ptr++;
	}
	tree->AddFile((char *) start);
	return (ptr);
}

BYTE *	parse_blocks (BYTE * ptr, const BYTE * end, treebranch * tree) {
	while(ptr < end) {
		switch (*ptr) {
			case ('"') :	// parse inside quotes; ptr - behind "
				ptr = parse_quotes (ptr + 1, end, tree);
				break;
			case ('{') :	// dive in; ptr - behind {
				ptr = parse_blocks (ptr + 1, end, tree->AddFolder());
				break;
			case ('}') :	// dive out; ptr - behind }
				return (ptr + 1);
				break;
			default:	// skip
				ptr++;
				break;
		}
	}
	return (ptr);
}

treebranch	* bq2tree(Pdata & data) {
	treebranch	*t = new treebranch;
	parse_blocks (data.data, data.data + data.size, t);
	return t;
}
