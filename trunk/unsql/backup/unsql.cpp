#include <stdio.h>
#include <string.h>

char	*findkey(char *key0, char *key1, char *src, char *dst) {
	char *start = NULL, *end = NULL;
	int i;

	start = strstr(src, key0);
	if (start) {
		start += strlen(key0);
		end = strstr(start, key1);
		if (end) {
			i = end - start;
			strncpy(dst, start, i);
			dst[i] = '\0';
		} else printf("end not found\n");
	} else printf("start not found\n");
	return dst;
}

int	main ( int argc, const char *argv[] ) {
        FILE *f;
	int i, ch;
	static char key[] = "19465912879oiuxc ensdfaiuo3i73798kjl";
	static char *k[6] = {
		"{{\"Server\",\"",
		"\"},{\"DB\",\"",
		"\"},{\"UID\",\"",
		"\"},{\"PWD\",\"",
		"\"},{\"Checksum\",\"",
		"\"}}"
	};
	static char buffer[100];
	static char result[5][100];

	if ( argc < 2 ) { printf("Usage: unsql <infile>\n"); return -1; }
	if (! (f = fopen(argv[1],"rb"))) { printf("Cannot open file %s for reading", argv[1]); return -1; }
	for (i=0; (ch = fgetc(f)) != EOF; ++i)
		buffer[i] = ch ^ key [ i % 36 ];
	fclose( f);
	buffer[i] = '\0';
	for (i=0; i < 5; ++i)
		findkey(k[i], k[i + 1], buffer, result[i]);
	printf("%s\n%s\t%s\t%s\t%s\t%s\n", buffer, result[0], result[1], result[2], result[3], result[4]);
	return 0;
}
