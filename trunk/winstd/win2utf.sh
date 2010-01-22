#!/bin/sh
# convert Windows' reg-file into utf text
# src file must be *.reg
#recode Unicode $1 && dos2unix $1
iconv -f UTF-16 -t UTF-8 $1 | dos2unix > `basename $1 .reg`.txt