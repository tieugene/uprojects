# -*- coding: utf-8 -*-
'''
TODO:
	* Inlines:	extra, raw_id_fields
	* Ordinar:	raw_id_fields, fields, fieldset
	* Selector: raw_id + readonly - or unicode + del/add + select
'''

from django.contrib import admin
from models import *
from rfm import ReadOnlyAdminFields

# 1. Inlines
class	OkopfInLine(admin.TabularInline):
	model		= Okopf
	extra		= 1

class	OkvedInLine(admin.TabularInline):
	model		= Okved
	extra		= 1

class	SpecialityInLine(admin.TabularInline):
	model		= Speciality
	extra		= 1

class	SkillInLine(admin.TabularInline):
	model		= Skill
	extra		= 1

class	StageInLine(admin.TabularInline):
	model		= Stage
	extra		= 1

class	JobInLine(admin.TabularInline):
	model		= Job
	extra		= 1

class	PersonSkillInLine(admin.TabularInline):
	model		= PersonSkill
	extra		= 1
	#raw_id_fields	= ('skill',)

class	PersonFileInLine(admin.TabularInline):
	model		= PersonFile
	extra		= 1

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

class	OrgOkvedInLine(admin.TabularInline):
	model		= OrgOkved
	extra		= 1
	raw_id_fields	= ('okved',)

class	OrgPhoneInLine(admin.TabularInline):
	model = OrgPhone
	extra = 1
	#def	save_model(self, request, obj, form, change):
	#	obj.id = int(request.POST['country'] + request.POST['trunk'] + request.POST['phone'])
	#	obj.save()

class	OrgEmailInLine(admin.TabularInline):
	model = OrgEmail
	extra = 1

class	OrgWWWInLine(admin.TabularInline):
	model = OrgWWW
	extra = 1

class	OrgStuffInLine(admin.TabularInline):
	model = OrgStuff
	extra = 1

class	OrgEventInLine(admin.TabularInline):
	model = OrgEvent
	extra = 1
	
class	OrgFileInLine(ReadOnlyAdminFields, admin.TabularInline):
	model = OrgFile
	extra = 1
	readonly = ('org',)

class	OrgLicenseInLine(admin.TabularInline):
	model = OrgLicense
	extra = 1

class	OrgInsuranceInLine(admin.TabularInline):
	model = OrgInsurance
	extra = 1

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
	list_display	= ('id', 'name')
	ordering	= ('id',)
	search_fields	= ('name',)
	inlines		= (OkvedInLine,)

class	SpecialityAdmin(admin.ModelAdmin):
	list_display	= ('name',)
	ordering	= ('name',)
	search_fields	= ('name',)

class	SkillAdmin(admin.ModelAdmin):
	list_display	= ('name',)
	ordering	= ('name',)
	search_field	= ('name',)
	#raw_id_fields	= ('okso',)

class	StageAdmin(admin.ModelAdmin):
	list_display	= ('id', 'name', 'hq', 'hs', 'mq', 'ms')
	ordering	= ('id', 'name')
	inlines		= (JobInLine,)

class	EventTypeAdmin(admin.ModelAdmin):
	list_display	= ('name', 'comments')
	ordering	= ('name',)

class	RoleAdmin(admin.ModelAdmin):
	list_display	= ('name', 'comments')
	ordering	= ('name',)

class	PersonAdmin(admin.ModelAdmin):
	list_display	= ('firstname', 'midname', 'lastname')
	ordering	= ('firstname', 'midname', 'lastname')
	inlines		= (PersonSkillInLine, OrgStuffInLine, PersonFileInLine,)
	#raw_id_fields	= ('skills',)
	#related_search_fields = {
	#	'skills': ('^id', 'name'),
	#}

class	OrgAdmin(admin.ModelAdmin):
	list_display	= ('name', 'fullname')
	ordering	= ('name',)
	inlines		= (OrgOkvedInLine, OrgPhoneInLine, OrgEmailInLine, OrgWWWInLine, OrgStuffInLine, PermitInLine, OrgEventInLine, OrgFileInLine, OrgLicenseInLine, OrgInsuranceInLine)
	raw_id_fields	= ('okveds',)
	#related_search_fields = {
	#	'okveds': ('^id',),
	#}

class	PermitAdmin(admin.ModelAdmin):
	list_display	= ('org', 'regno', 'date',)
	list_filter	= ('org',)
	ordering	= ('org', 'regno',)
	inlines		= (PermitStageInLine,)

class	PermitStageAdmin(admin.ModelAdmin):
	list_display	= ('permit', 'stage')
	list_filter	= ('permit',)
	ordering	= ('permit', 'stage',)
	#filter_horizontal = ('jobs',)
	inlines = (PermitStageJobInLine,)

class	OrgEventAdmin(admin.ModelAdmin):
	list_display	= ('org', 'type',)
	list_filter	= ('org', 'type',)
	ordering	= ('org', 'type',)

class	FileAdmin(ReadOnlyAdminFields, admin.ModelAdmin):
	list_display = ('name', 'comments', 'saved', 'mime')
	inlines = (PersonFileInLine, OrgFileInLine,)
	readonly = ('name', 'mime')

class	MeetingAdmin(admin.ModelAdmin):
	list_display = ('regno', 'date', 'common', 'agenda')
	inlines = (MeetingOrgInLine,)
	date_hierarchy = 'date'

admin.site.register(Okopf,		OkopfAdmin)
admin.site.register(Okved,		OkvedAdmin)
admin.site.register(Speciality,		SpecialityAdmin)
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
