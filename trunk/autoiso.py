#!/bin/env python
# sript to make ISOs from folders and remove them after:
# 1. calculate folders sizes in given folder
# 2. pack them into ISOs (as many as possible)
# 3. remove them
# folder names must be YYMMDD
# ISOs will YYMMDDYYMMDD.iso
# in: * dir of archives, * dir of ISOs

import sys, os

DVDSIZE = 4700000000
MKISOARGS = "-graft-points -rational-rock -joliet -joliet-long -no-cache-inodes -full-iso9660-filenames -iso-level 2"

def	foldersize(path):
	retvalue = 0
	for (path, dirs, files) in os.walk(path):
		for file in files:
			retvalue += os.path.getsize(os.path.join(path, file))
	return retvalue

def	getfolders(path):
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
	srcdir = sys.argv[1]
	dstdir = sys.argv[2]
	if (not os.path.isdir(srcdir)):
		sys.stderr.write(srcdir + ' is not dir')
		sys.exit(1)
	if (not os.path.isdir(dstdir)):
		sys.stderr.write(dstdir + ' is not dir')
		sys.exit(2)
	# 1. get files
	folders = getfolders(srcdir)
	# 2. create ISOs
	foldernames = folders.keys()
	foldernames.sort()
	i = 0
	popd = os.getcwd()
	os.chdir(srcdir)
	report = list()
	# 2. while is anything to write
	while (sum(folders.values()) > DVDSIZE):
		tmplist = list()	# folders to create current ISO
		tmpsize = 0		# summary of folder sizes
	# 3. while fill 1 ISO
		while ((tmpsize + folders[foldernames[i]]) < DVDSIZE):
			tmplist.append(foldernames[i])
			tmpsize += folders[foldernames[i]]
			del folders[foldernames[i]]
			i += 1
	# 4. mk command: iso name and all arguments
		isoname = tmplist[0] + tmplist[-1] + ".iso"
		dirlist = " ".join(tmplist)
		cmd = "LISTFILE=`mktemp`; for i in %s; do find $i -type f | while read j; do echo \"$j=$j\" >> $LISTFILE; done; done; mkisofs %s -o %s/%s -path-list $LISTFILE && rm -rf %s" % (dirlist, MKISOARGS, dstdir, isoname, dirlist)
		report.append(os.path.join(dstdir, isoname))
		#print cmd
		os.system(cmd)
	# 5. that's all
	os.chdir(popd)
	# 6. report
	print "\n".join(report)
