/*
TODO:
* tune http
* Win
In Process:
* icons
* translations
* systray (QSystemTrayIcon) 
*/

#include <QTranslator>
#include <QLocale>
#include <QLibraryInfo>
#include <QApplication>
#include <QMessageBox>

#include "mainwindow.h"
#include "appinfo.h"
#include "settings.h"

int main(int argc, char *argv[])
{
	QApplication a(argc, argv);

	// Translation: /usr/share/qt4/translations
	QTranslator appTranslator;
	QString trpath = QLibraryInfo::location(QLibraryInfo::TranslationsPath);
	appTranslator.load("l10n/run1s_" + QLocale::system().name().left(2));
	a.installTranslator(&appTranslator);

	AppInfo::setQCore();
	Settings::read();
	MainWindow w;
	w.show();
	w.slUpdate();	// FIXME:
	return a.exec();
}
