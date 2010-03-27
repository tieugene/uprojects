# -*- conding: utf-8 -*-
'''
	mxlab.com: kladr.imp
	author: mpenzin@gmail.com
'''

import os, logging; log = logging.getLogger(__name__)

from django.conf import settings
from django.db import connection as conn
from django.db import transaction as trs

import dbf_ro
from models import *

DBF_DIR = os.path.join( settings.MEDIA_ROOT, 'KLADR' )

def imp_socr(f):
	rd = dbf_ro.dbfreader( open(f,'rb') )
	fields, type = rd.next(), rd.next()
	Short.objects.all().delete()
	for dbf_row in rd:
		r = [ unicode( r, 'cp866' ).strip() for r in dbf_row ]
		short = Short.objects.get(name=r[1])
		if (not short):
			short = Short(name=r[1], fullname=r[2])
			short.save()
	rd.close()

def calc_level( code ):
	'''mask: SSRRRGGGPPP'''
	if code[8:11] != '000': return 4
	if code[5:8]  != '000': return 3
	if code[2:5]  != '000': return 2
	return 1
	
def imp_kladr(f):
	rd = dbf_rw.dbfreader( open(f,'rb') )
	print 'file:', f
	
	fields, type = rd.next(), rd.next()
	print 'fields:', map( lambda x, y: str(x)+str(y), fields, type )

	curs = conn.cursor() #@UndefinedVariable
	curs.execute( 'delete from kladr_kladr' )

	line = 0
	for dbf_row in rd:
		line += 1

		r = [ unicode( r, 'cp866' ).strip() for r in dbf_row ]

		curs.execute( 
			"insert into kladr_kladr(code,level,name,socr,stat,indx)"+
			" values (%s,%s,%s,%s,%s,%s)",
			(r[2], calc_level(r[2]), r[0], r[1], r[7], r[3])
		)
		trs.commit_unless_managed()
	print "lines:", line
	rd.close()

def imp_street(f):
	rd = dbf_rw.dbfreader( open(f,'rb') )
	print 'file:', f
	
	fields, type = rd.next(), rd.next()
	print 'fields:', map( lambda x, y: str(x)+str(y), fields, type )

	curs = conn.cursor() #@UndefinedVariable
	curs.execute( 'delete from kladr_street' )

	line = 0
	for dbf_row in rd:
		line += 1

		r = [ unicode( r, 'cp866' ).strip() for r in dbf_row ]

		curs.execute( 
			"insert into kladr_street(code,name,socr,indx)"+
			" values (%s,%s,%s,%s)", (r[2], r[0], r[1], r[3])         
		)
		trs.commit_unless_managed()         
	#-
	print "lines:", line
	rd.close()

def imp_all():
	imp_socr( os.path.join( DBF_DIR, 'SOCRBASE.DBF' ) )
	#imp_kladr( os.path.join( DBF_DIR, 'KLADR.DBF' ) )
	#imp_street( os.path.join( DBF_DIR, 'STREET.DBF' ) )
