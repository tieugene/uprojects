# -*- coding: utf-8 -*-
'''
todo
'''

from django import forms
from django.contrib import admin
from models import *
'''
# 1. Inlines
class	InsurerInLine(admin.TabularInline):
	model		= Insurer
	extra		= 1

class	OkatoInLine(admin.TabularInline):
	model		= Okato
	extra		= 1

class	OkopfInLine(admin.TabularInline):
	model		= Okopf
	extra		= 1

class	OkvedInLine(admin.TabularInline):
	model		= Okved
	extra		= 1

class	SroTypeInLine(admin.TabularInline):
	model		= SroType
	extra		= 1

class	SroInLine(admin.TabularInline):
	model		= Sro
	extra		= 1

class	StageInLine(admin.TabularInline):
	model		= Stage
	extra		= 1

class	JobInLine(admin.TabularInline):
	model		= Job
	extra		= 1

class	SpecialityInLine(admin.TabularInline):
	model		= Speciality
	extra		= 1

class	SpecialityStageInLine(admin.TabularInline):
	model		= SpecialityStage
	extra		= 1

class	SkillInLine(admin.TabularInline):
	model		= Skill
	extra		= 1

class	EventTypeInLine(admin.TabularInline):
	model		= EventType
	extra		= 1

class	RoleInLine(admin.TabularInline):
	model		= Role
	extra		= 1

class	PersonInLine(admin.TabularInline):
	model		= Person
	extra		= 1

class	PersonSkillInLine(admin.TabularInline):
	model		= PersonSkill
	extra		= 1

class	OrgInLine(admin.TabularInline):
	model		= Org
	extra		= 1

class	OrgOkvedInLine(admin.TabularInline):
	model		= OrgOkved
	extra		= 1
	raw_id_fields	= ('okved',)

class	OrgPhoneInLine(admin.TabularInline):
	model = OrgPhone
	extra = 1

class	OrgEmailInLine(admin.TabularInline):
	model = OrgEmail
	extra = 1

class	OrgWWWInLine(admin.TabularInline):
	model = OrgWWW
	extra = 1

class	OrgStuffInLine(admin.TabularInline):
	model = OrgStuff
	extra = 1

class	OrgSroInLine(admin.TabularInline):
	model = OrgSro
	extra = 1

class	OrgEventInLine(admin.TabularInline):
	model = OrgEvent
	extra = 1

class	OrgLicenseInLine(admin.TabularInline):
	model = OrgLicense
	extra = 1

class	OrgInsuranceInLine(admin.TabularInline):
	model = OrgInsurance
	extra = 1

class	ProtocolInLine(admin.TabularInline):
	model = Protocol
	extra = 1

class	StageListTypeInLine(admin.TabularInline):
	model = StageListType
	extra = 1

class	StageListInLine(admin.TabularInline):
	model = StageList
	extra = 1

class	PermitStageInLine(admin.TabularInline):
	model = PermitStage
	extra = 1

class	PermitStageJobInLine(admin.TabularInline):
	model = PermitStageJob
	extra = 1

class	StatementInLine(admin.TabularInline):
	model = Statement
	extra = 1

class	PermitInLine(admin.TabularInline):
	model = Permit
	extra = 1
'''
# 2. Odmins
class	ProjectAdmin(admin.ModelAdmin):
	list_display	= ('title',)
	ordering	= ('title',)
	search_fields	= ('title',)
	#inlines		= (OkopfInLine,)

class	StatusAdmin(admin.ModelAdmin):
	list_display	= ('id', 'title',)
	ordering	= ('title',)
	search_fields	= ('title',)

class	TaskAdmin(admin.ModelAdmin):
	list_display	= ('project', 'title', 'status',)
	ordering	= ('project', 'title',)
	search_fields	= ('title',)

admin.site.register(Project,		ProjectAdmin)
admin.site.register(Status,		StatusAdmin)
admin.site.register(Task,		TaskAdmin)
#admin.site.register(Comment,		CommentAdmin)
#admin.site.register(CommonAttach,	CommonAttachAdmin)
#admin.site.register(ProjectAttach,	ProjectAttachAdmin)
#admin.site.register(TaskAttach,		TaskAttachAdmin)
