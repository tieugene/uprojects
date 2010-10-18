#!/bin/env python
# -*- coding: utf-8 -*-
'''
dosemu:
	vm.mmap_min_addr
sysctl -w vm.mmap_min_addr=0
/etc/sysctl.conf

Naming:
	* Tunes:	<T>770xxx.tar.gz
	* Reports:	<T>yy
Upacking:
	* tunes:
	* reports: unupx + unrar
'''
import sys, os, tempfile, array, httplib, subprocess, shutil, tarfile

# URLs
URLBASE		= 'downloads.1c.ru'
URLAUTH		= '/auth.jsp'
URLKEY2		= URLAUTH+'?its=%d'			# KEY1
URLGET		= '/get.jsp'
URLMAGIC	= URLGET+'?its=%s&addr=%s&d=%s'		# KEY1, KEY2, KEY3
URLTUNES	= '/ipp/ITSREPV/%s/VER.ID'		# tune remote dir

# PATHs
INFODAT		= "./INFO.DAT"
BASEDIR		= "/mnt/shares/tmp/1C"

tunes = (	# Name, local, remote
	(u'Бухгалтерия',	'A', 'BU42TK'),
	(u'УСН',		'U', 'BASUOR'),
	(u'Предприниматель',	'E', 'PBOUL'),
	(u'ТиС',		'T', 'OUTK'),
	(u'ЗиК',		'S', 'R2CLKTK'),
)
reports = (
	(u'Бухгалтерия',	'A', 'GeneralN'),
	(u'УСН',		'U', 'BASUOR'),
	(u'Предприниматель',	'E', 'PBOUL'),
)

reload(sys)
sys.setdefaultencoding("utf-8")

def	getkey1(path):
	return os.path.getsize(path) / 1000 - 828

def	getkey3(path, index):
	'''
	Function to get INFO.DAT secret data
	@param path:str - path of INFO.DAT
	@param index:int - 
	'''
	mask = (23,1,24,10,22,4,6,9,14,24,11,13,15,1,22,3)
	retvalue = ''
	special = os.path.getsize(path) / 1000 + 1
	f = open(path, "rb")
	if (f):
		block = array.array('c')
		f.seek(index)
		block.fromfile(f, 16)
		for i, c in enumerate(block):
			if (i==1):
				val = ord(block[0]) + special;
			else:
				val = ord(c) + mask[i];
			retvalue += chr(((val - 1) % 26) + 65)	# mod(en) + 'A'
	return retvalue

def	dlstr(conn, path):
	'''
	download string
	@param conn:HTTPConnection - connection
	@param pat:str - subpath
	@return (bool, string)
	'''
	retvalue = (False, None)
	conn.request('GET', path)
	rq = conn.getresponse()
	if (rq.status == 200):
		retvalue = (True, rq.read())
	return retvalue

def	getmagic(conn):
	'''
	Get magic URL
	@param conn:HTTPConnection
	@return str
	'''
	key = [None, None, None]
	key[0] = getkey1(INFODAT)		# key1
	r, s = dlstr(conn, URLKEY2 % key[0])
	if r:
		key[1] = int(s)
	key[2] = getkey3(INFODAT, key[1])	# key3
	return URLMAGIC % tuple(key)

def	ucase(dn):
	'''
	Uppercase all of files and dirs in given dir
	'''
	flag = False
	for root, dirs, files in os.walk(dn):
		# 1. files
		for name in files:
			ff = os.path.join(root, name)
			# 1. chmod files
			os.chmod(ff, 0666)
			# 2. rename files
			uname = name.upper()
			if name != uname:
				os.rename(ff, os.path.join(root, uname))
		for i, name in enumerate(dirs):
			uname = name.upper()
			if name != uname:
				os.rename(os.path.join(root, name), os.path.join(root, uname))
				dirs[i] = uname

def	unpack(fn):
	tdir = tempfile.mkdtemp()
	shutil.copy(fn, tdir)
	p = subprocess.Popen(['dosemu', '-dumb', fn], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=tdir)
	p.wait()	# FIXME: deadlock: stdout=PIPE and/or stderr=PIPE
	if p.returncode:
		print "StdOut:", p.stdout.read()
		print "StdErr:", p.stderr.read()
	else:
		# 1. kill source update.exe
		os.remove(os.path.join(tdir, fn))
		# 2. upercase
		ucase(tdir)
		# 3. pack
		aname = tempfile.mktemp(suffix='.tar.gz')
		popd = os.getcwd()
		os.chdir(tdir)
		tar = tarfile.open(aname, 'w:gz')
		for i in os.listdir(tdir):
			tar.add(i)
		tar.close()
		os.chdir(popd)
		# 4. remove tmp
		shutil.rmtree(tdir)
		shutil.move(aname, 'tmp.tar.gz')
	return

if (__name__ == '__main__'):
#	unpack('tmp.exe')
#	exit()

	conn = httplib.HTTPConnection(URLBASE)
	# 1. check 1C news:
	#getnews();
	for t in tunes:
		r, s = dlstr(conn, URLTUNES % t[2])
	#	if r:
	#		print s
	# 2. check our last tunes
	#getour();
	# 3. try download tunes
	MAGIC = getmagic(conn)
	for i in xrange(5):
		#i = 1	# BASUOR
		url = MAGIC + '&dir=%s&file=UPDATE.EXE' % tunes[i][2]
		# http://downloads.1c.ru/get.jsp?its=24&addr=3078&d=FDRAOODTFNIZKDAD&dir=BASUOR&file=UPDATE.EXE
		# 4. download tunes
		r, s = dlstr(conn, url)
		if r:
			if len(s) < 100:			# 'Ошибка - неверный номер ИТС!', 'Неверный адрес ключа!', 'Неверный ключ!'
				print s.decode('windows-1251')
			else:
				fn = tunes[i][1] + '.EXE'
				f = open(fn, 'wb')
				f.write(s)
				f.close()
	conn.close()
