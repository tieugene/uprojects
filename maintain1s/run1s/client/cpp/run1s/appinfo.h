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

#ifndef APPINFO_H
#define APPINFO_H

#include <QString>

class AppInfo
{
public:
	static QString getAppName() { return "Run1s"; }
	static QString getAppVersion() { return "0.2"; }
	static QString getAppRelease() { return "0"; }
	static QString getOrgDomain() { return "eap.su"; }
	static QString getAuthorName() { return "TI_Eugene"; }
	static QString getAuthorEMail() { return "ti.eugene@gmail.com"; }
	static void setQCore(void);
};

#endif // APPINFO_H
