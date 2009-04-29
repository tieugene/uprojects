# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

class	OkopfAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'shortname', 'disabled']

class	OkvedAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'disabled']

class	OksoAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'disabled']

class	QualificationAdmin(admin.ModelAdmin):
	list_display = ['id', 'okso', 'qid', 'name']

class	OkdpAdmin(admin.ModelAdmin):
	list_display = ['id', 'name']

class	OkdpGroupAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'hq', 'hs', 'mq', 'ms']

class	Okdp4SROAdmin(admin.ModelAdmin):
	list_display = ['id', 'group']

class	PhoneAdmin(admin.ModelAdmin):
	list_display = ['id', 'country', 'trunk', 'phone', 'ext']

class	EmailAdmin(admin.ModelAdmin):
	list_display = ['URL']

class	EventTypeAdmin(admin.ModelAdmin):
	list_display = ['name', 'comments']

class	RoleAdmin(admin.ModelAdmin):
	list_display = ['name', 'comments']

class	PersonAdmin(admin.ModelAdmin):
	list_display = ['firstname', 'midname', 'lastname']

class	PersonFileAdmin(admin.ModelAdmin):
	list_display = ['person', 'file']

class	OrgAdmin(admin.ModelAdmin):
	list_display = ['name', 'fullname']

class	OrgEventAdmin(admin.ModelAdmin):
	list_display = ['org', 'type']

class	OrgStuffAdmin(admin.ModelAdmin):
	list_display = ['org', 'role']

class	OrgFileAdmin(admin.ModelAdmin):
	list_display = ['org', 'file']

class	MeetingAdmin(admin.ModelAdmin):
	list_display = ['date', 'agenda']

admin.site.register(Okved,	OkvedAdmin)
admin.site.register(Okso,	OksoAdmin)
admin.site.register(Qualification,	QualificationAdmin)
admin.site.register(Okdp,	OkdpAdmin)
admin.site.register(OkdpGroup,	OkdpGroupAdmin)
admin.site.register(Okdp4SRO,	Okdp4SROAdmin)
admin.site.register(Phone,	PhoneAdmin)
admin.site.register(Email,	EmailAdmin)
admin.site.register(EventType,	EventTypeAdmin)
admin.site.register(Role,	RoleAdmin)
admin.site.register(Person,	PersonAdmin)
admin.site.register(Org,	OrgAdmin)
admin.site.register(OrgEvent,	OrgEventAdmin)
admin.site.register(OrgStuff,	OrgStuffAdmin)
admin.site.register(OrgFile,	OrgFileAdmin)
admin.site.register(Meeting,	MeetingAdmin)
