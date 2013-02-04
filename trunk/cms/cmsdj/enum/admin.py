# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *

class	GenderAdmin(admin.ModelAdmin):
	pass

class	PersonAddrTypeAdmin(admin.ModelAdmin):
	pass

class	PersonPhoneTypeAdmin(admin.ModelAdmin):
	pass

class	PersonDocTypeAdmin(admin.ModelAdmin):
	pass

class	PersonCodeTypeAdmin(admin.ModelAdmin):
	pass

admin.site.register(Gender,             GenderAdmin)
admin.site.register(PersonAddrType,	    PersonAddrTypeAdmin)
admin.site.register(PersonPhoneType,    PersonPhoneTypeAdmin)
admin.site.register(PersonDocType,	    PersonDocTypeAdmin)
admin.site.register(PersonCodeType,	    PersonCodeTypeAdmin)
