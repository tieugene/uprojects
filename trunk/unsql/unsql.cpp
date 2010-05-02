// unsql.cpp version 0.0.2
/* Todo:
	server:	{{"Server","
	db:	"},{"DB","
	UID:	"},{"UID","
	pwd:	"},{"PWD","
	crc:	"},{"Checksum","
	eof:	"}} (or buflen - 3)
*/	
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int	main ( int argc, char **argv )
{
        FILE		*fp;
	int		op = 0;
	bool		action[6] = {false, false, false, false, false, false};
	char		delimiter = '\t', *buffer;
	static char	key[] = "19465912879oiuxc ensdfaiuo3i73798kjl";
	long		fsize;

	// 1. get options
	while ((op = getopt(argc, argv, "radsbupcS:B:U:P:C:")) != -1) {
		switch (op){
			case 'r':
				action[0] = true;
				break;
			case 'a':
				action[1] = action[2] = action[3] = action[4] = action[5] = true;
				break;
			case 'd':
				delimiter = optarg[0];
				break;
			case 's':
				action[1] = true;
				break;
			case 'b':
				action[2] = true;
				break;
			case 'u':
				action[3] = true;
				break;
			case 'p':
				action[4] = true;
				break;
			case 'c':
				action[5] = true;
				break;
			case '?':
				printf("Error found !\n");
				break;
			default:
				printf("Default\n");
		};
	};
	// 2. read file
	// 2.1. open
	if (! (fp=fopen(argv[argc - 1],"rb"))) {
		printf("Cannot open input file %s for reading\n", argv[1]);
		return -1;
	}
	// 2.2. get file size
	fseek(fp, 0L, SEEK_END);
	fsize = ftell(fp);
	rewind(fp);
	// 2.3. make buffer
	buffer = (char *) malloc(fsize);
	if (buffer == NULL) {
		printf("Cannot allocate memory for buffer\n");
		return -2;
	};
	// 2.4. read and close
	if (fread(buffer, sizeof(char), fsize, fp) != fsize) {
		printf("Cannot allocate memory for buffer\n");
		return -3;
	};
	fclose(fp);
	// 3. decode file
	for (int i=0; i < fsize; i++) {
		buffer[i] ^= key[i % 36];
	};
	// 4. split on parts
	printf("%s\n", buffer);
	free(buffer);
	return 0;
}
