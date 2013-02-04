# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *

class	PersonAdmin(admin.ModelAdmin):
	ordering	= ('lastname', 'firstname', 'midname',)
	list_display	= ('lastname', 'firstname', 'midname',)

admin.site.register(Person,	PersonAdmin)
