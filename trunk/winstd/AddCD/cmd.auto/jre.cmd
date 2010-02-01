\bin\jre-6u18-windows-i586.exe /quiet /norestart
reg delete HKLM\Software\Microsoft\Windows\CurrentVersion\Run /v SunJavaUpdateSched /f
reg import \reg\jre.reg
