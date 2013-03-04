// Show all installed rpms - via rpm interface
// Compile: gcc -Wall -lrpm -o rpm-qa2 rpm-qa2.c

#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

#include <rpm/rpmlib.h>

int main( int argc, char **argv )
{
	int_32 type, count;
	char *name;
	rpmdb db;
	Header h;

	rpmReadConfigFiles( NULL, NULL );
	if( rpmdbOpen( "", &db, O_RDONLY, 0644 ) != 0 ) {
		fprintf( stderr, "cannot open database!\n" );
		exit( 1 );
	}
	rpmdbMatchIterator mi = rpmdbInitIterator(db, RPMDBI_PACKAGES, NULL, 0);
	while ((h = rpmdbNextIterator(mi))) {
		headerGetEntry(h, RPMTAG_NAME, &type, (void **) &name, &count);
		printf("%s\n", strdup(name));
	}
	rpmdbFreeIterator(mi);
	rpmdbClose( db );
	return 0;
}

