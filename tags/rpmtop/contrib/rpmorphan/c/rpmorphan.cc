
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
   string_map prov_to_pack;

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
      packages.insert (sname);

      HeaderIterator j = headerInitIterator (head);
      if (j == NULL) {
         fprintf (stderr, "headerInitIterator failed.\n");
         exit (1);
      }

      int_32 htag;
      int_32 htype;
      hPTR_t hptr;
      int_32 hcount;
      string_set package_required;

      while (headerNextIterator (j,
                                 &htag,
                                 &htype,
                                 &hptr,
                                 &hcount) == 1) {
         if (htag == RPMTAG_PROVIDENAME) {
            assert (htype == RPM_STRING_ARRAY_TYPE);
            for (int k = 0; k != hcount; ++k) {
               const char * prov = ((const char * const *) hptr)[k];
               prov_to_pack.insert (std::make_pair (prov, sname));
//                if (!res.second && sname != res.first->second) {
//                   printf ("Both %s and %s provide %s\n",
//                           sname.c_str(), res.first->second.c_str(), prov);
//                }
            }
         }
         else if (htag == RPMTAG_REQUIRENAME) {
            assert (htype == RPM_STRING_ARRAY_TYPE);
            for (int k = 0; k != hcount; ++k) {
               package_required.insert (((const char * const *) hptr)[k]);
            }
         }
      }

      headerFreeIterator (j);

      // Now add package_required to required, but only if not provided by self.
      for (string_set::const_iterator k = package_required.begin();
	   k != package_required.end(); ++k) {
         string_map::const_iterator p = prov_to_pack.find (*k);
         if (p == prov_to_pack.end() || p->second != sname)
            required.insert (*k);
      }
   }

   rpmdbFreeIterator (i);

   rpmdbClose (db);

   for (string_set::const_iterator ii = required.begin();
        ii != required.end(); ++ii) {
      string_map::const_iterator jj = prov_to_pack.find (*ii);

      if (jj == prov_to_pack.end()) {
         fprintf (stderr, "%s is required but not provided.\n", ii->c_str());
         continue;
      }

      packages.erase (jj->second);
   }

   for (string_set::const_iterator ii = packages.begin();
        ii != packages.end(); ++ii) {
      printf ("%s\n", ii->c_str());
   }

   rpmcliFini (options);

   return 0;
}
