# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# 1. inlines
class   PersonAddressLine(admin.TabularInline):
    model   = PersonAddress
    extra   = 1

class   PersonPhoneLine(admin.TabularInline):
    model   = PersonPhone
    extra   = 1

class   PersonEmailLine(admin.TabularInline):
    model   = PersonEmail
    extra   = 1

class   PersonDocumentLine(admin.TabularInline):
    model   = PersonDocument
    extra   = 1

class   PersonCodeLine(admin.TabularInline):
    model   = PersonCode
    extra   = 1

# 2. Ordinar
class	PersonAdmin(admin.ModelAdmin):
    ordering	    = ('lastname', 'firstname', 'midname',)
    list_display	= ('lastname', 'firstname', 'midname',)
    #Unicode error
    #inlines         = (PersonPhoneLine,)
    inlines         = (PersonAddressLine, PersonPhoneLine, PersonEmailLine, PersonDocumentLine, PersonCodeLine,)

#admin.site.register(PersonAddress)
#admin.site.register(PersonPhone)
#admin.site.register(PersonEmail)
#admin.site.register(PersonDocument)
#admin.site.register(PersonCode)
admin.site.register(Person, PersonAdmin)
