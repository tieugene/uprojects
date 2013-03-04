#!/bin/sh
./test.py Name | sort > Name.txt
./test.py Requirename | sort > Requirename.txt
./test.py Providename | sort > Providename.txt
