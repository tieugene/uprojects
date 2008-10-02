# -*- coding: utf-8 -*-

'''
backup.py - XML Backup & Restore procedures.
'''

from xml.parsers import expat
import data, utility

def	__X(s, mode = False):
	'''
	Prepare given string to xml output.
	@param s:str - string
	@param mode:bool - False = attribute, True = content
	'''
	s = s.replace("&", "&amp;")
	if (mode):
		s = s.replace("<", "&lt;").replace(">", "&gt;")
	else:
		s = s.replace("\"", "&quot;")
	return s

def	U2W(s):
	'''Xcode UTF8 to CP1251'''
	return utility.XCode(s, utility.UTF8, utility.CP1251)

def	Backup(outfile):
	data.DataBase.Exec(data.DataBase.SQL_Select)
	d = data.DataBase.GetAll()
	f = open(outfile, "w")
	f.write(U2W(\
		"<?xml version = '1.0' encoding = 'windows-1251'?>\
		\n<!DOCTYPE db SYSTEM 'jobru.dtd'>\
		\n<db>"))
	for r in d:
		f.write(U2W("\n<rec id=\"%d\" dt=\"%s\" tit=\"%s\" et=\"%d\" epl=\"%s\" cit=\"%s\" sex=\"%d\" af=\"%d\" at=\"%d\" edu=\"%d\" exp=\"%d\" emp=\"%d\" sal=\"%d\" cnt=\"%s\" ph=\"%s\" eml=\"%s\" new=\"%d\" pri=\"%d\"" % (
			r[0], r[1], __X(r[2]), r[3], __X(r[4]), __X(r[5]),
			r[6], r[7], r[8], r[9], r[10], r[11],
			r[12], __X(r[16]), __X(r[17]), __X(r[18]), r[19], r[20]
			)))
		Flag = False
		if (len(r[13])):
			f.write(U2W(">\n<r>%s</r" % __X(r[13], True)))
			Flag = True
		if (len(r[14])):
			f.write(U2W(">\n<d>%s</d" % __X(r[14], True)))
			Flag = True
		if (len(r[15])):
			f.write(U2W(">\n<c>%s</c" % __X(r[15], True)))
			Flag = True
		if (Flag):
			f.write(">\n</rec>")
		else:
			f.write("/>")
	f.write("\n</db>")
	f.close()

def	Restore(infile):
	data.DataBase.KillAll()
	Cfg().Load(infile)

class Cfg:
	'''
	Main Cfg reader class
	'''
	def __init__(self):
		'''
		Constructor.
		@param fname filename of configuration file
		'''
		self.p = expat.ParserCreate()
		self.p.returns_unicode = 0
		self.p.StartElementHandler = self.start_element
		self.p.EndElementHandler = self.end_element
		self.p.CharacterDataHandler = self.char_data
		#
		self.buffer = []
		self.Will = 0
	def start_element(self, name, attrs):
		'''
		start tag catcher
		@param name tag name
		@param attrs dict of tag attributes
		'''
		stackvalue = None
		if (name == 'rec'):
			self.buffer = data.EmptyBuffer[:]
			self.buffer[ 0] = long(attrs['id'])
			self.buffer[ 1] = utility.Iso2DateTime(attrs['dt'])
			self.buffer[ 2] = attrs['tit']
			self.buffer[ 3] = int(attrs['et'])
			self.buffer[ 4] = attrs['epl']
			self.buffer[ 5] = attrs['cit']
			self.buffer[ 6] = int(attrs['sex'])
			self.buffer[ 7] = int(attrs['af'])
			self.buffer[ 8] = int(attrs['at'])
			self.buffer[ 9] = int(attrs['edu'])
			self.buffer[10] = int(attrs['exp'])
			self.buffer[11] = int(attrs['emp'])
			self.buffer[12] = long(attrs['sal'])
			self.buffer[16] = attrs['cnt']
			self.buffer[17] = attrs['ph']
			self.buffer[18] = attrs['eml']
			self.buffer[19] = int(attrs['new'])
			self.buffer[20] = int(attrs['pri'])
			self.Will = 0
		elif (name == 'r'):	# Requirements
			self.Will = 13
		elif (name == 'd'):	# Duty
			self.Will = 14
		elif (name == 'c'):	# 
			self.Will = 15
		else:
			pass
	def end_element(self, name):
		'''
		end tag catcher
		@param name tag name
		'''
		if (name == 'rec'):
##			pass
			data.DataBase.InsertRecord(self.buffer)
	def char_data(self, data):
		'''
		character data catcher
		@param data data themselves - one (!) line per call
		'''
		if (self.Will):
##			if (self.buffer[0] == 17635246):			# DEBUG
##				print utility.XCode(data, utility.UTF8)	# DEBUG
##				print data
			self.buffer[self.Will] = data
			self.Will = 0
	def Load(self, path):
		'''
		Load and parse cfg file.
		@param path (not worx now) requested data.
		@return None (if error occurs) or Global Module text
		'''
		self.p.ParseFile(open(path))
