# -*- coding: utf-8 -*-
'''
TODO:
	* Inlines:	extra, raw_id_fields
	* Ordinar:	raw_id_fields, fields, fieldset
	* Selector: raw_id + readonly - or unicode + del/add + select
'''

from django.contrib import admin
from models import *
from addons.autocomplete.widgets import *
from rfm import ReadOnlyAdminFields

# 1. Inlines
class	OkopfInLine(admin.TabularInline):
	model		= Okopf
	extra		= 1

class	OkvedInLine(admin.TabularInline):
	model		= Okved
	extra		= 1

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
	#raw_id_fields	= ('okdp',)

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

class	PermitInLine(admin.TabularInline):
	list_display	= ('id', 'date')
	model = Permit
	extra = 1

class	PermitStageInLine(admin.TabularInline):
	model = PermitStage
	extra = 1

class	PermitStageJobInLine(admin.TabularInline):
	model = PermitStageJob
	extra = 1

class	OrgPhoneInLine(admin.TabularInline):
	model = OrgPhone
	extra = 1

	def	save_model(self, request, obj, form, change):
		obj.id = int(request.POST['country'] + request.POST['trunk'] + request.POST['phone'])
		obj.save()

class	OrgEmailInLine(admin.TabularInline):
	model = OrgEmail
	extra = 1

class	OrgEventInLine(admin.TabularInline):
	model = OrgEvent
	extra = 1
	
class	OrgEventStageInLine(admin.TabularInline):
	model = OrgEventStage
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
	ordering	= ('id',)
	search_fields	= ('name',)
	inlines		= (OkvedInLine,)

class	OksoAdmin(admin.ModelAdmin):
	list_display	= ('id', 'name')
	ordering	= ('id',)
	search_fields	= ('name',)
	inlines		= (SkillInLine,)

class	SkillAdmin(admin.ModelAdmin):
	list_display = ('id', 'okso', 'skill', 'name')
	raw_id_fields	= ('okso',)

class	StageAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'hq', 'hs', 'mq', 'ms')
	inlines = (StageOksoInLine, JobInLine,)

class	EventTypeAdmin(admin.ModelAdmin):
	list_display = ('name', 'comments')

class	RoleAdmin(admin.ModelAdmin):
	list_display = ('name', 'comments')

class	PersonAdmin(admin.ModelAdmin):
	list_display = ('firstname', 'midname', 'lastname')
	inlines = (PersonSkillInLine, OrgStuffInLine, PersonFileInLine,)
	raw_id_fields	= ('skills',)
	#related_search_fields = {
	#	'skills': ('^id', 'name'),
	#}

class	OrgAdmin(admin.ModelAdmin):
	list_display = ('name', 'fullname')
	inlines = (OrgOkvedInLine, OrgPhoneInLine, OrgEmailInLine, OrgStuffInLine, OrgEventInLine, PermitInLine, OrgFileInLine)
	raw_id_fields	= ('okveds',)
	#related_search_fields = {
	#	'okveds': ('^id',),
	#}

class	PermitAdmin(admin.ModelAdmin):
	list_display	= ('id', 'date', 'org')
	list_filter	= ('org',)
	inlines		= (PermitStageInLine,)

class	PermitStageAdmin(admin.ModelAdmin):
	list_display = ('permit', 'stage')
	#list_filter = ('org',)
	#filter_horizontal = ('jobs',)
	inlines = (PermitStageJobInLine,)

class	OrgEventAdmin(admin.ModelAdmin):
	list_display = ('org', 'type')
	list_filter = ('org',)
	inlines = (OrgEventStageInLine,)

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
admin.site.register(Stage,		StageAdmin)
admin.site.register(EventType,		EventTypeAdmin)
admin.site.register(Role,		RoleAdmin)
admin.site.register(Person,		PersonAdmin)
admin.site.register(Org,		OrgAdmin)
admin.site.register(Permit,		PermitAdmin)
admin.site.register(PermitStage,	PermitStageAdmin)
admin.site.register(OrgEvent,		OrgEventAdmin)
admin.site.register(File,		FileAdmin)
admin.site.register(Meeting,		MeetingAdmin)
