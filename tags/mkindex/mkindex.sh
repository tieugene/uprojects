#!/bin/sh
# mkindex.sh - make html list from dir done. Put it into ~/bin
if [ -z "$1" ]; then
	P=`pwd`
else
	P="$1"
fi
pushd $P>/dev/null 2>&1
echo "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\">\
	<head>\
	<META HTTP-EQUIV=\"CONTENT-TYPE\" CONTENT=\"text/html; charset=utf-8\">\
	<title>Index of $P</title></head><body>\
	<h1> Index of $P </h1>" > index.html
OLDIFS=$IFS; IFS=$'\n'
for i in `ls -1LF | grep /$ && ls -1LF | grep -v /$ | tr -d \*`; do
    echo "<a href=\"$i\"> $i </a></br>" >> index.html
done
echo "</body></html>" >> index.html
popd $P>/dev/null 2>&1
