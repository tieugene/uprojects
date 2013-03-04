#!/bin/sh
./chkattr.py $1/cfg.xml $2 $3 | sort | uniq