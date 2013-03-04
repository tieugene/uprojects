
#include <fcntl.h>
#include <rpm/rpmcli.h>
#include <rpm/rpmdb.h>

#include <map>
#include <set>
#include <string>

typedef std::set <std::string> string_set;
typedef std::map <std::string, std::string> string_map;

static struct poptOption optionTable[] = {
   { NULL, '\0', POPT_ARG_INCLUDE_TABLE, rpmcliAllPoptTable, \
     0, "Generic rpm options:", NULL },
   POPT_AUTOHELP
   POPT_TABLEEND
};

int main (int argc, char * const * argv)
{
   poptContext options = rpmcliInit (argc, argv, optionTable);

   if (rpmReadConfigFiles (NULL, NULL) != 0) {
      fprintf (stderr, "rpmReadConfigFiles fail.\n");
      exit (1);
   }

   rpmdb db;

   if (rpmdbOpen ("", &db, O_RDONLY, 0) != 0) {
      fprintf (stderr, "rpmdbOpen failed.\n");
      exit (1);
   }

   rpmdbMatchIterator i = rpmdbInitIterator (db, RPMTAG_NAME, NULL, 0);

   if (i == NULL) {
      fprintf (stderr, "rpmdbInitIterator failed.\n");
      exit (1);
   }

   string_set packages;
   string_set required;
   string_map prov_to_pack, file_to_pack;

   while (Header head = rpmdbNextIterator (i)) {

	const char * name;
	const char * version;
	const char * release;

	int res = headerNVR (head, &name, &version, &release);
	assert (res == 0);

	std::string sname = name;
	sname += "-";
	sname += version;
	sname += "-";
	sname += release;
//	packages.insert (sname);

	int_32 htag;
	int_32 htype;
//	hPTR_t hptr;
	void	*hptr;
	int_32 hcount;
	// services
	headerGetEntry(head, RPMTAG_PROVIDES, &htype, &hptr, &hcount);
	assert (htype == RPM_STRING_ARRAY_TYPE);
	for (int i = 0; i != hcount; ++i) {
		const char * prov = ((const char * const *) hptr)[i];
		string_map::const_iterator	ptr = prov_to_pack.find (prov);
		if (ptr == prov_to_pack.end())
			prov_to_pack[prov] = sname;
		else
			fprintf (stderr, "%s: service \"%s\" already provided by %s\n", sname.c_str(), prov, ptr->second.c_str());
	}
	//free(hptr);
//	headerGetEntry(h, RPMTAG_OLDFILENAMES, NULL, (void **) &p, &__count);
	headerGetEntry(head, RPMTAG_OLDFILENAMES, &htype, &hptr, &hcount);
	assert (htype == RPM_STRING_ARRAY_TYPE);
	for (int i = 0; i != hcount; ++i) {
		const char * prov = ((const char * const *) hptr)[i];
		string_map::const_iterator	ptr = file_to_pack.find (prov);
		if (ptr == file_to_pack.end())
			file_to_pack[prov] = sname;
		else
			fprintf (stderr, "%s: file \"%s\" already provided by %s\n", sname.c_str(), prov, ptr->second.c_str());
	}
   }

   rpmdbFreeIterator (i);

   rpmdbClose (db);

   rpmcliFini (options);

   return 0;
}
