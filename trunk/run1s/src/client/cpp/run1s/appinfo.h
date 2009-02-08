#ifndef APPINFO_H
#define APPINFO_H

#include <QtCore/QCoreApplication>
#include <QtCore/QString>

class AppInfo
{
public:
	static QString getAppName() { return "Run1s"; }
	static QString getAppVersion() { return "0.1"; }
	static QString getAppRelease() { return "0"; }
	static QString getOrgDomain() { return "eap.su"; }
	static QString getAuthorName() { return "TI_Eugene"; }
	static QString getAuthorEMail() { return "ti.eugene@gmail.com"; }
	static void setQCore(void);
};

#endif // APPINFO_H
