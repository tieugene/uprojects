# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *

class	EmployeeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Employee,	EmployeeAdmin)
