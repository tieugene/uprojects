#include <QLabel>
#include <QMessageBox>
#include <QProcess>
#include <QXmlStreamReader>
#include <QUrl>
#include <QNetworkRequest>

#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "appsettings.h"

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
}

MainWindow::~MainWindow()
{
	delete ui;
	delete settingsDlg;
	delete aboutDlg;
	delete netmgr;
	delete tray;
}

void MainWindow::createTrayIcon() {
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
	connect(ui->actionSettings, SIGNAL(triggered()), SLOT(slSettings()));
	connect(ui->actionAbout, SIGNAL(triggered()), SLOT(slAbout()));
	connect(ui->actionAboutQt, SIGNAL(triggered()), SLOT(slAboutQt()));
	connect(ui->tableWidget, SIGNAL(currentItemChanged (QTableWidgetItem *, QTableWidgetItem *)), SLOT(slItemChanged(QTableWidgetItem *, QTableWidgetItem *)));
	connect(tray, SIGNAL(activated ( QSystemTrayIcon::ActivationReason)), SLOT(slTray(QSystemTrayIcon::ActivationReason)));
	connect(actionHideRestore, SIGNAL(triggered()), SLOT(slHideRestore()));
	connect(netmgr, SIGNAL(finished(QNetworkReply *)), SLOT(slNetReplyFinished(QNetworkReply *)));
}

void MainWindow::processReply(const QByteArray &resp) {
	QString token, ver, host, share, path, type, org, comments;

	QXmlStreamReader xml(resp);
	while (!xml.atEnd()) {
		xml.readNext();
		if (xml.isStartElement ()) {
			token = xml.name().toString();
			if (token == "run1s") {
				ver = xml.attributes().value("", "ver").toString();
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
			} else {
			}
		}
	}
}

void MainWindow::slUpdate() {
	if (AppSettings::getTrayEnabled()) {
		if (!tray->isVisible())
			tray->show();
	} else {
		if (tray->isVisible())
			tray->hide();
	}
	ui->tableWidget->setRowCount(0);
	netmgr->get(QNetworkRequest(QUrl(AppSettings::getServer() + "/baselist")));
}

void MainWindow::slExit() {
	close();
}

void MainWindow::slRunEnterprise() {
	// check 1C executable and path
	//QProcess *process = new QProcess(); process->execute("juffed");
	QProcess::startDetached("juffed");
}

void MainWindow::slAbout() {
	aboutDlg->exec();
}

void MainWindow::slAboutQt() {
	QMessageBox::aboutQt(this, tr("About Qt"));
}

void MainWindow::slSettings() {
	if (settingsDlg->exec())
		slUpdate();
}

void MainWindow::slItemChanged(QTableWidgetItem *curr, QTableWidgetItem *prev) {
	if (ui->tableWidget->rowCount())
		if ((curr) and ((!prev) or (curr->row() != prev->row())))
			statusBar()->showMessage(baselist[curr->row()]);
}

void MainWindow::slTray(QSystemTrayIcon::ActivationReason reason) {
	if (reason == QSystemTrayIcon::Trigger)
		slHideRestore();
}

void MainWindow::slHideRestore() {
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
		statusBar()->showMessage(tr("Network error: ") + reply->errorString(), 3000);
	else
		processReply(reply->readAll());
}
