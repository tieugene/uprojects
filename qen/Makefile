all: Ui_Main.py Main_rc.py Ui_Settings.py Settings_rc.py

clean:
	rm -f Main_*
	rm -f Settings_*
	rm -f Ui_*
	rm -f *.pyc

Ui_Main.py :
	pyuic4 Main.ui -o Ui_Main.py

Main_rc.py :
	pyrcc4 Main.qrc -o Main_rc.py

Ui_Settings.py :
	pyuic4 Settings.ui -o Ui_Settings.py

Settings_rc.py :
	pyrcc4 Settings.qrc -o Settings_rc.py
