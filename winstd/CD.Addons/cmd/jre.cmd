\bin\jre-6u29-windows-i586-s.exe /s
reg delete HKLM\Software\Microsoft\Windows\CurrentVersion\Run /v SunJavaUpdateSched /f
reg import \meta\jre.reg
