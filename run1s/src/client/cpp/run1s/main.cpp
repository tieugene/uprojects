/*
TODO:
* icons
* translations
* tune http
* systray (QSystemTrayIcon)
* Win
* use QStyle::StandardPixmap
*/

#include <QtCore/QTranslator>
#include <QtCore/QLocale>
#include <QtCore/QLibraryInfo>
#include <QtGui/QApplication>

#include "mainwindow.h"
#include "appinfo.h"
#include "settings.h"

int main(int argc, char *argv[])
{
	QApplication a(argc, argv);

	// Translation
	QTranslator appTranslator;
	printf("%s\n", QLibraryInfo::location(QLibraryInfo::TranslationsPath)); 
	appTranslator.load("l10n/juffed_" + QLocale::system().name().left(2));
	a.installTranslator(&appTranslator);

	AppInfo::setQCore();
	Settings::read();
	MainWindow w;
	w.show();
	w.Update();	// FIXME:
	return a.exec();
}
