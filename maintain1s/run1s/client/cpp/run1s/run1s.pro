TEMPLATE = app
TARGET =
DEPENDPATH += . translations
INCLUDEPATH += .
HEADERS += aboutdialog.h \
 appinfo.h \
 appsettings.h \
 mainwindow.h \
 settings.h \
 settingsdialog.h \
 dsingleapplication.h
FORMS += ui/aboutdialog.ui ui/mainwindow.ui ui/settingsdialog.ui
SOURCES += aboutdialog.cpp \
 appinfo.cpp \
 appsettings.cpp \
 main.cpp \
 mainwindow.cpp \
 settings.cpp \
 settingsdialog.cpp \
 dsingleapplication.cpp
TRANSLATIONS += translations/run1s_ru.ts
QT += core network gui xml
CONFIG += warn_on
RESOURCES += run1s.qrc
VERSION = 0.0.1
