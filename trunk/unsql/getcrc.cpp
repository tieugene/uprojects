// getcrc.cpp
// calculate "crc" on given file (just sum of 4-byte integers
// unsql.cpp version 0.0.1

#include <stdio.h>
#include <stdint.h>

int	main ( int argc, const char *argv[] )
{
        FILE		*fp;
	uint32_t	buffer, crc = 0;

	if ( argc != 2 ) {
		printf("Usage: %s infile\n", argv[0]);
		return -1;
	}
	if (! (fp=fopen(argv[1],"rb"))) {
    		printf("Cannot open input file %s for reading", argv[1]);
		return -2;
	}
	while (fread(&buffer, sizeof(uint32_t), 1, fp) == 1)
		crc += buffer;
	fclose(fp);
	printf("%08x\n", crc);
	return 0;
}
