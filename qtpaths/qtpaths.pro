isEqual(QT_MAJOR_VERSION, 5) {
  DEFINES += HAVE_QT5
}
TEMPLATE = app
TARGET = qtpaths
SOURCES += qtpaths.cpp
