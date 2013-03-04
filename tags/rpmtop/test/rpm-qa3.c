// Show all installed rpms - via rpm interface
// Compile: gcc -Wall -O3 -lrpm -o rpm-qa3 rpm-qa3.c

#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

#include <rpm/rpmlib.h>

int main( int argc, char **argv )
{
	int_32 type, count, i=2;
	char *name;
	rpmdb db;
	Header h;
	rpmdbMatchIterator mi;

	rpmReadConfigFiles( NULL, NULL );
	if( rpmdbOpen( "", &db, O_RDONLY, 0644 ) != 0 ) {
		fprintf( stderr, "cannot open database!\n" );
		exit( 1 );
	}
	for (i=0; i<2; i++) {
		mi = rpmdbInitIterator(db, RPMDBI_PACKAGES, NULL, 0);
		while ((h = rpmdbNextIterator(mi))) {
			headerGetEntry(h, RPMTAG_NAME, &type, (void **) &name, &count);
			printf("%d: %s\n", i, name);
		}
		rpmdbFreeIterator(mi);
	}
	rpmdbClose( db );
	return 0;
}

