TEMPLATE = app
TARGET =
DEPENDPATH += . l10n qtc-gdbmacros
INCLUDEPATH += .
HEADERS += aboutdialog.h \
 appinfo.h \
 appsettings.h \
 mainwindow.h \
 settings.h \
 settingsdialog.h
FORMS += aboutdialog.ui mainwindow.ui settingsdialog.ui
SOURCES += aboutdialog.cpp \
 appinfo.cpp \
 appsettings.cpp \
 main.cpp \
 mainwindow.cpp \
 settings.cpp \
 settingsdialog.cpp \
 qtc-gdbmacros/gdbmacros.cpp
TRANSLATIONS += l10n/run1s_ru.ts
QT += core network gui
CONFIG += warn_on
RESOURCES += run1s.qrc
VERSION = 0.1
