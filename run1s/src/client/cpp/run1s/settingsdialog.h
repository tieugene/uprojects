#ifndef SETTINGSDIALOG_H
#define SETTINGSDIALOG_H

#include <QtGui/QDialog>

namespace Ui {
    class SettingsDialog;
}

class SettingsDialog : public QDialog {
	Q_OBJECT
	Q_DISABLE_COPY(SettingsDialog)
public:
	explicit SettingsDialog(QWidget *parent = 0);
	virtual ~SettingsDialog();

public slots:
	int exec();
	void accept();
	void reject();
	void slPath();

protected:
	virtual void changeEvent(QEvent *e);

private:
	Ui::SettingsDialog *m_ui;
	void init();
};

#endif // SETTINGSDIALOG_H
