# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from models import *

# 1. Inlines
class	KladrInLine(admin.TabularInline):
	model = Kladr
	extra = 0

# 2. Odmins
class	ShortAdmin(admin.ModelAdmin):
	list_display	= ('id', 'name', 'fullname')
	ordering	= ('name',)
	search_fields	= ('name',)

class	StateTypeAdmin(admin.ModelAdmin):
	list_display	= ('id', 'comments')
	ordering	= ('id',)
	search_fields	= ('id',)

class	KladrAdmin(admin.ModelAdmin):
	list_display	= ('id', 'name')
	ordering	= ('id',)
	search_fields	= ('name',)
	inlines		= (KladrInLine,)

admin.site.register(Short,	ShortAdmin)
admin.site.register(StateType,	StateTypeAdmin)
admin.site.register(Kladr,	KladrAdmin)
