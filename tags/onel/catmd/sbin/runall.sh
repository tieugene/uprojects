#!/bin/sh
# convert batch of MDs

if [ $# = 0 ]
	then
		echo "Usage: $0 <filelist> - w/o extention (.md)" >&2
	else
		if test -r $1
			then
				for i in $(cat $1 | grep -v ^#); do echo "**** $i: ****" >&2; nice ./run.sh $i; done
			else
				echo "$1 doesn't exists." >&2
		fi
fi
