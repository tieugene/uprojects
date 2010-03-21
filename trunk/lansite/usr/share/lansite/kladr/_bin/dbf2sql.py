#!/bin/env python
# -*- coding: utf-8 -*-

'''
Converts KLADR's DBFs into sql string
'''
import os, sys, struct, datetime, decimal, itertools

reload(sys)
sys.setdefaultencoding("utf-8")

def	__dbfreader(f):
	"""Returns an iterator over records in a Xbase DBF file.
	The first row returned contains the field names.
	The second row contains field specs: (type, size, decimal places).
	Subsequent rows contain the data records.
	If a record is marked as deleted, it is skipped.
	File should be opened for binary reads.
	"""

	numrec, lenheader = struct.unpack('<xxxxLH22x', f.read(32))    
	numfields = (lenheader - 33) // 32

	fields = []
	for unused_fieldno in xrange(numfields):
		name, typ, size, deci = struct.unpack('<11sc4xBB14x', f.read(32))
		name = name.replace('\0', '')       # eliminate NULs from string   
		fields.append((name, typ, size, deci))
	yield [field[0] for field in fields]
	yield [tuple(field[1:]) for field in fields]

	terminator = f.read(1)
	assert terminator == '\r'

	fields.insert(0, ('DeletionFlag', 'C', 1, 0))
	fmt = ''.join(['%ds' % fieldinfo[2] for fieldinfo in fields])
	fmtsiz = struct.calcsize(fmt)
	for unused in xrange(numrec):
		record = struct.unpack(fmt, f.read(fmtsiz))
		if record[0] != ' ':
			continue                        # deleted record
		result = []
		for (name, typ, size, deci), value in itertools.izip(fields, record):
			if name == 'DeletionFlag':
				continue
			if typ == "N":
				value = value.replace('\0', '').lstrip()
				if value == '':
					value = 0
				elif deci:
					value = decimal.Decimal(value)
				else:
					value = int(value)
			elif typ == 'D':
				y, m, d = int(value[:4]), int(value[4:6]), int(value[6:8])
				value = datetime.date(y, m, d)
			elif typ == 'L':
				value = (value in 'YyTt' and 'T') or (value in 'NnFf' and 'F') or '?'
			result.append(value)
		yield result

def	__statetype():
	print u'DELETE FROM kladr_statetype'
	print u'INSERT INTO kladr_statetype (id, comments) VALUES (1, "Центр района");'
	print u'INSERT INTO kladr_statetype (id, comments) VALUES (2, "Центр региона");'
	print u'INSERT INTO kladr_statetype (id, comments) VALUES (3, "Центр района и региона");'
	print u'INSERT INTO kladr_statetype (id, comments) VALUES (4, "Центральный район");'

def	__short(path):
	print u'DELETE FROM kladr_short'
	rd = __dbfreader( open(os.path.join( path, 'SOCRBASE.DBF' ), 'rb') )
	fields, type = rd.next(), rd.next()
	short = dict()
	counter = 1
	for dbf_row in rd:
		r = [ unicode( r, 'cp866' ).strip() for r in dbf_row ]
		if (not short.has_key(r[1])):
			print u'INSERT INTO kladr_short (id, name, fullname) VALUES (%d, "%s", "%s");' % (counter, r[1], r[2])
			short[r[1]] = counter
			counter += 1
	rd.close()
	return short

def	__calc_level( code ):
	'''mask: SSRRRGGGPPP'''
	if code[8:11] != '000': return 4
	if code[5:8]  != '000': return 3
	if code[2:5]  != '000': return 2
	return 1

def	__kladr(path, short):
	print u'DELETE FROM kladr_kladr'
	rd = __dbfreader( open(os.path.join( path, 'KLADR.DBF' ), 'rb') )
	fields, type = rd.next(), rd.next()
	for dbf_row in rd:
		r = [ unicode( r, 'cp866' ).strip() for r in dbf_row ]
		if ((r[2][11:]) == '00'):			# actual
			level = __calc_level(r[2])
			zip = r[3] if (r[3]) else 'NULL'
			state = r[7] if int(r[7]) else 'NULL'
			if (level == 1):
				parent = 'NULL'
			else:
				a = (level * 3) - 4
				parent = r[2][:a] + '000' + r[2][a+3:] + '00'
			print u'INSERT INTO kladr_kladr (id, parent_id, name, short_id, level, zip, okato, center_id) VALUES (%s, %s, "%s", %d, %d, %s, %s, %s);' % (r[2] + '00', parent, r[0], short[r[1]], level, zip, r[6], state)

def	__street(path, short):
	rd = __dbfreader( open(os.path.join( path, 'STREET.DBF' ), 'rb') )
	fields, type = rd.next(), rd.next()
	for dbf_row in rd:
		r = [ unicode( r, 'cp866' ).strip() for r in dbf_row ]
		if ((r[2][15:]) == '00'):			# actual
			zip = r[3] if (r[3]) else 'NULL'
			print u'INSERT INTO kladr_kladr (id, parent_id, name, short_id, level, zip, okato, center_id) VALUES (%s, %s, "%s", %d, 5, %s, %s, NULL);' % (r[2][:15], r[2][:11] + '0000', r[0], short[r[1]], zip, r[6])

if (len(sys.argv) != 1):
        print "Usage: %s" % sys.argv[0]
else:
	dbpath = '/mnt/shares/lansite/media/KLADR'
	print u'BEGIN;'
	__statetype()
	print >> sys.stderr, "short"
	short = __short(dbpath)
	print >> sys.stderr, "kladr"
	__kladr(dbpath, short)
	print >> sys.stderr, "street"
	__street(dbpath, short)
	print u'COMMIT;'
	print u'VACUUM;'
