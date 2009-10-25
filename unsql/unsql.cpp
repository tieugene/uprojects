#include <stdio.h>

int	main ( int argc, const char *argv[] )
{
        FILE *fp, *fr;
	int i;
	static char key[] = "19465912879oiuxc ensdfaiuo3i73798kjl";
	int ch;

	if ( argc < 2 || argc > 3 ) {
		printf("Usage: unsql infile [outfile]\n");
		return -1;
	}
	fr = (argc==3 ? fopen(argv[2],"w+") : stdout );
	if (!fr) {
		printf ("Cannot open output file\n");
		return -1;
	}

	if (! (fp=fopen(argv[1],"rb"))) {
    		printf("Cannot open file %s for reading", argv[1]);
		return -1;
	}
	for (i=0; (ch=fgetc(fp))!=EOF ; ++i) {
		fputc( ch ^ key [ i % 36 ] , fr);
	}
	fclose( fp);
	fclose( fr);
	return 0;
}
