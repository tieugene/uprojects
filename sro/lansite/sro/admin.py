# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

class	OrgAdmin(admin.ModelAdmin):
	list_display = ['name', 'fullname']

admin.site.register(Org,	OrgAdmin)
