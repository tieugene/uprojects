#!/bin/sh
# repack RpYYqQ.tar into ready Rp
MYDIR=`pwd`
TMPDIR=`mktemp -d`
tar xf $1 -C $TMPDIR
pushd $TMPDIR > /dev/null
for i in `ls *.EXE`; do unrar x -y $i > /dev/null; rm -f $i; done
tar zcf $MYDIR/`basename $1`.gz *
popd > /dev/null
rm -rf $TMPDIR
