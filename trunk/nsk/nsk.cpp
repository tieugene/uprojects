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
#include <time.h>
#include <sys/types.h>
#include "mytypes.h"
#include "nsk.h"

WORD	Crc16(BYTE *pcBlock, WORD len) {
	WORD crc = 0xFFFF;

	while (len--) {
		BYTE temp = BYTE(crc) ^ *pcBlock++;
		for(BYTE i = 0; i < 8; i++) {
			if( temp & 1 )
				crc ^= 0xA001;
			crc = crc & 1 ? (crc >> 1) | 0x8000 : crc >> 1;
			temp >>= 1;
		}
	}
	return (crc << 8) | (crc >> 8);
}

void	Query::print(void) {
	fprintf(stderr, "Query:\nSAddr:\t%02X\nCmd:\t%02X\nCRC:\t%04X", SAddr, Cmd, Crc);
}

void	Query::serialize(BYTE *ptr) {
	ptr[0]	= '\xA5';
	ptr[1]	= SAddr;
	ptr[2]	= Cmd;
	Crc	= Crc16(ptr + 1, 13);
	ptr[14]	= Crc & 0xFF;
	ptr[15]	= Crc >> 8;
}

void	Query0::serialize(BYTE *ptr) {
	for (int i = 3; i <= 13; i++)
		ptr[i] = '\0';
	Query::serialize(ptr);
}

void	Query1::serialize(BYTE *ptr) {
	ptr[3]	= BYTE(Id >> 24);
	ptr[4]	= BYTE(Id >> 16);
	ptr[5]	= BYTE(Id >> 8);
	ptr[6]	= BYTE(Id);
	ptr[7]	= Access;
	ptr[8]	= WGfxI;
	ptr[9]	= WGfxO;
	ptr[10]	= Bio;
	ptr[11]	= ptr[12] = ptr[13] = '\0';
	Query::serialize(ptr);
}

void	Query2::serialize(BYTE *ptr) {
	ptr[3]	= BYTE(Id >> 24);
	ptr[4]	= BYTE(Id >> 16);
	ptr[5]	= BYTE(Id >> 8);
	ptr[6]	= BYTE(Id);
	for (int i = 7; i <= 13; i++)
		ptr[i] = '\0';
	Query::serialize(ptr);
}

void	Query6::serialize(BYTE *ptr) {
	ptr[3]	= DateTime.tm_sec;
	ptr[4]	= DateTime.tm_min;
	ptr[5]	= DateTime.tm_hour;
	ptr[6]	= DateTime.tm_wday;
	ptr[7]	= DateTime.tm_mday;
	ptr[8]	= DateTime.tm_mon + 1;
	ptr[9]	= DateTime.tm_year - 100;
	Query::serialize(ptr);
}

void	Query6::settime(const tm &t) {
	DateTime.tm_sec		= t.tm_sec;
	DateTime.tm_min		= t.tm_min;
	DateTime.tm_hour	= t.tm_hour;
	DateTime.tm_wday	= t.tm_wday;
	DateTime.tm_mday	= t.tm_mday;
	DateTime.tm_mon		= t.tm_mon;
	DateTime.tm_year	= t.tm_year;
	fprintf(stderr, "%d, %s", t.tm_year, asctime(&DateTime));
}

int	Reply::unserialize(const BYTE *ptr) {
	// TODO: check signature
	Sign		= ptr[0];
	MAddr		= ptr[1];
	SAddr		= ptr[2];
	Cmd		= ptr[3] & 0x7;
	CmdState	= ptr[3] & 0x8;
	Crc		= (ptr[14] << 8) | ptr[15];
	return 0;
}

void	Reply::print(void) {
	fprintf(stderr, "Reply:\nSign:\t%02X\nMAddr:\t%02X\nSAddr:\t%02X\nCmd:\t%02X\nCmdSt:\t%02X\nCRC:\t%04X\n", Sign, MAddr, SAddr, Cmd, CmdState, Crc);
}

int	Reply0::unserialize(const BYTE *ptr) {
	static union {
		BYTE	raw[3];
		struct	{	// Reply Time Stamp (3 bytes)
			unsigned int	mon:2;
			unsigned int	day:5;
			unsigned int	hour:5;
			unsigned int	min:6;
			unsigned int	sec:6;
			} fmt;
		} cvt;

	Reply::unserialize(ptr);
	Events		= ptr[3] >> 4;
	if (Events) {	// events
		Code			= ptr[4];
/*		cvt.raw[0]		= ptr[5];
		cvt.raw[1]		= ptr[6];
		cvt.raw[0]		= ptr[7];
		DateTime.tm_sec		= cvt.fmt.sec;
		DateTime.tm_min		= cvt.fmt.min;
		DateTime.tm_hour	= cvt.fmt.hour;
		DateTime.tm_mday	= cvt.fmt.day;
		DateTime.tm_mon		= cvt.fmt.mon;*/
		DateTime.tm_year	= 0;
		DateTime.tm_mon		= ptr[5] >> 6;
		DateTime.tm_mday	= (ptr[5] >> 1) & 0x1F;
		DateTime.tm_hour	= ((ptr[5] << 4) | (ptr[6] >> 4)) & 0x1F;
		DateTime.tm_min		= ((ptr[6] << 2) | (ptr[7] >> 6)) & 0x3F;
		DateTime.tm_sec		= ptr[7] & 0x3F;
		Id			= (DWORD(ptr[8]) << 24) | (DWORD(ptr[9]) << 16) | (DWORD(ptr[10]) << 8) | ptr[11];
	} else {	// empty
		DateTime.tm_sec		= ptr[4];
		DateTime.tm_min		= ptr[5];
		DateTime.tm_hour	= ptr[6];
		DateTime.tm_mday	= ptr[7];
		DateTime.tm_mon		= ptr[8] - 1;
		DateTime.tm_year	= ptr[9] + 100;
		Head	= (ptr[10] << 8) | ptr[11];
	}
	SS_State	= ptr[12];
	EE_State	= ptr[13];
	return 0;
}

void	Reply0::print(void) {
	Reply::print();
	fprintf(stderr, "Events:\t%02X\n", Events);
	if (Events)	// events
		fprintf(stderr, "Event:\t%02X\nDate:\t%02d/%02d %02d:%02d:%02d\nID:\t%08X\n", Code, DateTime.tm_mday, DateTime.tm_mon + 1, DateTime.tm_hour, DateTime.tm_min, DateTime.tm_sec, Id);
	else	// empty
		fprintf(stderr, "Date:\t%02d/%02d/%02d %02d:%02d:%02d\nHead:\t%04X\n", DateTime.tm_mday, DateTime.tm_mon + 1, DateTime.tm_year - 100, DateTime.tm_hour, DateTime.tm_min, DateTime.tm_sec, Head);
	fprintf(stderr, "SS:\t%02X\nEE:\t%02X\n", SS_State, EE_State);
}

int	Reply1::unserialize(const BYTE *ptr) {
	// TODO: handle error
	Reply::unserialize(ptr);
	Id		= (DWORD(ptr[4]) << 24) | (DWORD(ptr[5]) << 16) | (DWORD(ptr[6]) << 8) | ptr[7];
	Access		= ptr[8];
	WGfxI		= ptr[9];
	WGfxO		= ptr[10];
	Bio		= ptr[11];
	Qty		= ptr[12];
	return 0;
}

void	Reply1::print(void) {
	Reply::print();
	fprintf(stderr, "ID:\t%08X\nAccess:\t%02X\nWGfxI:\t%02X\nWGfxO:\t%02X\nBio:\t%02X\nQty:\t%02X\n", Id, Access, WGfxI, WGfxO, Bio, Qty);
}

int	Reply2::unserialize(const BYTE *ptr) {
	// TODO: handle error
	Reply::unserialize(ptr);
	Id		= (DWORD(ptr[4]) << 24) | (DWORD(ptr[5]) << 16) | (DWORD(ptr[6]) << 8) | ptr[7];
	ErrCode		= ptr[8];
	IdQty		= (WORD(ptr[12]) << 8) | ptr[13];
	return 0;
}

void	Reply2::print(void) {
	Reply::print();
	fprintf(stderr, "ID:\t%08X\nErrCode:\t%02X\nIdQty:\t%04X\n", Id, ErrCode, IdQty);
}

int	Reply6::unserialize(const BYTE *ptr) {
	Reply::unserialize(ptr);
	DateTime.tm_sec		= ptr[4];
	DateTime.tm_min		= ptr[5];
	DateTime.tm_hour	= ptr[6];
	DateTime.tm_mday	= ptr[7];
	DateTime.tm_wday	= ptr[8];
	DateTime.tm_mon		= ptr[9] - 1;
	DateTime.tm_year	= ptr[10] + 100;
	Ctrl	= (ptr[11] << 8) | ptr[12];
	dummy0	= ptr[13];
	return 0;
}

void	Reply6::print(void) {
	Reply::print();
	fprintf(stderr, "Date:\t%02d/%02d/%02d (%d) %02d:%02d:%02d\nCtrl:\t%04X\n", DateTime.tm_mday, DateTime.tm_mon + 1, DateTime.tm_year - 100, DateTime.tm_wday, DateTime.tm_hour, DateTime.tm_min, DateTime.tm_sec, Ctrl);
}
