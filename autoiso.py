#!/env python
# sript to make ISOs from folders and remove them after
# folder names must be YYMMDD
# ISOs will YYMMDDYYMMDD.iso
# in: * dir of archives, * dir of ISOs
# os.chdir(), os.getcwd()
'''
#!/bin/sh
# script to make iso from bulk of dirs
# USAGE: <outfile.iso> dir[ dir...]
# TODO: Usage:, options, -volid <volumeid>, checksize (4483MB)
LISTFILE=`mktemp`
DESTFILE="$1"
shift
for i in "$@"; do find $i -type f | while read j; do    echo "$j=$j" >> $LISTFILE; done; done
mkisofs -o $DESTFILE -graft-points -rational-rock -joliet -joliet-long -no-cache-inodes -full-iso9660-filenames -iso-level 2 -path-list $LISTFILE
rm -rf $LISTFILE

pushd raw
mkiso.sh ../110515110708.iso 110515 110706 110707 110708 && rm -rf 110515 110706 110707 110708
popd
'''

import sys, os

DVDSIZE = 4700000000
MKISOARGS = "-graft-points -rational-rock -joliet -joliet-long -no-cache-inodes -full-iso9660-filenames -iso-level 2"

def	foldersize(path):
	retvalue = 0
	for (path, dirs, files) in os.walk(folder):
		for file in files:
			retvalue += os.path.getsize(os.path.join(path, file))
	return retvalue

def	getfolder(path):
	'''
	Get files - names and sizes
	'''
	folders = dict()
	foldernames = os.listdir(path)
	for folder in foldernames:
		fullpath = os.path.join(path, folder)
		if (os.path.isdir(fullpath)):
			size = foldersize(fullpath)
			if (size < DVDSIZE):
				folders[folder] = size
			else:
				sys.stderr.write(folder + ' is too big')
	return folders

if (__name__ == '__main__'):
	# 0. check args
	if (len(sys.argv) != 3):
		print "Usage: %s <srcdir> <dstdir>" % sys.argv[0]
		sys.exit(0)
	srcdir = argv[1]
	dstdir = argv[2]
	if (!os.path.isdir(srcdir)):
		sys.stderr.write(srcdir + ' is not dir')
		sys.exit(1)
	if (!os.path.isdir(dstdir)):
		sys.stderr.write(dstdir + ' is not dir')
		sys.exit(2)
	# 1. get files
	folders = getfolders(srcdir)
	# 2. create ISOs
	foldersnames = folders.keys()
	foldernames.sort()
	i = 0
	popd = os.getcwd()
	os.chdir(srcdir)
	report = list()
	# 2. while is anything to write
	while (sum(folders.values()) > DVDSIZE()):
		tmplist = list()	# folders to create current ISO
		tmpsize = 0		# summary of folder sizes
	# 3. while fill 1 ISO
		while ((tmpsize + folders[foldernames[i]]) < DVDSIZE):
			tmplist.append(foldernames[i])
			tmpsize += folders[foldernames[i]]
			i += 1
			del folders[foldernames[i]]
	# 4. mk command: iso name and all arguments
		isoname = tmplist[0] + tmplist[-1] + ".iso"
		dirs = " ".join(tmplist)
		cmd = "echo \"%s\" | mkisofs %s -o %s -path-list - && rm -rf %s" % (dirs, MKISOARGS, dstdir, isoname, dirs)
		report.append(isoname)
		print cmd
	# 5. that's all
	os.chdir(popd)
	# 6. report
	print "\n".join(report)
