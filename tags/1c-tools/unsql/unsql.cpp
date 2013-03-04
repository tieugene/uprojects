// unsql.cpp version 0.0.3

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <regex.h>
#include <err.h>

const char *mask = "^{{\"Server\",\"\\(\\w*\\)\"},{\"DB\",\"\\(\\w*\\)\"},{\"UID\",\"\\(\\w*\\)\"},{\"PWD\",\"\\(\\w*\\)\"},{\"Checksum\",\"\\(\\w*\\)\"}}$";
const char *outmask = "{{\"Server\",\"%s\"},{\"DB\",\"%s\"},{\"UID\",\"%s\"},{\"PWD\",\"%s\"},{\"Checksum\",\"%s\"}}";
const char *usage = "Usage: unsql [options] 1Cv7.DBA\n\
-r		show raw\n\
-a		get all\n\
-d <str>	set delimiter\n\
-s		get Server - server\n\
-b		get DB - SQL database name\n\
-u		get UID - SQL database user\n\
-p		get PWD - SQL database password\n\
-c		get Checksum\n\
-h		show help (default)\n\
-S <str>	set Server\n\
-B <str>	set DB\n\
-U <str>	set UID\n\
-P <str>	set PWD\n\
-C <str>	set Checksum";

void	showusage(void) { printf("%s\n", usage); }

int	main ( int argc, char **argv )
{
        FILE		*fp;
	int		op = 0, reti;
	bool		action[11] = {false, false, false, false, false, false, false, false, false, false, false}, opted=false, showed=false, seted=false;
	char		*delimiter = (char *) "\t", *buffer, *outbuffer, *term[5], *set[5];
	static char	key[] = "19465912879oiuxc ensdfaiuo3i73798kjl";
	unsigned long	fsize;
	regex_t		regex;
	regmatch_t	match[7];

	// 1. get options
	while ((op = getopt(argc, argv, "rad:sbupcS:B:U:P:C:")) != -1) {
		switch (op){
			case 'r': action[5] = true; opted = true; break;
			case 'a': action[0] = action[1] = action[2] = action[3] = action[4] = true; opted = true; break;
			case 'd': delimiter = optarg; opted = true; break;
			case 's': action[0] = true; opted = true; break;
			case 'b': action[1] = true; opted = true; break;
			case 'u': action[2] = true; opted = true; break;
			case 'p': action[3] = true; opted = true; break;
			case 'c': action[4] = true; opted = true; break;
			case 'S': action[6] = true; set[0] = optarg; opted = true; seted = true; break;
			case '?': showusage(); return 0; break;
			default: printf("Default\n");
		};
	};
	if (not opted) {
		showusage();
		return 0;
	}
	// 2. read file
	// 2.1. open
	if (! (fp=fopen(argv[argc - 1],"rb")))
		err(-1, "Error opening input file for reading");
	// 2.2. get file size
	fseek(fp, 0L, SEEK_END);
	fsize = ftell(fp);
	rewind(fp);
	// 2.3. make buffer
	buffer = (char *) malloc(fsize);
	if (buffer == NULL)
		err(-2, "Error allocating memory for buffer");
	// 2.4. read and close
	if (fread(buffer, sizeof(char), fsize, fp) != fsize)
		err(-3, "Error reading file");
	fclose(fp);
	// 3. decode file
	for (unsigned int i=0; i < fsize; i++) { buffer[i] ^= key[i % 36]; }
	if (action[5])
		printf("%s\n", buffer);
	// 4. prepare regex
	reti = regcomp(&regex, mask, 0);
	if( reti )
		err(-4, "Error compiling regex");
	// 5. split on parts
	reti = regexec(&regex, buffer, 6, match, 0);
	if (reti)
		err(-5, "Error matching regex");
	for (int i = 0; i < 5; i++) {
		buffer[match[i+1].rm_eo] = '\0';	// set EOL
		term[i] = &buffer[match[i+1].rm_so];	// set term
	// 6. show values
		if (action[i]) {
			if (showed)
				fprintf(stdout, "%s%s", delimiter, term[i]);
			else {
				fprintf(stdout, "%s", term[i]);
				showed = true;
			}
		}
	}
	if (showed)
		fprintf(stdout, "\n");
	// 7. set values
	if (seted) {
		// 7.1. set values, calc new size
		fsize = 63;
		for (int i = 0; i < 5; i++) {
			if (action[6+i])
				term[i] = set[i];
				fsize += strlen(term[i]);
			
		}
		// 7.2. make buffer
		outbuffer = (char *) malloc(fsize);
		if (outbuffer == NULL)
			err(-6, "Error allocating memory for out buffer");
		// 7.3. make new string
		sprintf(outbuffer, outmask, term[0], term[1], term[2], term[3], term[4]);
		// 7.4. crypt'm
		for (unsigned int i=0; i < fsize; i++) { outbuffer[i] ^= key[i % 36]; }
		// 7.5. open file
		if (! (fp=fopen(argv[argc - 1],"wb")))
			err(-7, "Error opening output file for reading");
		// 7.6. write
		if (fwrite(outbuffer, sizeof(char), fsize, fp) != fsize)
			err(-8, "Error writing file");
		fclose(fp);
		free(outbuffer);
	}
	// x. the end
	free(buffer);
	return 0;
}
