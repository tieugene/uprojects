#include <QtGui/QFileDialog>

#include "settingsdialog.h"
#include "ui_settingsdialog.h"
#include "appsettings.h"

SettingsDialog::SettingsDialog(QWidget *parent) :
    QDialog(parent),
    m_ui(new Ui::SettingsDialog)
{
    m_ui->setupUi(this);
    connect(m_ui->pbPath, SIGNAL(clicked()), SLOT(slPath()));
}

SettingsDialog::~SettingsDialog()
{
    delete m_ui;
}

void SettingsDialog::changeEvent(QEvent *e)
{
    switch (e->type()) {
    case QEvent::LanguageChange:
        m_ui->retranslateUi(this);
        break;
    default:
        break;
    }
}

int SettingsDialog::exec() {
	init();
	return QDialog::exec();
}

void SettingsDialog::init() {
	m_ui->leServer->setText(AppSettings::getServer());
	m_ui->leLogin->setText(AppSettings::getLogin());
	m_ui->lePassword->setText(AppSettings::getPassword());
	m_ui->lePath->setText(AppSettings::getPath1C());
}

void SettingsDialog::accept() {
	AppSettings::setServer(m_ui->leServer->text());
	AppSettings::setLogin(m_ui->leLogin->text());
	AppSettings::setPassword(m_ui->lePassword->text());
	AppSettings::setPath1C(m_ui->lePath->text());
	Settings::write();
	QDialog::accept();
}

void SettingsDialog::reject() {
	QDialog::reject();
}

void SettingsDialog::slPath() {
	QString filename = QFileDialog::getOpenFileName(
			this,
			tr("Open 1C executable"),
			AppSettings::getPath1C(),
			tr("Executable files (*.exe)")
	);
	if (!filename.isEmpty()) {
		m_ui->lePath->setText(filename);
	}
}
