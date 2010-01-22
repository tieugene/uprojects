#!/bin/sh
# converts utf-8 text file into Windows' unicode
# src file must be *.txt
cat $1 | unix2dos | iconv -f UTF-8 -t UTF-16 > `basename $1 .txt`.reg
