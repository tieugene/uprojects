# -*- coding: utf-8 -*-

'''
xmlimpex.py - XML Backup & Restore procedures.
'''

from PyQt4 import QtCore, QtGui, QtXml
import data, utility, model

def	__X(s, mode = False):
	'''
	Prepare given string to xml output.
	@param s:string - string
	@param mode:bool - False = attribute, True = content
	'''
	s = s.replace("&", "&amp;")
	if (mode):
		s = s.replace("<", "&lt;").replace(">", "&gt;")
	else:
		s = s.replace("\"", "&quot;")
	return s

def	Export(outfile):
	data.DataBase.Exec(data.DataBase.SQL_Select)
	d = data.DataBase.GetAll()
	f = open(outfile, "w")
	f.write(\
		"<?xml version = '1.0' encoding = 'utf-8'?>\
		\n<!DOCTYPE db SYSTEM 'jobru.dtd'>\
		\n<db>")
	for r in d:
		f.write("\n<rec id=\"%d\" dt=\"%s\" tit=\"%s\" et=\"%d\" epl=\"%s\" cit=\"%s\" sex=\"%d\" af=\"%d\" at=\"%d\" edu=\"%d\" exp=\"%d\" emp=\"%d\" sal=\"%d\" cnt=\"%s\" ph=\"%s\" eml=\"%s\" new=\"%d\" pri=\"%d\"" % (
			r[0], r[1], __X(r[2]), r[3], __X(r[4]), __X(r[5]),
			r[6], r[7], r[8], r[9], r[10], r[11],
			r[12], __X(r[16]), __X(r[17]), __X(r[18]), r[19], r[20]
			))
		Flag = False
		if (len(r[13])):
			f.write(">\n<r>%s</r" % __X(r[13], True))
			Flag = True
		if (len(r[14])):
			f.write(">\n<d>%s</d" % __X(r[14], True))
			Flag = True
		if (len(r[15])):
			f.write(">\n<c>%s</c" % __X(r[15], True))
			Flag = True
		if (Flag):
			f.write(">\n</rec>")
		else:
			f.write("/>")
	f.write("\n</db>")
	f.close()

class	JobRuHandler(QtXml.QXmlDefaultHandler):
	def __init__(self, mod):
		QtXml.QXmlDefaultHandler.__init__(self)
		self.errorStr = QtCore.QString()
		self.mod = mod
		self.metJobRuTag = False

	def startElement(self, namespaceURI, localName, qName, attrs):
		if not self.metJobRuTag and qName != "jobru":
			self.errorStr = QtGui.qApp.tr("The file is not an JobRu backup file.")
			return False
		if (qName == "jobru"):
			version = attrs.value("version")
			if not version.isEmpty() and version != "1.0":
				print "bad version"
				self.errorStr = QtGui.qApp.tr("The File is not an JobRu version 1.0 file.")
				return False
			self.__Will = 0
			self.metJobRuTag = True
		# >>>
		elif (qName == 'rec'):
			self.buffer = data.EmptyBuffer[:]
			self.buffer[ 0] = attrs.value('id')		# long
			self.buffer[ 1] = QtCore.QDateTime().fromString(attrs.value('dt'), "yyyy-MM-dd hh:mm:ss")
			self.buffer[ 2] = attrs.value('tit')
			self.buffer[ 3] = attrs.value('et')		# int
			self.buffer[ 4] = attrs.value('epl')
			self.buffer[ 5] = attrs.value('cit')
			self.buffer[ 6] = attrs.value('sex')	# int
			self.buffer[ 7] = attrs.value('af')		# int
			self.buffer[ 8] = attrs.value('at')		# int
			self.buffer[ 9] = attrs.value('edu')	# int
			self.buffer[10] = attrs.value('exp')	# int
			self.buffer[11] = attrs.value('emp')	# int
			self.buffer[12] = attrs.value('sal')	# long
			self.buffer[13] = QtCore.QString()
			self.buffer[14] = QtCore.QString()
			self.buffer[15] = QtCore.QString()
			self.buffer[16] = attrs.value('cnt')
			self.buffer[17] = attrs.value('ph')
			self.buffer[18] = attrs.value('eml')
			self.buffer[19] = attrs.value('new')	# int
			self.buffer[20] = attrs.value('pri')	# int
			self.__Will = 0
		elif (qName == 'r'):	# Requirements
			self.__Will = 13
		elif (qName == 'd'):	# Duty
			self.__Will = 14
		elif (qName == 'c'):	# 
			self.__Will = 15
		else:
			self.errorStr = QtGui.qApp.tr("Unknown tag <%s>." % qName)
			return False
		# <<<
		return True

	def endElement(self, namespaceURI, localName, qName):
		if (qName == 'rec'):
			return model.AddRecord(self.mod, self.buffer)
		return True

	def characters(self, txt):
		if (self.__Will):
			self.buffer[self.__Will] += txt
			self.__Will = 0
		return True

	def fatalError(self, exception):	# parent = self.treeWidget.window()
		QtGui.QMessageBox.information(None,
					QtGui.qApp.tr("SAX JobRu4 Backup"),
					QtGui.qApp.tr("Parse error at line %1, column %2 :\n%3")
							.arg(exception.lineNumber())
							.arg(exception.columnNumber())
							.arg(exception.message()))
		return False

	def errorString(self):
		return self.errorStr

def Import(widget, mod, fileName):
	# 2. prepare parser
	handler = JobRuHandler(mod)
	reader = QtXml.QXmlSimpleReader()
	reader.setContentHandler(handler)
	reader.setErrorHandler(handler)
	# 3. open file
	file = QtCore.QFile(fileName)
	if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
		QtGui.QMessageBox.warning(widget, widget.tr("JobRu backup"),
					widget.tr("Cannot read file %1:\n%2.")
						.arg(fileName)
						.arg(file.errorString()))
		return False
	# 4. parse
	xmlInputSource = QtXml.QXmlInputSource(file)
	model.BeginMassAdd(mod)
	if reader.parse(xmlInputSource):
		retvalue = model.CommitMassAdd(mod)
	else:
		retvalue = model.RollbackMassAdd(mod)
	return retvalue
