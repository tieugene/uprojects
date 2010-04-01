#!/bin/sh
# validate xml
cd ../../src/Raw/catmd
sbin/src2dtd.sh
cd ../../../run/catmd
#clear
xmllint --noout --valid --postvalid $1/cfg.xml 2>Err/$1.err