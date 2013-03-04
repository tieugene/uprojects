#!/bin/sh
for i in (Cards Price A T P); do ./chkattr.sh $i/cfg.xml $1 $2 | sort | uniq; done