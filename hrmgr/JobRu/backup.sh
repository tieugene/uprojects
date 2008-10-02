#!/bin/sh
rm -rf *~
rm -rf *.pyc
rm -rf doc/*~
tar jcf ../JobRu.$(date +%y%m%d).tar.bz2 .
