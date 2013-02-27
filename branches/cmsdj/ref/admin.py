# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# 1. inlines
class   PMU3Line(admin.TabularInline):
    model   = PMU3

# 2. Ordinar
class	PMU1Admin(admin.ModelAdmin):
    ordering	    = ('id',)
    list_display	= ('id', 'name',)
    inlines         = (PMU3Line,)

class	PMU2Admin(admin.ModelAdmin):
    ordering	    = ('id',)
    list_display	= ('id', 'name',)
    inlines         = (PMU3Line,)

admin.site.register(PMU1,   PMU1Admin)
admin.site.register(PMU2,   PMU2Admin)
admin.site.register(PMU3)
