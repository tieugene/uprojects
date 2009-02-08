#ifndef APPSETTINGS_H
#define APPSETTINGS_H

#include <QtCore/QString>

#include "settings.h"

class AppSettings : public Settings
{
public:
	static QString getServer(void);	// ? QURL
	static QString getLogin(void);
	static QString getPassword(void);
	static QString getPath1C(void);
	static bool getMinOnRun(void);
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
