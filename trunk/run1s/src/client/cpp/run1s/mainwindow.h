#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QtCore/QList>
#include <QtGui/QMainWindow>
#include <QtGui/QTableWidgetItem>
#include <QtNetwork/QHttp>

namespace Ui
{
	class MainWindowClass;
}

class	Interior;

class MainWindow : public QMainWindow
{
	Q_OBJECT

public:
	MainWindow(QWidget *parent = 0);
	~MainWindow();
	void	Update(void);

private slots:
	void exit();
	void runEnterprise();
	void settings();
	void about();
	void aboutQt();
	void slReadyRead(const QHttpResponseHeader &);
	void slItemChanged(QTableWidgetItem *, QTableWidgetItem *);

private:
	Ui::MainWindowClass *ui;
	void    setSlots(void);

	Interior	*interior;
	QHttp		*http;
	QList<QString>	baselist;
};

#endif // MAINWINDOW_H
