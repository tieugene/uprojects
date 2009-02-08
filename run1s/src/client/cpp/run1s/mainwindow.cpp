#include <QtCore/QXmlStreamReader>
#include <QtCore/QProcess>
#include <QtGui/QLabel>
#include <QtGui/QMessageBox>
#include <QtGui/QTableWidgetItem>

#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "settingsdialog.h"
#include "aboutdialog.h"
#include "appsettings.h"

class	Interior {
public:
	Interior(QWidget* parent) :
		toolBar(0),
		panelsMenu(0),
		toolbarsMenu(0) {

		settingsDlg = new SettingsDialog(parent);
		aboutDlg = new AboutDialog(parent);
	}
	~Interior() {
		delete settingsDlg;
		delete aboutDlg;
	}

	SettingsDialog* settingsDlg;
	AboutDialog* aboutDlg;

	QLabel* fileNameL;
	QToolBar* toolBar;
	QMap<QString, QMenu*> mainMenuItems;
	QMenu* panelsMenu;
	QMenu* toolbarsMenu;
	QRect geometry;
};


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), ui(new Ui::MainWindowClass)
{
	ui->setupUi(this);
	interior = new Interior(this);
	http = new QHttp();
	setSlots();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::setSlots(void) {
	connect(ui->actionExit, SIGNAL(triggered()), SLOT(exit()));
	connect(ui->actionEnterprise, SIGNAL(triggered()), SLOT(runEnterprise()));
	connect(ui->actionSettings, SIGNAL(triggered()), SLOT(settings()));
	connect(ui->actionAbout, SIGNAL(triggered()), SLOT(about()));
	connect(ui->actionAboutQt, SIGNAL(triggered()), SLOT(aboutQt()));


	connect(http, SIGNAL(readyRead(const QHttpResponseHeader &)), SLOT(slReadyRead(const QHttpResponseHeader &)));
	connect(ui->tableWidget, SIGNAL(currentItemChanged (QTableWidgetItem *, QTableWidgetItem *)), SLOT(slItemChanged(QTableWidgetItem *, QTableWidgetItem *)));
}

void MainWindow::Update() {
	http->setHost(AppSettings::getServer(), 80);
	http->get("/baselist");		// put something into /var/www/html/baselist file
}

void MainWindow::exit() {
	close();
}

void MainWindow::runEnterprise() {
	// check 1C executable and path
	//QProcess *process = new QProcess(); process->execute("juffed");
	QProcess::startDetached("juffed");
}

void MainWindow::about() {
	interior->aboutDlg->exec();
}

void MainWindow::aboutQt() {
	QMessageBox::aboutQt(this, tr("About Qt"));
}

void MainWindow::settings() {
	interior->settingsDlg->exec();
}

void MainWindow::slReadyRead(const QHttpResponseHeader &resp) {
	QString token, ver, host, share, path, type, org, comments;

	printf("Status: %d", resp.statusCode());
	QXmlStreamReader xml(http->readAll());
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

void MainWindow::slItemChanged(QTableWidgetItem *curr, QTableWidgetItem *prev) {
	if ((!prev) or (curr->row() != prev->row())) {
		statusBar()->showMessage(baselist[curr->row()]);
	}
}
