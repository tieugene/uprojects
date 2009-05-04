#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Preload constant references
'''

import sys, csv, sqlite3

reload(sys)
sys.setdefaultencoding( "utf-8" )

def	__get_bool(s):
	return (s.strip() == '1')

def	__get_int(s):
	return int(s.strip())			if s.strip() else None

def	__get_str(s):
	return unicode(s.strip(), "utf-8")	if s.strip() else None

def	__get_reader(s):
	return csv.reader(open('%s' % s), delimiter='\t')

def	load_okdp(c):
	print 'Loading OKDPs'
	c.execute('DELETE FROM sro_okdp')
	for s in __get_reader('okdp.txt'):
		c.execute('INSERT INTO sro_okdp (id, name) VALUES (?, ?)', (__get_str(s[0]), __get_str(s[1])))

def	load_okopf(c):
	print 'Loading OKOPFs'
	c.execute('DELETE FROM sro_okopf')
	for s in __get_reader('okopf.txt'):
		c.execute('INSERT INTO sro_okopf (id, name, shortname, disabled) VALUES (?, ?, ?, ?)', (__get_int(s[0]), __get_str(s[1]), __get_str(s[2]), __get_bool(s[3])))

def	load_okso(c):
	print 'Loading OKSO'
	c.execute('DELETE FROM sro_okso')
	for s in __get_reader('okso.txt'):
		c.execute('INSERT INTO sro_okso (id, name, disabled) VALUES (?, ?, ?)', (__get_int(s[0]), __get_str(s[1]), False))

def	load_okved(c):
	print 'Loading OKVED'
	c.execute('DELETE FROM sro_okved')
	for s in __get_reader('okved.txt'):
		c.execute('INSERT INTO sro_okved (id, name, disabled) VALUES (?, ?, ?)', (__get_str(s[0]).replace('.', ''), __get_str(s[1]), False))

def	load_skill(c):
	print 'Loading Skills'
	c.execute('DELETE FROM sro_skill')
	curoid = 0
	curqid = 0
	counter = 0
	for s in __get_reader('skill.txt'):
		oid	= __get_int(s[0])	# okso id
		sid	= __get_int(s[1])	# skill id
		name	= __get_str(s[2])
		if ((curoid <> oid) or (curqid <> sid)):
			curoid = oid
			curqid = sid
			counter = 0
		else:
			counter += 1
		id = int('%d%d%d' % (curoid, curqid, counter))
		c.execute('INSERT INTO sro_skill (id, okso_id, skill, name) VALUES (?, ?, ?, ?)', (id, oid, sid, name))

def	load_stage(c):
	print 'Loading Stages'
	c.execute('DELETE FROM sro_stage')
	for s in __get_reader('stage.txt'):
		c.execute('INSERT INTO sro_stage (id, name, hq, hs, mq, ms) VALUES (?, ?, ?, ?, ?, ?)', (__get_str(s[0]), __get_str(s[1]), __get_int(s[2]), __get_int(s[3]), __get_int(s[4]), __get_int(s[5])))

def	load_stageokdp(c):
	print 'Loading Stage OKDPs'
	c.execute('DELETE FROM sro_stageokdp')
	for s in __get_reader('stageokdp.txt'):
		stage	= __get_int(s[0])
		okdp	= __get_str(s[1])
		c.execute('INSERT INTO sro_stageokdp (id, stage_id, okdp_id) VALUES (?, ?, ?)', (int('%d%s' % (stage, okdp)), stage, okdp))

def	load_stageokso(c):
	print 'Loading Stage OKSOs'
	c.execute('DELETE FROM sro_stageokso')
	for s in __get_reader('stageokso.txt'):
		stage	= __get_int(s[0])
		okso	= __get_int(s[1])
		c.execute('INSERT INTO sro_stageokso (id, stage_id, okso_id) VALUES (?, ?, ?)', (int('%d%d' % (stage, okso)), stage, okso))

def	main():
	conn = sqlite3.connect('../lansite/lansite.db')
	c = conn.cursor()
	load_okopf(c)
	load_okved(c)
	load_okso(c)
	load_skill(c)
	load_okdp(c)
	load_stage(c)
	load_stageokdp(c)
	load_stageokso(c)
	c.execute('VACUUM')
	conn.close()

if (__name__ == '__main__'):
	main()
