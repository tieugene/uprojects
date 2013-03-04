/*
Copyright 2009 Eugene A. Pivnev

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

#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QAction>
#include <QList>
#include <QMainWindow>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QMenu>
#include <QSystemTrayIcon>
#include <QListWidgetItem>

#include "settingsdialog.h"
#include "aboutdialog.h"

namespace Ui
{
	class MainWindowClass;
}

class MainWindow : public QMainWindow
{
	Q_OBJECT

	enum	Mode1C {
		Simple,
		Mono,
		Config,
		Monitor,
		Debug
	};
public:
	MainWindow(QWidget *parent = 0);
	~MainWindow();
	void	go(void);

public slots:
	void	slUpdate(void);

private slots:
	void	slExit(void);
	void	slRunEnterprise(void);
	void	slRunEnterpriseMono(void);
	void	slRunConfigurer(void);
	void	slRunMonitor(void);
	void	slSettings(void);
	void	slAbout(void);
	void	slAboutQt(void);
	void	slNetReplyFinished(QNetworkReply *);
	void	slRowChanged(int);
	void	slItemDClicked(QListWidgetItem *);
	void	slTray(const QSystemTrayIcon::ActivationReason);
	void	slHideRestore(void);

private:
	Ui::MainWindowClass *ui;
	void	setSlots(void);
	void	createTrayIcon(void);
	void	processXmlReply(QByteArray);
	void	processTxtReply(QByteArray);
	void	run1Cexe(const Mode1C);
	QString	mkTitle(QString, QString, QString);

	SettingsDialog		*settingsDlg;
	AboutDialog		*aboutDlg;
	QSystemTrayIcon		*tray;
	QMenu			*trayMenu;
	QAction			*actionHideRestore;
	QNetworkAccessManager	*netmgr;
	QList<QString>		baselist;
	int			serial;

protected:
	void	hideEvent ( QHideEvent *);
};

#endif // MAINWINDOW_H
