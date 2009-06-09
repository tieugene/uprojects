# -*- coding: utf-8 -*-
'''
'''

from django.contrib import admin
from models import *

# 1. inlines
class	PolicyCountryInLine(admin.TabularInline):
	model		= PolicyCountry
	extra		= 1

class	PolicyRatioInLine(admin.TabularInline):
	model		= PolicyRatio
	extra		= 1

class	InsuredInLine(admin.TabularInline):
	model		= Insured
	extra		= 1

# 2. Odmins

class	PolicyAdmin(admin.ModelAdmin):
	fieldsets = (
		(None,			{'fields': ('id', 'date', 'state')}),
		(u'Страхователь',	{'fields': ('isorg', 'insurant', 'datebirth', 'address', 'phone')}),
		(u'Срок действия',	{'fields': ('dateeff', 'dateexp', 'days')}),
		(u'Страховая сумма',	{'fields': ('program', 'sumper', 'currency', 'course', 'fixrate', 'rate', 'refusal', 'freeratio', 'premium', 'reward')}),
		(u'Разное',		{'fields': ('terms',)}),
		(u'Выдано',		{'fields': ('issuedate', 'issueplace', 'contractno', 'contractdate', 'attorneyno', 'attorneydate')}),
	)

	list_display	= ('id', 'date', 'sumper', 'dateeff', 'dateexp', 'premium', 'reward', 'state')
	ordering	= ('id', 'date')
	search_fields	= ('id', 'date')
	inlines		= (PolicyCountryInLine, PolicyRatioInLine, InsuredInLine)

admin.site.register(Policy,	PolicyAdmin)
