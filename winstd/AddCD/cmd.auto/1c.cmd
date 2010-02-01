rmdir /q /s ""C:\Program Files\1Cv77"
\bin\Accounting\1CV77\DISK1\setup.exe /s /sms
rename "C:\Program Files\1Cv77\BIN\lckls.pls" trade.dll
rename "C:\Program Files\1Cv77\BIN\tnsct.pls" salary.dll
copy /Y \bin\Accounting\1CV77\1cv7.exe "C:\Program Files\1Cv77\BIN\"
copy \bin\Accounting\1CV77\v7plus.* "C:\Program Files\1Cv77\BIN\"
regsvr32 /s "C:\Program Files\1Cv77\BIN\v7plus.dll"
