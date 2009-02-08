#include "appinfo.h"

#include <QtCore/QCoreApplication>

void AppInfo::setQCore(void) {
	QCoreApplication::setApplicationName(getAppName());
	QCoreApplication::setApplicationVersion(getAppVersion());
	QCoreApplication::setOrganizationDomain(getOrgDomain());
	QCoreApplication::setOrganizationName(getAuthorName());
}
