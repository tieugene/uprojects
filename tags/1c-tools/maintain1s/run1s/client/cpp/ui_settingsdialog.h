/********************************************************************************
** Form generated from reading ui file 'settingsdialog.ui'
**
** Created: Fri Apr 24 11:39:55 2009
**      by: Qt User Interface Compiler version 4.5.0
**
** WARNING! All changes made in this file will be lost when recompiling ui file!
********************************************************************************/

#ifndef UI_SETTINGSDIALOG_H
#define UI_SETTINGSDIALOG_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QCheckBox>
#include <QtGui/QDialog>
#include <QtGui/QDialogButtonBox>
#include <QtGui/QGridLayout>
#include <QtGui/QHeaderView>
#include <QtGui/QLabel>
#include <QtGui/QLineEdit>
#include <QtGui/QPushButton>

QT_BEGIN_NAMESPACE

class Ui_SettingsDialog
{
public:
    QGridLayout *gridLayout;
    QLabel *labelServer;
    QLineEdit *leServer;
    QLabel *labelLogin;
    QLineEdit *leLogin;
    QLabel *labelPassword;
    QLineEdit *lePassword;
    QLabel *label1sPath;
    QLineEdit *lePath;
    QPushButton *pbPath;
    QCheckBox *cbMinOnRun;
    QCheckBox *cbTrayEnabled;
    QDialogButtonBox *buttonBox;
    QCheckBox *cbMinToTray;
    QCheckBox *cbStartHidden;

    void setupUi(QDialog *SettingsDialog)
    {
        if (SettingsDialog->objectName().isEmpty())
            SettingsDialog->setObjectName(QString::fromUtf8("SettingsDialog"));
        SettingsDialog->resize(431, 238);
        gridLayout = new QGridLayout(SettingsDialog);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        labelServer = new QLabel(SettingsDialog);
        labelServer->setObjectName(QString::fromUtf8("labelServer"));

        gridLayout->addWidget(labelServer, 0, 0, 1, 1);

        leServer = new QLineEdit(SettingsDialog);
        leServer->setObjectName(QString::fromUtf8("leServer"));

        gridLayout->addWidget(leServer, 0, 1, 1, 5);

        labelLogin = new QLabel(SettingsDialog);
        labelLogin->setObjectName(QString::fromUtf8("labelLogin"));

        gridLayout->addWidget(labelLogin, 1, 0, 1, 1);

        leLogin = new QLineEdit(SettingsDialog);
        leLogin->setObjectName(QString::fromUtf8("leLogin"));

        gridLayout->addWidget(leLogin, 1, 1, 1, 2);

        labelPassword = new QLabel(SettingsDialog);
        labelPassword->setObjectName(QString::fromUtf8("labelPassword"));

        gridLayout->addWidget(labelPassword, 1, 4, 1, 1);

        lePassword = new QLineEdit(SettingsDialog);
        lePassword->setObjectName(QString::fromUtf8("lePassword"));
        lePassword->setEchoMode(QLineEdit::Password);

        gridLayout->addWidget(lePassword, 1, 5, 1, 1);

        label1sPath = new QLabel(SettingsDialog);
        label1sPath->setObjectName(QString::fromUtf8("label1sPath"));

        gridLayout->addWidget(label1sPath, 2, 0, 1, 1);

        lePath = new QLineEdit(SettingsDialog);
        lePath->setObjectName(QString::fromUtf8("lePath"));

        gridLayout->addWidget(lePath, 2, 1, 1, 4);

        pbPath = new QPushButton(SettingsDialog);
        pbPath->setObjectName(QString::fromUtf8("pbPath"));

        gridLayout->addWidget(pbPath, 2, 5, 1, 1);

        cbMinOnRun = new QCheckBox(SettingsDialog);
        cbMinOnRun->setObjectName(QString::fromUtf8("cbMinOnRun"));
        cbMinOnRun->setLayoutDirection(Qt::RightToLeft);

        gridLayout->addWidget(cbMinOnRun, 3, 0, 1, 3);

        cbTrayEnabled = new QCheckBox(SettingsDialog);
        cbTrayEnabled->setObjectName(QString::fromUtf8("cbTrayEnabled"));
        cbTrayEnabled->setLayoutDirection(Qt::RightToLeft);

        gridLayout->addWidget(cbTrayEnabled, 3, 3, 1, 3);

        buttonBox = new QDialogButtonBox(SettingsDialog);
        buttonBox->setObjectName(QString::fromUtf8("buttonBox"));
        buttonBox->setOrientation(Qt::Horizontal);
        buttonBox->setStandardButtons(QDialogButtonBox::Cancel|QDialogButtonBox::Ok);

        gridLayout->addWidget(buttonBox, 6, 0, 1, 6);

        cbMinToTray = new QCheckBox(SettingsDialog);
        cbMinToTray->setObjectName(QString::fromUtf8("cbMinToTray"));
        cbMinToTray->setLayoutDirection(Qt::RightToLeft);

        gridLayout->addWidget(cbMinToTray, 4, 3, 1, 3);

        cbStartHidden = new QCheckBox(SettingsDialog);
        cbStartHidden->setObjectName(QString::fromUtf8("cbStartHidden"));
        cbStartHidden->setLayoutDirection(Qt::RightToLeft);

        gridLayout->addWidget(cbStartHidden, 4, 0, 1, 3);

#ifndef QT_NO_SHORTCUT
        labelServer->setBuddy(leServer);
        labelLogin->setBuddy(leLogin);
        labelPassword->setBuddy(lePassword);
        label1sPath->setBuddy(lePath);
#endif // QT_NO_SHORTCUT
        QWidget::setTabOrder(leServer, leLogin);
        QWidget::setTabOrder(leLogin, lePassword);
        QWidget::setTabOrder(lePassword, lePath);
        QWidget::setTabOrder(lePath, pbPath);
        QWidget::setTabOrder(pbPath, cbMinOnRun);
        QWidget::setTabOrder(cbMinOnRun, cbTrayEnabled);
        QWidget::setTabOrder(cbTrayEnabled, buttonBox);

        retranslateUi(SettingsDialog);
        QObject::connect(buttonBox, SIGNAL(accepted()), SettingsDialog, SLOT(accept()));
        QObject::connect(buttonBox, SIGNAL(rejected()), SettingsDialog, SLOT(reject()));

        QMetaObject::connectSlotsByName(SettingsDialog);
    } // setupUi

    void retranslateUi(QDialog *SettingsDialog)
    {
        SettingsDialog->setWindowTitle(QApplication::translate("SettingsDialog", "Settings", 0, QApplication::UnicodeUTF8));
        labelServer->setText(QApplication::translate("SettingsDialog", "&Server:", 0, QApplication::UnicodeUTF8));
        labelLogin->setText(QApplication::translate("SettingsDialog", "&Login:", 0, QApplication::UnicodeUTF8));
        labelPassword->setText(QApplication::translate("SettingsDialog", "&Password:", 0, QApplication::UnicodeUTF8));
        label1sPath->setText(QApplication::translate("SettingsDialog", "&1C path:", 0, QApplication::UnicodeUTF8));
        pbPath->setText(QApplication::translate("SettingsDialog", "...", 0, QApplication::UnicodeUTF8));
        cbMinOnRun->setText(QApplication::translate("SettingsDialog", "Minimize on run 1C", 0, QApplication::UnicodeUTF8));
        cbTrayEnabled->setText(QApplication::translate("SettingsDialog", "Use system tray", 0, QApplication::UnicodeUTF8));
        cbMinToTray->setText(QApplication::translate("SettingsDialog", "Minimize to tray", 0, QApplication::UnicodeUTF8));
        cbStartHidden->setText(QApplication::translate("SettingsDialog", "Start hidden", 0, QApplication::UnicodeUTF8));
        Q_UNUSED(SettingsDialog);
    } // retranslateUi

};

namespace Ui {
    class SettingsDialog: public Ui_SettingsDialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_SETTINGSDIALOG_H
