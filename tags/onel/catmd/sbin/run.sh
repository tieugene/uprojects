#!/bin/sh
if [ $# = 0 ]
	then
		echo "Usage: $0 <Name>(.md) - w/o extention" >&2
	else
		if test -r MD/$1.md
			then
				#clear
				rm -rf $1
				./catmd MD/$1.md $1
				ln catmd.dtd $1/catmd.dtd
			else
				echo "$1.md doesn't exists." >&2
		fi
fi
