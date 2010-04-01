#!/bin/sh
# converts source DTD (w/ comments) into working
# dtd2 Schema: trang.sh catmd.dtd catmd.xsd

if [ $# = 0 ]
	then
		echo "Usage: $0 <Name.src.dtd>" >&2
	else
		SRC=$1
		DST=$(basename $1 .src.dtd).dtd
		if test -r $SRC
			then
				cat $SRC | gawk -F "\t+//" '{print $1}' > $DST
			else
				echo "File $SRC doesn't exists." >&2
		fi
fi
