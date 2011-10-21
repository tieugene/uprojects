\bin\jre-6u21-windows-i586-s.exe /quiet /norestart
reg delete HKLM\Software\Microsoft\Windows\CurrentVersion\Run /v SunJavaUpdateSched /f
reg import \reg\jre.reg
