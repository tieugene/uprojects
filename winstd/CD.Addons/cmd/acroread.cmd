\bin\AdbeRdr1010_ru_RU.exe /msi /quiet /norestart
del /Q "%ALLUSERSPROFILE%\����稩 �⮫\Adobe Reader X.lnk"
reg delete HKLM\Software\Microsoft\Windows\CurrentVersion\Run /v "Adobe ARM" /f
