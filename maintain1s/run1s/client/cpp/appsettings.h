/*
Copyright 2009 Eugene A. Pivnev

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
version 2 as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
*/

#ifndef APPSETTINGS_H
#define APPSETTINGS_H

#include <QString>

#include "settings.h"

class AppSettings : public Settings
{
public:
	static QString getServer(void);	// ? QURL
	static QString getLogin(void);
	static QString getPassword(void);
	static QString getPath1C(void);
	static bool getMinOnRun(void);	// minimize on running 1C
	static bool getTrayEnabled(void);
	static bool getStartHidden(void);
	static bool getMinToTray(void);
	static void setServer(const QString&);	// ? QURL
	static void setLogin(const QString&);
	static void setPassword(const QString&);
	static void setPath1C(const QString&);
	static void setMinOnRun(const bool);
	static void setTrayEnabled(const bool);
	static void setStartHidden(const bool);
	static void setMinToTray(const bool);
};

#endif // APPSETTINGS_H
