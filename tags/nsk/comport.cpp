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
#include <unistd.h>
#include <termios.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/signal.h>
#include <sys/types.h>

#include "comport.h"

static struct termios oldtio;			//place for old and new port settings for serial port

int	set_comport(void (*sh) (int)) {
	char *device	= "/dev/ttyS1";
	struct termios newtio;
	struct sigaction saio;               //definition of signal action

	//open the device(com port) to be non-blocking (read will return immediately)
	int f = open ( device, O_RDWR | O_NOCTTY | O_NONBLOCK );
	if ( f < 0 )
	{
		perror ( device );
		return ( -1 );
	}
	//install the serial handler before making the device asynchronous
	saio.sa_handler = sh;
	sigemptyset ( &saio.sa_mask );   //saio.sa_mask = 0;
	saio.sa_flags = 0;
	saio.sa_restorer = NULL;
	sigaction ( SIGIO, &saio, NULL );

	fcntl ( f, F_SETOWN, getpid() );	// allow the process to receive SIGIO
	fcntl ( f, F_SETFL, FASYNC );		// Make the file descriptor asynchronous (the manual page says only O_APPEND and O_NONBLOCK, will work with F_SETFL...)

	tcgetattr ( f, &oldtio );		// save current port settings
	// set new port settings for canonical input processing
	newtio.c_cflag = B57600 | CS8 | CSTOPB | CREAD;
	newtio.c_iflag = IGNPAR;
	newtio.c_oflag = 0;
	newtio.c_lflag = 0;       //ICANON;
	newtio.c_cc[VMIN] = 1;
	newtio.c_cc[VTIME] = 0;
	tcflush ( f, TCIFLUSH );
	tcsetattr ( f, TCSANOW, &newtio );
	return f;
}

void	reset_comport(int f) {
	tcsetattr ( f, TCSANOW, &oldtio );
	close ( f );
}

