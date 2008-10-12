# -*- coding: cp1251 -*-
'''
parser.py - Parser module.
Parse input html text to array of records.
'''

import sys
from datetime import datetime
from HTMLParser import HTMLParser
import data

class MyHTMLParser(HTMLParser):

	def	LetsGo(self, text):
		'''
		@param text:str - text to parse (cp1251)
		@return list**2 of records
		'''
		self.MaxLen = {				# buffer[#]:(maxlen, name)
			 2:(200, "Title"),
			 4:(200, "Employer"),
			 5:( 50, "City"),
			13:(800, "Requirements"),
			14:(800, "Duty"),
			15:(400, "Conditions"),
			16:(100, "Contact"),
			17:(100, "Phone"),
			18:(100, "E-Mail"),
			}
		self.datalist = []
		self.status = 0
		self.level = 0
		self.row = 0
		self.col = 0
		self.Div = False
		self.Bold = False
		self.Italic = False
		self.InCell = False
		self.WillField = 0
		self.feed(text)
		self.close()
		print self.datalist
		return self.datalist

	def	handle_starttag(self, tag, attrs):
		if (self.status == 0):
			pass
		elif (self.status == 1):			# main table?
			if (tag == "table"):
				self.level += 1
				self.row = 0
				if (self.level == 2):
					self.buffer = data.EmptyBuffer[:]
##					self.buffer[19] = 1	# New
			elif (tag == "tr"):
				self.row += 1
				self.col = 0
			elif (tag == "td"):
				self.col += 1
				self.InCell = True
			elif (tag == "div"):
				self.Div = True
			elif (tag == "b"):
				self.Bold = True
			elif (tag == "i"):
				self.Italic = True
			elif (tag == "br"):
				if (self.WillField == 4):	# GUM: Employer
					self.WillField = 0	# reset
			else:
				pass
		else:
			pass

	def	handle_endtag(self, tag):
		if (self.status == 0):
			if (tag == "table"):
				self.status = 1			# end of 1st table
		elif (self.status == 1):			# main table?
			if (tag == "table"):
				self.level -= 1
				if (self.level == 0):		# end of main table
					self.status = 2
				elif (self.level == 1):
					self.datalist.append(self.buffer)	# add new record
			elif (tag == "tr"):
				pass
			elif (tag == "td"):
				self.InCell = False
			elif (tag == "div"):
				self.Div = False
			elif (tag == "b"):
				self.Bold = False
			elif (tag == "i"):
				self.Italic = False
			else:
				pass
		else:
			pass

	def	handle_data(self, d):
		if ((self.status) and (self.level > 1) and (self.InCell)):
			s = d.strip()
			if len(s):
				self.DataProcess(s)

	def	DataProcess(self, text):
		if (self.level == 2):
			if (self.row == 2):			# Date, Title
				if (not self.Bold):
					date, time = text[:-1].strip().split(" ", 1)
					d, m, y = date.split(".")
					h, mi, s = time.split(":")
					self.buffer[1] = datetime(int(y), int(m), int(d), int(h), int(mi), int(s))	# Date
				else:
					self.buffer[2] = self.__X(text, 2)	# Title
			else:
				if (self.Bold):		# 
					if (text == "Прямой работодатель"):
						self.WillField = 4
						self.buffer[3] = 0
					elif (text == "Кадровое агентство"):
						self.WillField = 4
						self.buffer[3] = 1
					elif (text == "Требования:"):
						self.WillField = 13
					elif (text == "Обязанности:"):
						self.WillField = 14
					elif (text == "Условия:"):
						self.WillField = 15
					elif (text.startswith("Зарплата:")):
						self.buffer[12] = long(text.split(":", 1)[1].lstrip())
					else:
						self.PrintError("2: %s" % text)
				else:
					if (self.WillField):
						if (self.WillField == 4):	# Employer
							text = text[1:].lstrip()
						self.buffer[self.WillField] = self.__X(text, self.WillField)
						self.WillField = 0
					else:
						tmp = text.split(":", 1)
						if len(tmp) > 1:
							key, s = tmp
						else:
							print text
							return
						text = s.strip()
						if (key == "Город"):
							self.buffer[5] = self.__X(text, 5)
						elif (key == "Пол"):
							self.buffer[6] = data.sex2i[text]
						elif (key == "Возраст"):
							age = text.splitlines()
							for a in age:
								as = a.strip()
								if (len(as) == 0):
									pass
								elif (as.startswith("от")):
									self.buffer[7] = int(as[2:].lstrip())
								elif (as.startswith("до")):
									self.buffer[8] = int(as[2:].lstrip())
						elif (key == "Образование"):
							self.buffer[9] = data.edu2i[text]
						elif (key == "Опыт работы"):
							self.buffer[10] = data.exp2i[text]
						elif (key == "Занятость"):
							self.buffer[11] = data.emp2i[text]
						else:
							self.PrintError("3: %s" % s)
		else:						# ID...Contacts
			if (self.col == 1):			# ID
				self.buffer[0] = long(text[12:].lstrip())
			else:
				if (not self.Italic):	# Contact, Phone
					if (text != "E-Mail:"):
						if (text.startswith("Контактное лицо:")):
							self.buffer[16] = self.__X(text.split(":", 1)[1].lstrip(), 16)
						elif (text.startswith("Телефон:")):
							self.buffer[17] = self.__X(text.split(":", 1)[1].lstrip(), 17)
						else:
							self.PrintError("1")
				else:				# Email
					self.buffer[18] = self.__X(text, 18)

	def	PrintError(self, msg):
		print "Error: %s" % msg

	def	__X(self, s, n):
		'''
		XCode input string from cp1251 into koi8-r.
		@param s:str - encoded string
		@param n:int - No in buffer
		'''
		maxl = self.MaxLen[n][0]
		l = len(s)
		if (l > maxl):
			print "W: Field %s is too long: %d chars. Cuted." % (self.MaxLen[n][1].ljust(12), l)
			s = s[:maxl-1]
		return unicode(s, "cp1251").encode("utf8")
