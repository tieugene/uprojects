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

#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <errno.h>
#include <sys/signal.h>
#include <sys/types.h>

#include "mytypes.h"
#include "nsk.h"
#include "comport.h"
#include "utility.h"

void		signal_handler_IO ( int );
int		query(int);
int		Ask0(BYTE, Reply0 &);
int		Ask1(BYTE, DWORD, Reply1 &);
int		Ask2(BYTE, DWORD, Reply2 &);
int		Ask6(BYTE, const tm &, tm &);

int		need_data = FALSE, fd;
BYTE		*replyptr, *Tx, *Rx, *Dummy;
static OPTS	opts;

int	main ( int argc, const char *argv[] )
{
	int res, i, error, status;
	time_t timer = time(NULL);

	opts.verbose = TRUE;
	if (parseopts(argc, argv, opts))
		exit(0);
	if (opts.verbose)
		fprintf( stderr, "#%s", ctime(&timer) );
	// 0. comport init
	if ((fd = set_comport(signal_handler_IO)) >= 0) {
	// 1. ask 0 func
		Tx = new BYTE[2048];
		Rx = new BYTE[2048];
		Dummy = new BYTE[2048];
		Reply0 r0;
		Reply1 r1;
		Reply2 r2;
		time_t timer;
		tm *lt, newtime;
		switch (opts.func) {
			case 0:
				Ask0(opts.saddr, r0);
				break;
			case 1:
				Ask1(opts.saddr, opts.id, r1);
				r1.print();
				break;
			case 2:
				Ask2(opts.saddr, opts.id, r2);
				r2.print();
				break;
			case 6:
				timer = time(NULL);
				lt = localtime(&timer);
				Ask6(opts.saddr, *lt, newtime);
				break;
			default:
				break;
		}
		reset_comport(fd);
	}
	return 0;
}

void signal_handler_IO ( int status ) {
//printf("SH start: %d\n", status);
	if (need_data) {
		int cursize = Rx + 2048 - replyptr;
		int res = read ( fd, replyptr, cursize );
//printf("cursize=%d, read=%d, ptr=%d\n", cursize, res, replyptr - Rx);
		if ( res > 0 ) {
//printf("Rx :");
//for ( int i = 0; i < res; i++ )
//	printf ( " %02X", replyptr[i] );
//puts("");
			replyptr += res;
		}
	} else {
		printf("Dummy=%d\n", read ( fd, &Dummy, sizeof(Dummy) ));
	}
//	puts("SH end");
}

int	query(int f) {
// TODO: retry
// TODO: busy
// 
	int retvalue = 0;
	// 2. set enable flag for reader
	if (opts.verbose)
		prn("> ", Tx);
	need_data = TRUE;
	replyptr = Rx;
	cleanptr(Rx, 16);
	// 3. put data
	write(f, Tx, 16);
	// 4. wait
	retvalue = force_usleep(100);
	need_data = FALSE;
	if (opts.verbose)
		prn("< ", Rx);
	if (retvalue) {
		fprintf(stderr, "Error of timer\n");
		return retvalue;
	}
	if ((replyptr - Rx) != 16) {
		fprintf(stderr, "Bad Rx size");
		return 1;
	}
	if (Rx[0] != 0xD6) {
		fprintf(stderr, "Bad header: %02X\n", Rx[0]);
		return 2;
	}
	WORD crctmp = Crc16(Rx + 1, 13);
	WORD crc1 = (crctmp << 8) | (crctmp >> 8), crc0 = (Rx[14] << 8) | Rx[15];
	if (crc1 != crc0) {
		fprintf(stderr, "Bad CRC: must %04X, is %04X\n", crc1, crc0);
		return 3;
	}
	return retvalue;
}

int	Ask0(BYTE addr, Reply0 &r) {
	Query0 q;
	q.SAddr = addr;
	q.serialize(Tx);
	int retvalue = 0, counter = 0;
	do {
		if (query(fd)) {
			retvalue = 1;
			break;
		} else {
			r.unserialize(Rx);
			if (r.Events) {
				fprintf(stdout, "%04d/%02d/%02d %02d:%02d:%02d %08X %02X %02X %02X\n",
					2008, r.DateTime.tm_mon, r.DateTime.tm_mday,
					r.DateTime.tm_hour, r.DateTime.tm_min, r.DateTime.tm_sec,
					r.Id,
					r.Code,
					r.SS_State,
					r.EE_State
					
				);	// date time id evt SS EE
				counter++;
			} else {
				fprintf(stderr, "%d event read\n", counter);
				r.print();
			}
		}
	} while (r.Events);
	return retvalue;
}

int	Ask1(BYTE addr, DWORD id, Reply1 &r) {
	Query1 q;
	q.SAddr = addr;
	q.Id = id;
	q.Access = q.WGfxI = q.WGfxO = q.Bio = '\0';
	q.serialize(Tx);
	int retvalue = 0;
	if (query(fd)) {
		retvalue = 1;
	} else
		r.unserialize(Rx);
	return retvalue;
}

int	Ask2(BYTE addr, DWORD id, Reply2 &r) {
	Query2 q;
	q.SAddr = addr;
	q.Id = id;
	q.serialize(Tx);
	int retvalue = 0;
	if (query(fd)) {
		retvalue = 1;
	} else
		r.unserialize(Rx);
	return retvalue;
}

int	Ask6(BYTE addr, const tm &set, tm &result) {
	Query6 q;
	Reply6 r;
	q.SAddr = addr;
	q.settime(set);
	q.serialize(Tx);
	int retvalue = 0;
	if (query(fd)) {
		retvalue = 1;
	} else
		r.unserialize(Rx);
	return retvalue;
	r.print();
	fprintf(stderr, "%s", asctime(&r.gettime()));
	return 0;
}
