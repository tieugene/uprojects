#include "appsettings.h"

QString \
	mainsection("main"),\
	serverkey("server"),\
	portkey("port"),\
	loginkey("login"),\
	passwordkey("password"),\
	path1skey("path1s"),\
	minonrunkey("minonrun"),\
	usetraykey("usetray"),\
	starthiddenkey("starthidden"),\
	mintotraykey("mintotray");


QString AppSettings::getServer(void) {
	return Settings::stringValue(mainsection, serverkey);
}

int AppSettings::getPort(void) {
	return Settings::intValue(mainsection, portkey, 80);
}

QString AppSettings::getLogin(void) {
	return Settings::stringValue(mainsection, loginkey);
}

QString AppSettings::getPassword(void) {
	return Settings::stringValue(mainsection, passwordkey);
}

QString AppSettings::getPath1C(void) {
	return Settings::stringValue(mainsection, path1skey);
}

bool AppSettings::getMinOnRun(void) {
	return Settings::boolValue(mainsection, minonrunkey, false);
}

bool AppSettings::getTrayEnabled(void) {
	return Settings::boolValue(mainsection, usetraykey, false);
}

bool AppSettings::getStartHidden(void) {
	return Settings::boolValue(mainsection, starthiddenkey, false);
}

bool AppSettings::getMinToTray(void) {
	return Settings::boolValue(mainsection, mintotraykey, false);
}

// ---

void AppSettings::setServer(const QString& value) {
	Settings::setValue(mainsection, serverkey, value);
}

void AppSettings::setPort(const int value) {
	Settings::setValue(mainsection, portkey, value);
}

void AppSettings::setLogin(const QString& value) {
	Settings::setValue(mainsection, loginkey, value);
}

void AppSettings::setPassword(const QString& value) {
	Settings::setValue(mainsection, passwordkey, value);
}

void AppSettings::setPath1C(const QString& value) {
	Settings::setValue(mainsection, path1skey, value);
}

void AppSettings::setMinOnRun(const bool value) {
	Settings::setValue(mainsection, minonrunkey, value);
}

void AppSettings::setTrayEnabled(const bool value) {
	Settings::setValue(mainsection, usetraykey, value);
}

void AppSettings::setStartHidden(const bool value) {
	Settings::setValue(mainsection, starthiddenkey, value);
}

void AppSettings::setMinToTray(const bool value) {
	Settings::setValue(mainsection, mintotraykey, value);
}
