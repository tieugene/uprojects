/***************************************************************************
 *   Copyright (C) 2007 by Eugene A. Pivnev   *
 *   ti.eugene@gmail.com   *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program; if not, write to the                         *
 *   Free Software Foundation, Inc.,                                       *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
 ***************************************************************************/


#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <string.h>

static	char	retvalue[17], *defaultpath = "INFO.DAT";

int	AskInfoDat(const char *path, const long index)	{
	/*
	@param index - searched index
	
	@return - word found
	*/
	static int	mask[16] = {23,1,24,10,22,4,6,9,14,24,11,13,15,1,22,3};
	unsigned char	block[16];
	FILE		*infodat;
	int		i, val, special, r;

	// prepare
	if (!(infodat = fopen(path, "rb")))
		return (1);
	fseek(infodat, 0L, SEEK_END);		// check
	special = ftell(infodat) / 1000 + 1;	// check
	// main
	fseek(infodat, index, SEEK_SET);	// check
	if(fread(block, 16, 1, infodat) == 1)	{
		for(i = 0; i < 16; i++)
		{
			if (i==1)
				val = block[0] + special;
			else
				val = block[i] + mask[i];
			retvalue[i] = (char) (((val - 1) % 26) + 'A');
		};
		r = 0;
	} else {
		r = 5;
	}
	fclose(infodat);
	retvalue[16] = '\0';
	return (r);
}

int main(int argc, char *argv[])	{
	int	r;
	long	key = 1;
	char	*path;
	bool	askmode = false;

	// 1. check syntax
	if ((argc < 2) || (argc > 3)) {
		fprintf(stderr, "Usage:\n"
				"%s [full path of info.dat] <key> | -v\n"
				"\t<key> - numeric key >0 to find word for\n"
				"\t-v - ask ITS disk \"number\"\n", argv[0]);
		exit(EXIT_FAILURE);
	}
	// 2. prepare data
	// 2.1. path to info.dat
	if (argc == 2)
		path = defaultpath;
	else
		path = argv[1];
	// 2.2. last argument
	if (strcmp(argv[argc-1], "-v") == 0) {
		key = 1;
		askmode = true;
	} else {
		key = atol(argv[argc-1]);
		askmode = false;
		if (key <= 0) {
			fprintf(stderr, "Last argument is not -v nor key\n");
			exit(EXIT_FAILURE);
		}
	}
	if ((r = AskInfoDat(path, key)))	{
		fprintf(stderr, "Can't read Info.dat\n");
		exit(EXIT_FAILURE);
	}
	// post - 
	if (askmode)
		fprintf(stdout, "%d", (retvalue[1] + 26 - retvalue[0]) % 26);
	else
		fprintf(stdout, "%s", retvalue);
	exit(EXIT_SUCCESS);
}
