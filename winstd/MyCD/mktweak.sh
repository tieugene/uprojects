#!/bin/sh
OUTFILE="\$OEM\$/tweaks.reg"
UTF2WIN=""
cat reg.utf/head.txt | unix2dos | iconv -f UTF-8 -t UTF-16 > $OUTFILE
for i in hkcr hklm hklm_services hkcu;
do
    cat reg.utf/$i.txt | unix2dos | iconv -f UTF-8 -t UTF-16 >> $OUTFILE
done
