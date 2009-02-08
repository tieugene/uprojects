#include "appsettings.h"

static char mainsection[] = "main";
static char serverkey[] = "server";
static char loginkey[] = "login";
static char passwordkey[] = "password";
static char path1skey[] = "path1s";
static char minonrunkey[] = "minonrun";
static char usetraykey[] = "usetray";
static char starthiddenkey[] = "starthidden";
static char mintotraykey[] = "mintotray";

QString AppSettings::getServer(void) {
	return Settings::value(mainsection, serverkey).toString();
}

QString AppSettings::getLogin(void) {
	return Settings::value(mainsection, loginkey).toString();
}

QString AppSettings::getPassword(void) {
	return Settings::value(mainsection, passwordkey).toString();
}

QString AppSettings::getPath1C(void) {
	return Settings::value(mainsection, path1skey).toString();
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
