#!/bin/sh
# script to make iso from bulk of dirs
# USAGE: <outfile.iso> dir[ dir...]
# TODO: Usage:, options, -volid <volumeid>
LISTFILE=`mktemp`
DESTFILE="$1"
shift
for i in "$@"; do find $i -type f | while read j; do 	echo "$j=$j" >> $LISTFILE; done; done
genisoimage -o $DESTFILE -graft-points -rational-rock -joliet -joliet-long -no-cache-inodes -full-iso9660-filenames -iso-level 2 -path-list $LISTFILE
rm -rf $LISTFILE
