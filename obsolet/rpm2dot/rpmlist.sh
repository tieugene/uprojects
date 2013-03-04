#!/bin/sh
# list all of dependencies
# 0. head
GETALL="/usr/local/bin/rpm-qa.py"
#GETALL="cat rpms | sort"

for i in `$GETALL`; do
	echo "$i"
	for j in `rpm -q --provides $i | gawk '{print $1}'`; do
		echo ">	$j"
	done
	for j in `rpm -q --requires $i | gawk '{print $1}'`; do
		echo "<	$j"
	done
done
