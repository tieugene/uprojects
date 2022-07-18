#include <QCoreApplication>
#include <QLibraryInfo>
#ifndef HAVE_QT5
#include <QDesktopServices>
#define LIqty 11
#define PATHSqty 11
#else
#define LIqty 14
#define PATHSqty 20
#include <QStandardPaths>
#endif

#include <string>
#include <iostream>

typedef struct {
        QLibraryInfo::LibraryLocation e;
        std::string s;
} QLI;

typedef struct {
#ifndef HAVE_QT5
        QDesktopServices::StandardLocation e;
#else
        QStandardPaths::StandardLocation e;
#endif
        std::string s;
} QPATHS;

static QLI qli[] = {
        { QLibraryInfo::PrefixPath, "QLibraryInfo::PrefixPath"},
        { QLibraryInfo::DocumentationPath, "QLibraryInfo::DocumentationPath"},
        { QLibraryInfo::HeadersPath, "QLibraryInfo::HeadersPath"},
        { QLibraryInfo::LibrariesPath, "QLibraryInfo::LibrariesPath"},
        { QLibraryInfo::BinariesPath, "QLibraryInfo::BinariesPath"},
        { QLibraryInfo::PluginsPath, "QLibraryInfo::PluginsPath"},
        { QLibraryInfo::DataPath, "QLibraryInfo::DataPath"},
        { QLibraryInfo::TranslationsPath, "QLibraryInfo::TranslationsPath"},
        { QLibraryInfo::SettingsPath, "QLibraryInfo::SettingsPath"},
        { QLibraryInfo::ExamplesPath, "QLibraryInfo::ExamplesPath"},
        { QLibraryInfo::ImportsPath, "QLibraryInfo::ImportsPath"},
#ifndef HAVE_QT5
        { QLibraryInfo::DemosPath, "QLibraryInfo::DemosPath"},
#else
        { QLibraryInfo::Qml2ImportsPath, "QLibraryInfo::Qml2ImportsPath"},
        { QLibraryInfo::ArchDataPath, "QLibraryInfo::ArchDataPath"},
        { QLibraryInfo::LibraryExecutablesPath, "QLibraryInfo::LibraryExecutablesPath"},
        { QLibraryInfo::TestsPath, "QLibraryInfo::TestsPath"}
#endif
};

static QPATHS qpaths[] {
#ifndef HAVE_QT5
        { QDesktopServices::DesktopLocation, "QDesktopServices::DesktopLocation"},
        { QDesktopServices::DocumentsLocation, "QDesktopServices::DocumentsLocation"},
        { QDesktopServices::FontsLocation, "QDesktopServices::FontsLocation"},
        { QDesktopServices::ApplicationsLocation, "QDesktopServices::ApplicationsLocation"},
        { QDesktopServices::MusicLocation, "QDesktopServices::MusicLocation"},
        { QDesktopServices::MoviesLocation, "QDesktopServices::MoviesLocation"},
        { QDesktopServices::PicturesLocation, "QDesktopServices::PicturesLocation"},
        { QDesktopServices::TempLocation, "QDesktopServices::TempLocation"},
        { QDesktopServices::HomeLocation, "QDesktopServices::HomeLocation"},
        { QDesktopServices::DataLocation, "QDesktopServices::DataLocation"},
        { QDesktopServices::CacheLocation, "QDesktopServices::CacheLocation"}
#else
        { QStandardPaths::DesktopLocation, "QStandardPaths::DesktopLocation"},
        { QStandardPaths::DocumentsLocation, "QStandardPaths::DocumentsLocation"},
        { QStandardPaths::FontsLocation, "QStandardPaths::FontsLocation"},
        { QStandardPaths::ApplicationsLocation, "QStandardPaths::ApplicationsLocation"},
        { QStandardPaths::MusicLocation, "QStandardPaths::MusicLocation"},
        { QStandardPaths::MoviesLocation, "QStandardPaths::MoviesLocation"},
        { QStandardPaths::PicturesLocation, "QStandardPaths::PicturesLocation"},
        { QStandardPaths::TempLocation, "QStandardPaths::TempLocation"},
        { QStandardPaths::HomeLocation, "QStandardPaths::HomeLocation"},
        { QStandardPaths::DataLocation, "QStandardPaths::DataLocation"},
        { QStandardPaths::CacheLocation, "QStandardPaths::CacheLocation"},
	// +qt5
        { QStandardPaths::GenericCacheLocation, "QStandardPaths::GenericCacheLocation"},
        { QStandardPaths::GenericDataLocation, "QStandardPaths::GenericDataLocation"},
        { QStandardPaths::RuntimeLocation, "QStandardPaths::RuntimeLocation"},
        { QStandardPaths::ConfigLocation, "QStandardPaths::ConfigLocation"},
        { QStandardPaths::DownloadLocation, "QStandardPaths::DownloadLocation"},
        { QStandardPaths::GenericConfigLocation, "QStandardPaths::GenericConfigLocation"},
        { QStandardPaths::AppDataLocation, "QStandardPaths::AppDataLocation"},
        { QStandardPaths::AppLocalDataLocation, "QStandardPaths::AppLocalDataLocation"},
        { QStandardPaths::AppConfigLocation, "QStandardPaths::AppConfigLocation"},
#endif
};

int main(int argc, char *argv[])
{
        QCoreApplication a(argc, argv);
        // 0. set app
        QCoreApplication::setApplicationName("QtInfo");
        QCoreApplication::setApplicationVersion("0.0.1");
        QCoreApplication::setOrganizationDomain("QtDesktop");
        QCoreApplication::setOrganizationName("TI_Eugene");
        // 1. QLibraryInfo
        for (unsigned int i = 0; i < LIqty; i++)
                std::cout << qli[i].s << ": " << QLibraryInfo::location(qli[i].e).toStdString() << std::endl;
        // 2. QDesktopServices/QStandardPaths
        for (unsigned int i = 0; i < PATHSqty; i++)
#ifndef HAVE_QT5
                std::cout << qpaths[i].s << ": " << QDesktopServices::storageLocation(qpaths[i].e).toStdString() << std::endl;
#else
                std::cout << qpaths[i].s << ": " << QStandardPaths::writableLocation(qpaths[i].e).toStdString() << std::endl;
#endif
}
// qt-devel / qt5-qtbase-devel
