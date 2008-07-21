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

#ifndef		_NSK_H
#define		_NSK_H

#include	"mytypes.h"
#include	<time.h>

// 0. simple types
typedef		DWORD	ID;
typedef		WORD	CRC;

class	Pkg {
	public:
		void	print(void);
		BYTE	Sign;
		BYTE	SAddr;
		BYTE	Cmd;
		CRC	Crc;
};

class	Query : public Pkg {
	public:
			Query(void) {};
		void	print(void);
		void	serialize(BYTE *);
};

class	Query0 : public Query {
	public:
			Query0(void) { Cmd = 0; }
		void	serialize(BYTE *);
};

class	Query1 : public Query {
	public:
			Query1(void) : Id(0), Access(0), WGfxI(0), WGfxO(0), Bio(0), Slave(0) { Cmd = 1; }
		void	serialize(BYTE *);
		ID	Id;
		BYTE	Access;
		BYTE	WGfxI;	// #1
		BYTE	WGfxO;	// #1
		BYTE	Bio;	// #1
		ID	Slave;	// #2
};

class	Query2 : public Query {
	public:
			Query2(void) : Id(0) { Cmd = 2; }
		void	serialize(BYTE *);
		ID	Id;
};

class	Query6 : public Query {
	public:
			Query6(void) { Cmd = 6; }
		void	serialize(BYTE *);
		void	settime(const tm &);
		tm	DateTime;
};

class	Reply : public Pkg {
	public:
			Reply(void) : MAddr(0), CmdState(0) {}
		int	unserialize(const BYTE *);
		void	print(void);
		BYTE	MAddr;
		bool	CmdState;
};

class	Reply0 : public Reply {
	public:
			Reply0(void) : Events(0), Code(0), Id(0), Head(0), SS_State(0), EE_State(0) {}
		int	unserialize(const BYTE *);
		void	print(void);
		const tm	&gettime(void) {return DateTime;};
		BYTE	Events;
		tm	DateTime;
		BYTE	Code;		// #1
		ID	Id;		// #1
		WORD	Head;		// #2
		BYTE	SS_State;
		BYTE	EE_State;
};

class	Reply1 : public Reply {
	public:
			Reply1(void) : Id(0), Access(0), WGfxI(0), WGfxO(0), Bio(0), Qty(0), ErrCode(0) {}
		int	unserialize(const BYTE *);
		void	print(void);
		ID	Id;
		BYTE	Access;
		BYTE	WGfxI;	// #1
		BYTE	WGfxO;	// #1
		BYTE	Bio;	// #1
//		ID	Slave;	// #2
		BYTE	Qty;
		BYTE	ErrCode;
};

class	Reply2 : public Reply {
	public:
			Reply2(void) : Id(0), ErrCode(0), IdQty(0) {}
		int	unserialize(const BYTE *);
		void	print(void);
		ID	Id;
		BYTE	ErrCode;
		WORD	IdQty;
};

class	Reply6 : public Reply {
	public:
			Reply6(void) : Ctrl(0), dummy0(0) {}
		int	unserialize(const BYTE *);
		void	print(void);
		const tm	&gettime(void) {return DateTime;};
		tm	DateTime;
		WORD	Ctrl;
		BYTE	dummy0;
};

WORD	Crc16(BYTE *, WORD);

#endif
