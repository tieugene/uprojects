/********************************************************************************
** Form generated from reading ui file 'mainwindow.ui'
**
** Created: Fri Apr 24 11:39:55 2009
**      by: Qt User Interface Compiler version 4.5.0
**
** WARNING! All changes made in this file will be lost when recompiling ui file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QGridLayout>
#include <QtGui/QHeaderView>
#include <QtGui/QListWidget>
#include <QtGui/QMainWindow>
#include <QtGui/QMenu>
#include <QtGui/QMenuBar>
#include <QtGui/QStatusBar>
#include <QtGui/QToolBar>
#include <QtGui/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindowClass
{
public:
    QAction *actionExit;
    QAction *actionHelp;
    QAction *actionAbout;
    QAction *actionAboutQt;
    QAction *actionSettings;
    QAction *actionEnterprise;
    QAction *actionEnterprise_singleuser;
    QAction *actionConfigurer;
    QAction *actionMonitor;
    QWidget *centralWidget;
    QGridLayout *gridLayout;
    QListWidget *listWidget;
    QMenuBar *menuBar;
    QMenu *menuFile;
    QMenu *menuOptions;
    QMenu *menuHelp;
    QMenu *menuAction;
    QStatusBar *statusBar;
    QToolBar *FileToolBar;
    QToolBar *OptionsToolBar;
    QToolBar *ActionsToolBar;

    void setupUi(QMainWindow *MainWindowClass)
    {
        if (MainWindowClass->objectName().isEmpty())
            MainWindowClass->setObjectName(QString::fromUtf8("MainWindowClass"));
        MainWindowClass->resize(274, 328);
        QSizePolicy sizePolicy(QSizePolicy::Maximum, QSizePolicy::MinimumExpanding);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(MainWindowClass->sizePolicy().hasHeightForWidth());
        MainWindowClass->setSizePolicy(sizePolicy);
        QIcon icon;
        icon.addPixmap(QPixmap(QString::fromUtf8("icons/1c_16x16.png")), QIcon::Normal, QIcon::Off);
        MainWindowClass->setWindowIcon(icon);
        actionExit = new QAction(MainWindowClass);
        actionExit->setObjectName(QString::fromUtf8("actionExit"));
        QIcon icon1;
        icon1.addPixmap(QPixmap(QString::fromUtf8(":/icons/exit_32x32.png")), QIcon::Normal, QIcon::Off);
        actionExit->setIcon(icon1);
        actionHelp = new QAction(MainWindowClass);
        actionHelp->setObjectName(QString::fromUtf8("actionHelp"));
        QIcon icon2;
        icon2.addPixmap(QPixmap(QString::fromUtf8(":/icons/help_32x32.png")), QIcon::Normal, QIcon::Off);
        actionHelp->setIcon(icon2);
        actionAbout = new QAction(MainWindowClass);
        actionAbout->setObjectName(QString::fromUtf8("actionAbout"));
        QIcon icon3;
        icon3.addPixmap(QPixmap(QString::fromUtf8(":/icons/1c_32x32.png")), QIcon::Normal, QIcon::Off);
        actionAbout->setIcon(icon3);
        actionAboutQt = new QAction(MainWindowClass);
        actionAboutQt->setObjectName(QString::fromUtf8("actionAboutQt"));
        QIcon icon4;
        icon4.addPixmap(QPixmap(QString::fromUtf8(":/icons/qt_32x32.png")), QIcon::Normal, QIcon::Off);
        actionAboutQt->setIcon(icon4);
        actionSettings = new QAction(MainWindowClass);
        actionSettings->setObjectName(QString::fromUtf8("actionSettings"));
        QIcon icon5;
        icon5.addPixmap(QPixmap(QString::fromUtf8(":/icons/settings_32x32.png")), QIcon::Normal, QIcon::Off);
        actionSettings->setIcon(icon5);
        actionEnterprise = new QAction(MainWindowClass);
        actionEnterprise->setObjectName(QString::fromUtf8("actionEnterprise"));
        QIcon icon6;
        icon6.addPixmap(QPixmap(QString::fromUtf8(":/icons/1cv7_ent_32x32.png")), QIcon::Normal, QIcon::Off);
        actionEnterprise->setIcon(icon6);
        actionEnterprise_singleuser = new QAction(MainWindowClass);
        actionEnterprise_singleuser->setObjectName(QString::fromUtf8("actionEnterprise_singleuser"));
        QIcon icon7;
        icon7.addPixmap(QPixmap(QString::fromUtf8(":/icons/1cv7_rep_32x32.png")), QIcon::Normal, QIcon::Off);
        actionEnterprise_singleuser->setIcon(icon7);
        actionConfigurer = new QAction(MainWindowClass);
        actionConfigurer->setObjectName(QString::fromUtf8("actionConfigurer"));
        QIcon icon8;
        icon8.addPixmap(QPixmap(QString::fromUtf8(":/icons/1cv7_cfg_32x32.png")), QIcon::Normal, QIcon::Off);
        actionConfigurer->setIcon(icon8);
        actionMonitor = new QAction(MainWindowClass);
        actionMonitor->setObjectName(QString::fromUtf8("actionMonitor"));
        QIcon icon9;
        icon9.addPixmap(QPixmap(QString::fromUtf8(":/icons/1cv7_mon_32x32.png")), QIcon::Normal, QIcon::Off);
        actionMonitor->setIcon(icon9);
        centralWidget = new QWidget(MainWindowClass);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        gridLayout = new QGridLayout(centralWidget);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        listWidget = new QListWidget(centralWidget);
        listWidget->setObjectName(QString::fromUtf8("listWidget"));

        gridLayout->addWidget(listWidget, 0, 0, 1, 1);

        MainWindowClass->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(MainWindowClass);
        menuBar->setObjectName(QString::fromUtf8("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 274, 23));
        menuFile = new QMenu(menuBar);
        menuFile->setObjectName(QString::fromUtf8("menuFile"));
        menuOptions = new QMenu(menuBar);
        menuOptions->setObjectName(QString::fromUtf8("menuOptions"));
        menuHelp = new QMenu(menuBar);
        menuHelp->setObjectName(QString::fromUtf8("menuHelp"));
        menuAction = new QMenu(menuBar);
        menuAction->setObjectName(QString::fromUtf8("menuAction"));
        MainWindowClass->setMenuBar(menuBar);
        statusBar = new QStatusBar(MainWindowClass);
        statusBar->setObjectName(QString::fromUtf8("statusBar"));
        MainWindowClass->setStatusBar(statusBar);
        FileToolBar = new QToolBar(MainWindowClass);
        FileToolBar->setObjectName(QString::fromUtf8("FileToolBar"));
        MainWindowClass->addToolBar(Qt::TopToolBarArea, FileToolBar);
        OptionsToolBar = new QToolBar(MainWindowClass);
        OptionsToolBar->setObjectName(QString::fromUtf8("OptionsToolBar"));
        MainWindowClass->addToolBar(Qt::TopToolBarArea, OptionsToolBar);
        ActionsToolBar = new QToolBar(MainWindowClass);
        ActionsToolBar->setObjectName(QString::fromUtf8("ActionsToolBar"));
        MainWindowClass->addToolBar(Qt::TopToolBarArea, ActionsToolBar);

        menuBar->addAction(menuFile->menuAction());
        menuBar->addAction(menuAction->menuAction());
        menuBar->addAction(menuOptions->menuAction());
        menuBar->addAction(menuHelp->menuAction());
        menuFile->addAction(actionExit);
        menuOptions->addAction(actionSettings);
        menuHelp->addAction(actionHelp);
        menuHelp->addAction(actionAbout);
        menuHelp->addAction(actionAboutQt);
        menuAction->addAction(actionEnterprise);
        menuAction->addAction(actionEnterprise_singleuser);
        menuAction->addAction(actionConfigurer);
        menuAction->addAction(actionMonitor);
        FileToolBar->addAction(actionExit);
        OptionsToolBar->addAction(actionSettings);
        ActionsToolBar->addAction(actionEnterprise);
        ActionsToolBar->addAction(actionEnterprise_singleuser);
        ActionsToolBar->addAction(actionConfigurer);
        ActionsToolBar->addAction(actionMonitor);

        retranslateUi(MainWindowClass);

        QMetaObject::connectSlotsByName(MainWindowClass);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindowClass)
    {
        MainWindowClass->setWindowTitle(QApplication::translate("MainWindowClass", "run1s", 0, QApplication::UnicodeUTF8));
        actionExit->setText(QApplication::translate("MainWindowClass", "&Exit", 0, QApplication::UnicodeUTF8));
        actionExit->setShortcut(QApplication::translate("MainWindowClass", "Ctrl+Q", 0, QApplication::UnicodeUTF8));
        actionHelp->setText(QApplication::translate("MainWindowClass", "Help", 0, QApplication::UnicodeUTF8));
        actionHelp->setShortcut(QApplication::translate("MainWindowClass", "F1", 0, QApplication::UnicodeUTF8));
        actionAbout->setText(QApplication::translate("MainWindowClass", "About", 0, QApplication::UnicodeUTF8));
        actionAboutQt->setText(QApplication::translate("MainWindowClass", "About Qt", 0, QApplication::UnicodeUTF8));
        actionSettings->setText(QApplication::translate("MainWindowClass", "Settings", 0, QApplication::UnicodeUTF8));
        actionEnterprise->setText(QApplication::translate("MainWindowClass", "Enterprise", 0, QApplication::UnicodeUTF8));
        actionEnterprise_singleuser->setText(QApplication::translate("MainWindowClass", "Enterprise (singleuser)", 0, QApplication::UnicodeUTF8));
        actionConfigurer->setText(QApplication::translate("MainWindowClass", "Configurer", 0, QApplication::UnicodeUTF8));
        actionMonitor->setText(QApplication::translate("MainWindowClass", "Monitor", 0, QApplication::UnicodeUTF8));
        actionMonitor->setShortcut(QApplication::translate("MainWindowClass", "Ctrl+M", 0, QApplication::UnicodeUTF8));
        menuFile->setTitle(QApplication::translate("MainWindowClass", "&File", 0, QApplication::UnicodeUTF8));
        menuOptions->setTitle(QApplication::translate("MainWindowClass", "&Options", 0, QApplication::UnicodeUTF8));
        menuHelp->setTitle(QApplication::translate("MainWindowClass", "&Help", 0, QApplication::UnicodeUTF8));
        menuAction->setTitle(QApplication::translate("MainWindowClass", "&Action", 0, QApplication::UnicodeUTF8));
        FileToolBar->setWindowTitle(QApplication::translate("MainWindowClass", "toolBar", 0, QApplication::UnicodeUTF8));
        OptionsToolBar->setWindowTitle(QApplication::translate("MainWindowClass", "toolBar", 0, QApplication::UnicodeUTF8));
        ActionsToolBar->setWindowTitle(QApplication::translate("MainWindowClass", "toolBar", 0, QApplication::UnicodeUTF8));
    } // retranslateUi

};

namespace Ui {
    class MainWindowClass: public Ui_MainWindowClass {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
