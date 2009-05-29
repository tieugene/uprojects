# -*- coding: utf-8 -*-
'''
TODO:
	* Inlines:	extra, raw_id_fields
	* Ordinar:	raw_id_fields, fields, fieldset
	* Selector: raw_id + readonly - or unicode + del/add + select
'''

from django.contrib import admin
from models import *
#from addons.autocomplete.widgets import *
from rfm import ReadOnlyAdminFields

# 1. inlines
class	OkopfInLine(admin.TabularInline):
	model		= Okopf
	extra		= 0
#	inlines		= [OkopfInLine,]

class	SkillInLine(admin.TabularInline):
	model		= Skill
	extra		= 1
	raw_id_fields	= ('okso',)

class	StageOksoInLine(admin.TabularInline):
	model		= StageOkso
	extra		= 1
	raw_id_fields	= ('stage', 'okso',)

class	JobInLine(admin.TabularInline):
	model		= Job
	extra		= 1
	raw_id_fields	= ('okdp',)

class	PersonSkillInLine(admin.TabularInline):
	model		= PersonSkill
	extra		= 1
	raw_id_fields	= ('skill',)

class	PersonFileInLine(admin.TabularInline):
	model		= PersonFile
	extra		= 1

class	OrgOkvedInLine(admin.TabularInline):
	model		= OrgOkved
	extra		= 1
	raw_id_fields	= ('okved',)

class	OrgLOkdpInLine(admin.TabularInline):
	model	= OrgLOkdp
	extra	= 1
	raw_id_fields	= ('okdp',)

class	OrgStageInLine(admin.TabularInline):
	model = OrgStage
	extra = 1

class	OrgJobInLine(admin.TabularInline):
	model = OrgJob
	extra = 1

class	OrgPhoneInLine(admin.TabularInline):
	model = OrgPhone
	extra = 1

class	OrgEmailInLine(admin.TabularInline):
	model = OrgEmail
	extra = 1

class	OrgEventInLine(admin.TabularInline):
	model = OrgEvent
	extra = 1
	
class	OrgEventStageInLine(admin.TabularInline):
	model = OrgEventStage
	extra = 1
	
class	OrgEventJobInLine(admin.TabularInline):
	model = OrgEventJob
	extra = 1
	
class	OrgStuffInLine(admin.TabularInline):
	model = OrgStuff
	extra = 1

class	OrgFileInLine(ReadOnlyAdminFields, admin.TabularInline):
	model = OrgFile
	extra = 1
	readonly = ('org',)

class	MeetingOrgInLine(admin.TabularInline):
	model = MeetingOrg
	extra = 1
	
# 2. Odmins

class	OkopfAdmin(admin.ModelAdmin):
	list_display	= ('id', 'name', 'shortname', 'disabled')
	ordering	= ('id',)
	search_fields	= ('shorname',)
	inlines		= (OkopfInLine,)
	#raw_id_fields	= ('parent',)

class	OkvedAdmin(admin.ModelAdmin):
	list_display	= ('id', 'name', 'disabled')

class	OksoAdmin(admin.ModelAdmin):
	list_display	= ('id', 'name', 'disabled')
	ordering	= ('id',)
	search_fields	= ('name',)
	inlines		= (SkillInLine,)

class	SkillAdmin(admin.ModelAdmin):
	list_display = ('id', 'okso', 'skill', 'name')
	raw_id_fields	= ('okso',)

class	OkdpAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')

class	StageAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'hq', 'hs', 'mq', 'ms')
	inlines = (JobInLine,)

class	PhoneAdmin(admin.ModelAdmin):
	list_display = ('id', 'country', 'trunk', 'phone', 'ext')
	fields = ('country', 'trunk', 'phone', 'ext')

	def	save_model(self, request, obj, form, change):
		obj.id = int(request.POST['country'] + request.POST['trunk'] + request.POST['phone'])
		obj.save()

class	EmailAdmin(admin.ModelAdmin):
	list_display = ('URL',)

class	EventTypeAdmin(admin.ModelAdmin):
	list_display = ('name', 'comments')

class	RoleAdmin(admin.ModelAdmin):
	list_display = ('name', 'comments')

class	PersonAdmin(admin.ModelAdmin):
	list_display = ('firstname', 'midname', 'lastname')
	inlines = (PersonSkillInLine, OrgStuffInLine, PersonFileInLine,)
	#fields = ('firstname', 'midname', 'lastname', 'skills', 'files')
	#filter_horizontal = ('firstname',), filter_vertical
	#fieldsets = (
	#	(None, {
	#		'fields': ('firstname', 'midname', 'lastname')
	#	}),
	#	(u'Разное', {
	#		'classes': ('collapse',),
	#		'fields': ('skills', 'files',)
	#	}),
	#)

#class	PersonAdmin(AutocompleteModelAdmin):
#	list_display = ('firstname', 'midname', 'lastname')
#	inlines = (OrgStuffInLine, PersonFileInLine,)
#	related_search_fields = { 
#		'skill': ('skill',),
#       }
	
#class	PersonSkillAdmin(admin.ModelAdmin):
#	list_display = ('person', 'skill')

#class	PersonFileAdmin(admin.ModelAdmin):
#	list_display = ('person', 'file')

class	OrgAdmin(admin.ModelAdmin):
	list_display = ('name', 'fullname')
	inlines = (OrgOkvedInLine, OrgLOkdpInLine, OrgStageInLine, OrgPhoneInLine, OrgEmailInLine, OrgStuffInLine, OrgFileInLine, OrgEventInLine)
	#raw_id_fields	= ('okopf',)

class	OrgStageAdmin(admin.ModelAdmin):
	list_display = ('org', 'stage')
	list_filter = ('org',)
	#prepopulated_fields = {"org": ("org",)}
	#fields = (,)
	filter_horizontal = ('jobs',)
	inlines = (OrgJobInLine,)

class	OrgEventAdmin(admin.ModelAdmin):
	list_display = ('org', 'type')
	list_filter = ('org',)
	inlines = (OrgEventStageInLine,)

#class	OrgStuffAdmin(admin.ModelAdmin):
#	list_display = ('org', 'role')

#class	OrgFileAdmin(admin.ModelAdmin):
#	list_display = ('org', 'file')
#	inlines = (OrgFileInLine, PersonFileInLine)

class	FileAdmin(ReadOnlyAdminFields, admin.ModelAdmin):
	list_display = ('name', 'comments', 'saved', 'mime')
	inlines = (PersonFileInLine, OrgFileInLine,)
	readonly = ('name', 'mime')

class	MeetingAdmin(admin.ModelAdmin):
	list_display = ('date', 'agenda')
	inlines = (MeetingOrgInLine,)
	date_hierarchy = 'date'

admin.site.register(Okopf,		OkopfAdmin)
admin.site.register(Okved,		OkvedAdmin)
admin.site.register(Okso,		OksoAdmin)
admin.site.register(Skill,		SkillAdmin)
admin.site.register(Okdp,		OkdpAdmin)
admin.site.register(Stage,		StageAdmin)
admin.site.register(Phone,		PhoneAdmin)
admin.site.register(Email,		EmailAdmin)
admin.site.register(EventType,		EventTypeAdmin)
admin.site.register(Role,		RoleAdmin)
admin.site.register(Person,		PersonAdmin)
#admin.site.register(PersonSkill,	PersonSkillAdmin)
#admin.site.register(PersonFile,		PersonFileAdmin)
admin.site.register(Org,		OrgAdmin)
admin.site.register(OrgStage,		OrgStageAdmin)
admin.site.register(OrgEvent,		OrgEventAdmin)
#admin.site.register(OrgStuff,		OrgStuffAdmin)
#admin.site.register(OrgFile,		OrgFileAdmin)
admin.site.register(File,		FileAdmin)
admin.site.register(Meeting,		MeetingAdmin)
