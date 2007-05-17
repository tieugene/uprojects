### Quamachi Makefile


# Defines

ifndef KDEDIR
	KDEDIR = /usr/
endif

ifndef USER
	USER = $(LOGNAME)
endif

ifndef HOME
	HOME = /home/$(USER)/
endif


# Aliases

all: Main_Ui.py Main_RCC.py Settings_Ui.py Settings_RCC.py
	@echo ""
	@echo "Making Quamachi.  Before installing Quamachi, please peruse the README."
	@echo ""


install: Install.AllUsers


install-user: Install.CurrentUser


uninstall: UnInstall.AllUsers


uninstall-user: UnInstall.CurrentUser


clean:
	@echo ""
	@echo "Cleaning the Quamachi objects."
	@echo ""
	rm -f ../Source/Main_*
	rm -f ../Source/Settings_*
	rm -f ../Source/*.pyc
	@echo ""
	@echo "The Quamachi objects have been cleaned."
	@echo ""


# Installers

Install.AllUsers :
	@echo ""
	@echo "Installing Quamachi for all users."
	@echo "Only root can run 'make install'.  Others should instead run: 'make install-user'"
	@echo "Before using this unstable script, please thoroughly read the Installation section of the README."
	@echo ""
	make uninstall
	make clean
	make all
	mkdir -p $(KDEDIR)/share/apps/Quamachi/
	cp -r ../Doc/ $(KDEDIR)/share/apps/Quamachi/
	cp -r ../Desktop/ $(KDEDIR)/share/apps/Quamachi/
	cp -r ../Source/ $(KDEDIR)/share/apps/Quamachi/
	chmod 777 $(KDEDIR)/share/apps/Quamachi/Source/
	chmod 775 $(KDEDIR)/share/apps/Quamachi/Source/Quamachi.pyw
	mkdir -p $(KDEDIR)/bin/
	ln -fs $(KDEDIR)/share/apps/Quamachi/Source/Quamachi.pyw $(KDEDIR)/bin/Quamachi.pyw
	#mkdir -p $(KDEDIR)/share/apps/konqueror/servicemenus/
	#cp -u ../Desktop/Context/Live/* $(KDEDIR)/share/apps/konqueror/servicemenus/
	#rm -f ~$(USER)/.kde/share/apps/konqueror/servicemenus/Quamachi*
	mkdir -p $(KDEDIR)/share/applnk/Internet/
	#mkdir -p $(KDEDIR)/share/applications/kde/
	cp ../Desktop/KMenu/* $(KDEDIR)/share/applnk/Internet/
	#cp ../Desktop/KMenu/* $(KDEDIR)/share/applications/kde/
	#mkdir -p $(KDEDIR)/share/icons/hicolor/32x32/actions/
	#ln -fs $(KDEDIR)/share/apps/Quamachi/Source/Images/actions/ark* $(KDEDIR)/share/icons/hicolor/32x32/actions/
	mkdir -p $(KDEDIR)/share/icons/hicolor/32x32/apps/
	ln -fs $(KDEDIR)/share/apps/Quamachi/Source/Images/apps/Quamachi* $(KDEDIR)/share/icons/hicolor/32x32/apps/
	@echo ""
	@echo "Finished.  To run Quamachi, enter: Quamachi.pyw &"
	@echo ""

Install.CurrentUser :
	@echo ""
	@echo "Installing Quamachi for the current user.  In the case of errors, please view the README."
	@echo ""
	make uninstall-user
	make clean
	make all
	mkdir -p $(HOME)/.kde/share/apps/Quamachi/
	cp -r ../Doc/ $(HOME)/.kde/share/apps/Quamachi/
	cp -r ../Desktop/ $(HOME)/.kde/share/apps/Quamachi/
	cp -r ../Source/ $(HOME)/.kde/share/apps/Quamachi/
	chmod 775 $(HOME)/.kde/share/apps/Quamachi/Source/Quamachi.pyw
	mkdir -p $(HOME)/bin/
	ln -fs $(HOME)/.kde/share/apps/Quamachi/Source/Quamachi.pyw $(HOME)/bin/Quamachi.pyw
	#mkdir -p $(HOME)/.kde/share/apps/konqueror/servicemenus/
	#rm -f $(HOME)/.kde/share/apps/konqueror/servicemenus/Quamachi.marker.*
	#rm -f $(HOME)/.kde/share/apps/konqueror/servicemenus/Quamachi*
	#cp -u ../Desktop/Context/Live/* $(HOME)/.kde/share/apps/konqueror/servicemenus/
	mkdir -p $(HOME)/.kde/share/applnk/Internet/
	#mkdir -p $(HOME)/.kde/share/applications/kde/
	cp ../Desktop/KMenu/* $(HOME)/.kde/share/applnk/Internet/
	#cp ../Desktop/KMenu/* $(HOME)/.kde/share/applications/kde/
	#mkdir -p $(HOME)/.kde/share/icons/hicolor/32x32/actions/
	#ln -fs $(HOME)/.kde/share/apps/Quamachi/Source/Images/actions/ark* $(HOME)/.kde/share/icons/hicolor/32x32/actions/
	mkdir -p $(HOME)/.kde/share/icons/hicolor/32x32/apps/
	ln -fs $(HOME)/.kde/share/apps/Quamachi/Source/Images/apps/Quamachi* $(HOME)/.kde/share/icons/hicolor/32x32/apps/
	@echo ""
	@echo "Finished.  You should add $(HOME)/bin to the PATH variable in your ~/.bash_profile or equivalent."
	@echo "Then restart KDE.  To run Quamachi, enter: Quamachi.pyw &"
	@echo ""


# Uninstallers

UnInstall.AllUsers :
	@echo ""
	@echo "Removing Quamachi for all users."
	@echo "Only root can run 'make uninstall'.  Others should instead run: 'make uninstall-user'"
	@echo "Before using this unstable script, please thoroughly read the UnInstallation section of the README."
	@echo ""
	#rm -f $(KDEDIR)/share/icons/hicolor/32x32/actions/ark*
	rm -f $(KDEDIR)/share/icons/hicolor/32x32/apps/Quamachi*
	#rm -f $(KDEDIR)/share/apps/konqueror/servicemenus/Quamachi*
	rm -f $(KDEDIR)/share/applnk/Internet/Quamachi*
	#rm -f $(KDEDIR)/share/applications/kde/Quamachi*
	rm -f $(KDEDIR)/bin/Quamachi*
	rm -rf $(KDEDIR)/share/apps/Quamachi/
	#rm -f ~$(USER)/.kde/share/apps/konqueror/servicemenus/Quamachi*
	@echo ""
	@echo "Quamachi has been removed."
	@echo ""

UnInstall.CurrentUser :
	@echo ""
	@echo "Removing Quamachi for the current user.  In the case of errors, please view the README."
	@echo ""
	#rm -f $(HOME)/.kde/share/icons/hicolor/32x32/actions/ark*
	rm -f $(HOME)/.kde/share/icons/hicolor/32x32/apps/Quamachi*
	#rm -f $(HOME)/.kde/share/apps/konqueror/servicemenus/Quamachi*
	rm -f $(HOME)/.kde/share/applnk/Internet/Quamachi*
	#rm -f $(HOME)/.kde/share/applications/kde/Quamachi*
	rm -f $(HOME)/bin/Quamachi*
	rm -rf $(HOME)/.kde/share/apps/Quamachi/
	@echo ""
	@echo "Quamachi has been removed."
	@echo ""


# Objects

Main_Ui.py :
	pyuic4 ../Source/Main.ui -o ../Source/Main_ui.py

Main_RCC.py :
	pyrcc4 ../Source/Main.qrc -o ../Source/Main_rc.py

Settings_Ui.py :
	pyuic4 ../Source/Settings.ui -o ../Source/Settings_ui.py

Settings_RCC.py :
	pyrcc4 ../Source/Settings.qrc -o ../Source/Settings_rc.py
