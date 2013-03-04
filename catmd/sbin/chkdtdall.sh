#!/bin/sh
# validate cfg.xml's in batch mode

if [ $# = 0 ]
	then
		echo "Usage: $0 <filelist> - w/o extention (.md)" >&2
	else
		if test -r $1
			then
				cd ../../src/Raw/catmd
				sbin/src2dtd.sh
				cd ../../../run/catmd
				for i in $(cat $1 | grep -v ^#); do echo $i; nice xmllint --noout --valid --postvalid $i/cfg.xml 2>Err/$i.err; done
			else
				echo "$1 doesn't exists." >&2
		fi
fi
