#!/bin/sh
# tool to make rpm dependencies list
# 0. head
echo "digraph rpm {
	rankdir=LR;"
# 1 - get all of rpms
echo "	node [shape = box];"
#/usr/local/bin/rpm-qa.py
for i in `cat rpms`; do
	echo "		\"$i\""
done
echo "	;"
# 2. get all requires
echo "	node [shape = ellipse];"
for i in `cat rpms | xargs rpm -q --requires | sort | uniq | gawk '{print $1}'`; do
	echo "		\"#$i\""
done
echo "	;"
# [3. get all provides]
# 4. for each of rpm
for i in `cat rpms`; do
# 4.1. show all provides
	for j in `rpm -q --provides $i | gawk '{print $1}'`; do
		echo "	\"$i\" -> \"#$j\""
	done
# 4.2. and requires
	for j in `rpm -q --requires $i | gawk '{print $1}'`; do
		echo "	\"#$j\" -> \"$i\""
	done
done

echo "}"
