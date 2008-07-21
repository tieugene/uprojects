/***************************************************************************
 *   Copyright (C) 2008 by Eugene A. Pivnev   *
 *   eugene@rgsg.ru   *
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

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <time.h>
#include <sys/types.h>


#include "mytypes.h"
#include "utility.h"

int	usage(const char *s, const char *e) {
	printf("%s\nUsage: %s <addr> <cmd> [id]\n\
	addr\t1..254\tAddress of slave controller.\n\
	cmd\t0|1|2|6\tController command.\n\
	id\tlong\tKey ID to add/delete.\n", e, s);
	return 1;
}

int     parseopts(int argc, const char *argv[], OPTS &opts) {
	if ((argc < 3) || (argc > 4))
		return usage(argv[0], "Wrong number of arguments." );
	// 1. addr
	opts.saddr = atoi(argv[1]);
	if ((opts.saddr < 1) || (opts.saddr > 254))
		return usage(argv[0], "Wrong slave address." );
	// 2. func
	if ((strlen(argv[2]) != 1) || (strchr("0126", (argv[2][0])) == NULL))
		return usage(argv[0], "Wrong functions value." );
	opts.func = argv[2][0] - '0';
	// 3. id
	if ((opts.func == 1) || (opts.func == 2)) {
		if (argc != 4)
			return usage(argv[0], "You must specify key ID." );
		else {
			sscanf(argv[3], "%08X", &opts.id);
			if (opts.id < 1)
				return usage( argv[0], "Wrong key ID." );
		}
	}
	return 0;
}

void	prn (const char *s, BYTE *ptr) {
	fprintf(stderr, "%s:", s);
	for (int i = 0; i < 16; i++)
		fprintf(stderr, " %02X", *ptr++);
	fprintf(stderr, "\n");
}

int	force_usleep(int msec) {
	timespec timer, remind;
	int retvalue = 0;

	timer.tv_sec = 0;
	timer.tv_nsec = msec * 1000000L;
	remind.tv_sec = 0;
	remind.tv_nsec = 0;
	while ((retvalue = nanosleep(&timer, &remind))) {
		if (errno != EINTR) {
			retvalue = 1;
			break;
		}
		timer = remind;
	}
	return retvalue;
}

void	cleanptr(BYTE *ptr, int c) { memset(ptr, '\0', c); }
