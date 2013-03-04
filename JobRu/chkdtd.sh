#!/bin/sh
# validate xml
#xmllint --noout --valid --postvalid $1/cfg.xml 2>Err/$1.err
xmllint --noout --valid --postvalid $1
