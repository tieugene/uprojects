#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QAction>
//#include <QHttp>
#include <QList>
#include <QMainWindow>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QMenu>
#include <QSystemTrayIcon>
#include <QTableWidgetItem>

#include "settingsdialog.h"
#include "aboutdialog.h"

namespace Ui
{
	class MainWindowClass;
}

class MainWindow : public QMainWindow
{
	Q_OBJECT

public:
	MainWindow(QWidget *parent = 0);
	~MainWindow();

public slots:
	void	slUpdate();

private slots:
	void	slExit();
	void	slRunEnterprise();
	void	slSettings();
	void	slAbout();
	void	slAboutQt();
	void	slNetReplyFinished(QNetworkReply *);
	void	slItemChanged(QTableWidgetItem *, QTableWidgetItem *);
	void	slTray(QSystemTrayIcon::ActivationReason);
	void	slHideRestore();

private:
	Ui::MainWindowClass *ui;
	void	setSlots(void);
	void	createTrayIcon();
	void	processReply(const QByteArray &);

	SettingsDialog			*settingsDlg;
	AboutDialog			*aboutDlg;
	QSystemTrayIcon			*tray;
	QMenu				*trayMenu;
	QAction				*actionHideRestore;
	QNetworkAccessManager		*netmgr;
	bool				fullsize;
	QList<QString>			baselist;
};

#endif // MAINWINDOW_H
