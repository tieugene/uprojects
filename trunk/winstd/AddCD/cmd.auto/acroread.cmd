\AutoIt3.exe \autoit\acroread.au3
del /Q "C:\Documents and Settings\All Users\Рабочий стол\Adobe Reader 9.lnk"
reg delete HKLM\Software\Microsoft\Windows\CurrentVersion\Run /v "Adobe ARM" /f
reg delete HKLM\Software\Microsoft\Windows\CurrentVersion\Run /v "Adobe Reader Speed Launcher" /f
