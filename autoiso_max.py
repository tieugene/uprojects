#!/bin/env python
# sript to make ISOs from folders and remove them after:
# in: * dir of archives, * dir of ISOs
# 1. calculate folders sizes in given folder
# 2. pack them into ISOs (as many as possible)
# 3. remove written
# src requirements:
# * src must contains folders only
# * that names must be YYMMDD
# * that must contains files only
# ISOs will YYMMDDYYMMDD.iso

import sys, os, tempfile

# global consts
DVDSIZE = 4700000000
MKISOFS = '/usr/bin/mkisofs'
MKISOARGS = '-quiet -graft-points -rational-rock -joliet -joliet-long -no-cache-inodes -full-iso9660-filenames -iso-level 2'
#YYMMDD = re.compile()

reload(sys)
sys.setdefaultencoding('utf-8')

def	flush_iso(srcdir, dstdir, filelist):
	retvalue = 0
	# 1. create list
	tmp = tempfile.NamedTemporaryFile(delete=False)
	for i in filelist:
		tmp.write("%s=%s\n" % (i, i))
	tmp.close()
	# 2. create iso
	isoname = os.path.join(dstdir, "%s%s.iso" % (filelist[0].split('/', 1)[0], filelist[-1].split('/', 1)[0]))
	popd = os.getcwd()
	os.chdir(srcdir)
	cmd = "mkisofs %s -o %s -path-list %s" % (MKISOARGS, isoname, tmp.name)
	print >> sys.stderr, "Creating ISO: %s" % isoname
	retvalue = os.system(cmd)
	os.chdir(popd)
	# 3. cleanup
	os.unlink(tmp.name)
	if (retvalue == 0):
		for i in filelist:
			#print >> sys.stderr, "remove %s" % os.path.join(srcdir, i)
			os.remove(os.path.join(srcdir, i))
	return retvalue

if (__name__ == '__main__'):
	# 0. check args
	# - arglist
	if (len(sys.argv) != 3):
		print 'Usage: %s <srcdir> <dstdir>' % sys.argv[0]
		sys.exit(0)
	# - mkisofs
	if (not os.path.exists(MKISOFS)):
		sys.stderr.write('"%s" not found.' % MKISOFS)
		sys.exit(1)
	# - src folder
	srcdir = sys.argv[1]
	if (not os.path.isdir(srcdir)):
		sys.stderr.write('Source "%s" is not folder.' % srcdir)
		sys.exit(2)
	# - dst folder
	dstdir = sys.argv[2]
	if (not os.path.isdir(dstdir)):
		sys.stderr.write('Destination "%s" is not folder.' % dstdir)
		sys.exit(3)
	# /0; go
	CurrSize = 0
	CurrList = list()
	foldernames = os.listdir(srcdir)
	foldernames.sort()
	# 1. scan source
	for yymmdd in foldernames:
		yymmdd_full = os.path.join(srcdir, yymmdd)
		if (not os.path.isdir(yymmdd_full)):		# skip not folders
			print >> sys.stderr, 'Skiping "%s" - is a file' % yymmdd_full
			continue
		filenames = os.listdir(yymmdd_full)
		filenames.sort()
		# 2. scan yymmdd/*
		for fn in filenames:
			full_fn = os.path.join(yymmdd_full, fn)
			if (not os.path.isfile(full_fn)):	# skip not files
				print >> sys.stderr, 'Skiping "%s" - is not file' % full_fn
				continue
			fs = os.path.getsize(full_fn)
			if ((CurrSize + fs) >= DVDSIZE):	# ready to flush
				if (flush_iso(srcdir, dstdir, CurrList)):
					print >> sys.stderr, 'Error creating ISO'
					break
				# 4. reset vars
				CurrSize = 0
				CurrList[:] = []
			CurrList.append(os.path.join(yymmdd, fn))
			CurrSize += fs
	# try to rmdir empty folders
	for yymmdd in foldernames:
		try:
			os.rmdir(os.path.join(srcdir, yymmdd))
		except:
			pass
