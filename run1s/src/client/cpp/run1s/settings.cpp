/*
Copyright 2007-2008 Mikhail Murzin

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
version 2 as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
*/

//	Qt includes
#include <QtCore/QDir>
#include <QtCore/QFileInfo>
#include <QtCore/QSettings>

#include "settings.h"

void Settings::read() {
	//QSettings sett(AppInfo::configFile(), QSettings::IniFormat);
	QSettings::setDefaultFormat(QSettings::IniFormat);
	QSettings sett;

	QStringList groups = sett.childGroups();
	foreach (QString grp, groups) {
		sett.beginGroup(grp);
		if (!settData->data.contains(grp))
			settData->data[grp] = Section();

		QStringList groupKeys = sett.childKeys();
		foreach (QString key, groupKeys) {
			QVariant value = sett.value(key);
			settData->data[grp][key] = value;
		}
		sett.endGroup();
	}
}

void Settings::write() {
	//QSettings sett(AppInfo::configFile(), QSettings::IniFormat);
	QSettings::setDefaultFormat(QSettings::IniFormat);
	QSettings sett;

	QStringList groups = settData->data.keys();
	foreach (QString grp, groups) {
		QStringList keys = settData->data[grp].keys();
		sett.beginGroup(grp);
		foreach (QString key, keys) {
			sett.setValue(key, value(grp, key));
		}
		sett.endGroup();
	}
}

bool Settings::valueExists(const QString& section, const QString& key) {
	return settData->data[section].contains(key);
}

QVariant Settings::value(const QString& section, const QString& key) {
	return settData->data[section][key];
}

QString Settings::stringValue(const QString& section, const QString& key, const QString& def) {
	return settData->data[section].value(key, def).toString();
}

int Settings::intValue(const QString& section, const QString& key, int def) {
	return settData->data[section].value(key, def).toInt();
}

bool Settings::boolValue(const QString& section, const QString& key, bool def) {
	return settData->data[section].value(key, def).toBool	();
}

void Settings::setValue(const QString& section, const QString& key, const QVariant& value) {
	settData->data[section][key] = value;
}

QStringList Settings::sectionList() {
	return settData->data.keys();
}

QStringList Settings::keyList(const QString& section) {
	return settData->data[section].keys();
}

SettingsData* Settings::settData = new SettingsData();
