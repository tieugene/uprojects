# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

class	PersonAddressInLine(admin.TabularInline):
	model = PersonAddress
	extra = 1

class	PersonPhoneInLine(admin.TabularInline):
	model = PersonPhone
	extra = 1

class	PersonEmailInLine(admin.TabularInline):
	model = PersonEmail
	extra = 1

class	PersonIMInLine(admin.TabularInline):
	model = PersonIM
	extra = 1

class	OrgAddressInLine(admin.TabularInline):
	model = OrgAddress
	extra = 1

class	OrgPhoneInLine(admin.TabularInline):
	model = OrgPhone
	extra = 1

class	OrgEmailInLine(admin.TabularInline):
	model = OrgEmail
	extra = 1

class	OrgIMInLine(admin.TabularInline):
	model = OrgIM
	extra = 1

class	OrgPersonInLine(admin.TabularInline):
	model = OrgPerson
	extra = 1

#	----
class	AddressAdmin(admin.ModelAdmin):
	list_display = ('name',)
	inlines = (PersonAddressInLine, OrgAddressInLine)

class	PhoneAdmin(admin.ModelAdmin):
	list_display = ('id', 'country', 'trunk', 'phone', 'ext')
	inlines = (PersonPhoneInLine, OrgPhoneInLine)

class	EmailAdmin(admin.ModelAdmin):
	list_display = ('URL',)
	inlines = (PersonEmailInLine, OrgEmailInLine)

class	IMAdmin(admin.ModelAdmin):
	list_display = ('URL',)
	inlines = (PersonIMInLine, OrgIMInLine)

class	PersonAdmin(admin.ModelAdmin):
	list_display = ('firstname', 'midname', 'lastname')
	inlines = (PersonAddressInLine, PersonPhoneInLine, PersonEmailInLine, PersonIMInLine)

class	OrgAdmin(admin.ModelAdmin):
	list_display = ('shortname', 'longname')
	inlines = (OrgAddressInLine, OrgPhoneInLine, OrgEmailInLine, OrgIMInLine, OrgPersonInLine)

admin.site.register(Address,	AddressAdmin)
admin.site.register(Phone,	PhoneAdmin)
admin.site.register(Email,	EmailAdmin)
admin.site.register(IM,		IMAdmin)
admin.site.register(Person,	PersonAdmin)
admin.site.register(Org,	OrgAdmin)
