#!/bin/sh
# cat all uniq c_<entity>\tattr\value
./catattrs.py $1/cfg.xml | sort | uniq > $1.log
wc -l $1.log