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

#include <QDir>
#include <QFile>
#include <QLabel>
#include <QMessageBox>
#include <QProcess>
#include <QXmlStreamReader>
#include <QUrl>
#include <QNetworkRequest>

#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "appsettings.h"

const char *modekey[4] = {
	"/enterprise",
	"/enterprise /M",
	"/config",
	"/monitor"
};

MainWindow::MainWindow(QWidget *parent) :
	QMainWindow(parent),
	ui(new Ui::MainWindowClass)
{
	ui->setupUi(this);
	settingsDlg = new SettingsDialog(this);
	aboutDlg = new AboutDialog(this);
	netmgr = new QNetworkAccessManager(this);
	createTrayIcon();
	setSlots();
	fullsize = true;
	serial = 0;
}

MainWindow::~MainWindow()
{
	delete ui;
	delete settingsDlg;
	delete aboutDlg;
	delete netmgr;
	delete tray;
}

void MainWindow::go(void) {
	show();
	QString warning;
	if (AppSettings::getServer().isEmpty())
		warning += tr("Server not defined.\n");
	if (AppSettings::getLogin().isEmpty())
		warning += tr("Login not defined.\n");
	if (AppSettings::getPath1C().isEmpty())
		warning += tr("1C executable not defined.\n");
	if (not warning.isEmpty())
		QMessageBox::warning(this, tr("Run1s"), warning + tr("Check Options->Settings."));
	slUpdate();	// FIXME:
}

void MainWindow::createTrayIcon(void) {
	trayMenu = new QMenu(this);
	actionHideRestore = new QAction(tr("&Hide"), this);
	trayMenu->addAction(actionHideRestore);
	trayMenu->addSeparator();
	trayMenu->addAction(ui->actionExit);

	tray = new QSystemTrayIcon(this);
	tray->setContextMenu(trayMenu);
	tray->setIcon(QIcon(QIcon(":/icons/1c_16x16.png")));
	tray->setToolTip(tr("Run1s client"));
}

void MainWindow::setSlots(void) {
	connect(ui->actionExit, SIGNAL(triggered()), SLOT(slExit()));
	connect(ui->actionEnterprise, SIGNAL(triggered()), SLOT(slRunEnterprise()));
	connect(ui->actionEnterprise_singleuser, SIGNAL(triggered()), SLOT(slRunEnterpriseMono()));
	connect(ui->actionConfigurer, SIGNAL(triggered()), SLOT(slRunConfigurer()));
	connect(ui->actionMonitor, SIGNAL(triggered()), SLOT(slRunMonitor()));
	connect(ui->actionSettings, SIGNAL(triggered()), SLOT(slSettings()));
	connect(ui->actionAbout, SIGNAL(triggered()), SLOT(slAbout()));
	connect(ui->actionAboutQt, SIGNAL(triggered()), SLOT(slAboutQt()));
	connect(ui->tableWidget, SIGNAL(currentItemChanged (QTableWidgetItem *, QTableWidgetItem *)), SLOT(slItemChanged(QTableWidgetItem *, QTableWidgetItem *)));
	connect(tray, SIGNAL(activated ( QSystemTrayIcon::ActivationReason)), SLOT(slTray(QSystemTrayIcon::ActivationReason)));
	connect(actionHideRestore, SIGNAL(triggered()), SLOT(slHideRestore()));
	connect(netmgr, SIGNAL(finished(QNetworkReply *)), SLOT(slNetReplyFinished(QNetworkReply *)));
}

void MainWindow::processReply(QByteArray resp) {
	QString token, ver, host, share, path, type, org, comments, error;
	int	sn;

	QXmlStreamReader xml(resp);
	while (!xml.atEnd()) {
		xml.readNext();
		if (xml.isStartElement ()) {
			token = xml.name().toString();
			if (token == "run1s") {
				ver = xml.attributes().value("", "ver").toString();
				sn = xml.attributes().value("", "sn").toString().toInt();
			} else if (token == "host") {
				host = xml.attributes().value("", "name").toString();
			} else if (token == "share") {
				share = xml.attributes().value("", "name").toString();
			} else if (token == "base") {
				path	= xml.attributes().value("", "path").toString();
				type	= xml.attributes().value("", "type").toString();
				org	= xml.attributes().value("", "org").toString();
				comments= xml.attributes().value("", "comments").toString();
				int r = ui->tableWidget->rowCount();
				ui->tableWidget->setRowCount(r + 1);
				ui->tableWidget->setItem(r, 0, new QTableWidgetItem(type));
				ui->tableWidget->setItem(r, 1, new QTableWidgetItem(org));
				ui->tableWidget->setItem(r, 2, new QTableWidgetItem(comments));
				baselist.append("\\\\" + host + "\\" + share + "\\" + path);
			} else if (token == "error") {
				error += xml.attributes().value("", "text").toString();
			}
		}
	}
	ui->tableWidget->resizeColumnsToContents();
	if (not error.isEmpty())
		QMessageBox::critical(this, tr("Run1s"), error);
}

void MainWindow::run1Cexe(const Mode1C mode) {
	QString _1s(AppSettings::getPath1C()), base;

	if (ui->tableWidget->rowCount() == 0)
		QMessageBox::critical(this, tr("Run1s"), tr("Database list is empty."));
	else if (ui->tableWidget->currentRow() < 0)
		QMessageBox::critical(this, tr("Run1s"), tr("No database selected."));
	else if (_1s.isEmpty())
		QMessageBox::critical(this, tr("Run1s"), tr("1C executable not defined.\nCheck Options->Settings."));
	else if (not QFile::exists(_1s))
		QMessageBox::critical(this, tr("Run1s"), tr("1C executable not found.\nCheck Options->Settings."));
	else {
		base = baselist[ui->tableWidget->currentRow()];
		//if (not QDir::exists(base))	// error: некорректный вызов элемента-функции ‘bool QDir::exists(const QString&) const’ без объекта
		//	QMessageBox::critical(this, tr("Run1s"), tr("Selected directory not exists."));
		//else
			QProcess::startDetached(_1s + " " + mode + " /D" + baselist[ui->tableWidget->currentRow()]);
			//QMessageBox::information(this, tr("Run1s"), _1s + " " + modekey[mode] + " /D" + base);
	}
}

void MainWindow::slUpdate(void) {
	if (AppSettings::getTrayEnabled()) {
		if (!tray->isVisible())
			tray->show();
	} else {
		if (tray->isVisible())
			tray->hide();
	}
	ui->tableWidget->setRowCount(0);
	if (not (AppSettings::getServer().isEmpty() or AppSettings::getLogin().isEmpty()))  
		netmgr->get(QNetworkRequest(QUrl(AppSettings::getServer() + "/baselist&login=" + AppSettings::getLogin() + "&password=" + AppSettings::getPassword())));
}

void MainWindow::slExit(void) {
	close();
}

void MainWindow::slRunEnterprise(void) {
	run1Cexe(Simple);
}

void MainWindow::slRunEnterpriseMono(void) {
	run1Cexe(Mono);
}

void MainWindow::slRunConfigurer(void) {
	run1Cexe(Config);
}

void MainWindow::slRunMonitor(void) {
	run1Cexe(Monitor);
}

void MainWindow::slAbout(void) {
	aboutDlg->exec();
}

void MainWindow::slAboutQt(void) {
	QMessageBox::aboutQt(this, tr("About Qt"));
}

void MainWindow::slSettings(void) {
	if (settingsDlg->exec())
		slUpdate();
}

void MainWindow::slItemChanged(QTableWidgetItem *curr, QTableWidgetItem *prev) {
	if (ui->tableWidget->rowCount())
		if ((curr) and ((!prev) or (curr->row() != prev->row())))
			statusBar()->showMessage(baselist[curr->row()]);
}

void MainWindow::slTray(const QSystemTrayIcon::ActivationReason reason) {
	if (reason == QSystemTrayIcon::Trigger)
		slHideRestore();
}

void MainWindow::slHideRestore(void) {
	if (fullsize) {
		hide();
		actionHideRestore->setText(tr("&Restore"));
	} else {
		show();
		actionHideRestore->setText(tr("&Hide"));
		slUpdate();
	}
	fullsize = not fullsize;
}

void MainWindow::slNetReplyFinished(QNetworkReply *reply) {
	QNetworkReply::NetworkError err = reply->error();
	if (err)
		statusBar()->showMessage(tr("Network error: ") + reply->errorString(), 5000);
	else
		processReply(reply->readAll());
}
