// unsql.cpp version 0.0.1
#include <stdio.h>

int	main ( int argc, const char *argv[] )
{
        FILE *fp;
	int i, ch;
	static char key[] = "19465912879oiuxc ensdfaiuo3i73798kjl";

	if ( argc != 2 ) {
		printf("Usage: unsql infile\n");
		return -1;
	}
	if (! (fp=fopen(argv[1],"rb"))) {
    		printf("Cannot open input file %s for reading", argv[1]);
		return -1;
	}
	for (i=0; (ch=fgetc(fp))!=EOF ; ++i) {
		putchar(ch ^ key[i % 36]);
	}
	fclose( fp);
	return 0;
}
