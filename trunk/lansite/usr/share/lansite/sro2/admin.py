# -*- coding: utf-8 -*-
'''
TODO:
	* Inlines:	extra, raw_id_fields
	* Ordinar:	raw_id_fields, fields, fieldset
	* Selector: raw_id + readonly - or unicode + del/add + select
w/o admin:
	Job, SpecialityStage, PersonSkill, OrgOkved, OrgPhone, OrgEmail, OrgWWW, OrgStuff, OrgEvent, OrgLicense, OrgInsurance, Protocol, PermitStageJob
'''

from django import forms
from django.contrib import admin
from models import *

# 1. Inlines
class	BranchUserInLine(admin.TabularInline):
	model		= BranchUser
	extra		= 1

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

# 2. Odmins
class	BranchAdmin(admin.ModelAdmin):
	list_display	= ('id', 'name', 'center')
	ordering	= ('id',)
	search_fields	= ('name',)
	inlines		= (BranchUserInLine,)

class	BranchUserAdmin(admin.ModelAdmin):
	list_display	= ('branch', 'user',)
	ordering	= ('branch', 'user',)

class	InsurerAdmin(admin.ModelAdmin):
	list_display	= ('id', 'name', 'fullname')
	ordering	= ('name',)
	search_fields	= ('name',)

class	OkatoAdmin(admin.ModelAdmin):
	list_display	= ('id', 'name')
	ordering	= ('id',)
	search_fields	= ('name',)

class	OkopfAdmin(admin.ModelAdmin):
	list_display	= ('id', 'name', 'shortname', 'namedp', 'disabled', 'parent')
	ordering	= ('id',)
	search_fields	= ('shorname',)
	inlines		= (OkopfInLine,)

class	OkvedAdmin(admin.ModelAdmin):
	list_display	= ('id', 'name', 'parent')
	ordering	= ('id',)
	search_fields	= ('name',)
	inlines		= (OkvedInLine,)

class	SroTypeAdmin(admin.ModelAdmin):
	list_display	= ('id', 'name')
	ordering	= ('id',)
	search_fields	= ('name',)

class	SroAdmin(admin.ModelAdmin):
	list_display	= ('name', 'fullname', 'type', 'own',)
	ordering	= ('name',)
	search_fields	= ('name',)
	inlines		= (ProtocolInLine,)

class	SroOwnAdmin(admin.ModelAdmin):
	list_display	= ('sro', 'boss',)
	ordering	= ('sro',)
	search_fields	= ('sro',)

class	StageAdmin(admin.ModelAdmin):
	list_display	= ('id', 'srotype', 'no', 'name', 'hq', 'hs', 'mq', 'ms')
	ordering	= ('srotype', 'no', 'name')
	inlines		= (JobInLine, SpecialityStageInLine)

class	SpecialityAdmin(admin.ModelAdmin):
	list_display	= ('name',)
	ordering	= ('name',)
	search_fields	= ('name',)
	inlines		= (PersonSkillInLine, SpecialityStageInLine)

class	SkillAdmin(admin.ModelAdmin):
	list_display	= ('high', 'name',)
	ordering	= ('high', 'name',)
	search_field	= ('name',)
	inlines		= (PersonSkillInLine,)

class	EventTypeAdmin(admin.ModelAdmin):
	list_display	= ('name', 'comments')
	ordering	= ('name',)

class	RoleAdmin(admin.ModelAdmin):
	list_display	= ('name', 'comments')
	ordering	= ('name',)

class	PersonAdmin(admin.ModelAdmin):
	list_display	= ('lastname', 'firstname', 'midname',)
	ordering	= ('lastname', 'firstname', 'midname',)
	inlines		= (PersonSkillInLine, OrgStuffInLine,)
	#inlines		= (PersonSkillInLine,)

class	OrgAdmin(admin.ModelAdmin):
	list_display	= ('name', 'fullname')
	ordering	= ('name',)
	inlines		= (OrgOkvedInLine, OrgPhoneInLine, OrgEmailInLine, OrgWWWInLine, OrgStuffInLine, OrgSroInLine)
	raw_id_fields	= ('okveds',)
	#readonly_fields

class	AgentAdmin(admin.ModelAdmin):
	list_display	= ('name',)
	ordering	= ('name',)

class	OrgSroAdmin(admin.ModelAdmin):
	list_display	= ('org', 'sro', 'agent',)
	ordering	= ('org', 'sro')
	list_filter	= ('sro', 'agent',)
	search_fields	= ('sro', 'agent')
	inlines		= (OrgEventInLine, OrgLicenseInLine, OrgInsuranceInLine, StageListInLine)

class	StageListTypeAdmin(admin.ModelAdmin):
	list_display	= ('id', 'name',)
	ordering	= ('id', 'name',)

class	StageListAdmin(admin.ModelAdmin):
	list_display	= ('orgsro', 'type',)
	ordering	= ('orgsro', 'type',)
	inlines		= (PermitStageInLine, StatementInLine, PermitInLine,)
	#inlines		= (PermitStageInLine,)

class	PermitStageAdmin(admin.ModelAdmin):
	list_display	= ('stagelist', 'stage',)
	ordering	= ('stagelist', 'stage',)
	inlines		= (PermitStageJobInLine,)

class	StatementAdmin(admin.ModelAdmin):
	list_display	= ('stagelist', 'date',)
	ordering	= ('stagelist', 'date',)

class	PermitAdmin(admin.ModelAdmin):
	list_display	= ('stagelist', 'no', 'date',)
	ordering	= ('stagelist', 'no', 'date',)

admin.site.register(Branch,		BranchAdmin)
admin.site.register(BranchUser,		BranchUserAdmin)
admin.site.register(Insurer,		InsurerAdmin)
admin.site.register(Okato,		OkatoAdmin)
admin.site.register(Okopf,		OkopfAdmin)
admin.site.register(Okved,		OkvedAdmin)
admin.site.register(SroType,		SroTypeAdmin)
admin.site.register(Sro,		SroAdmin)
admin.site.register(SroOwn,		SroOwnAdmin)
admin.site.register(Stage,		StageAdmin)
admin.site.register(Speciality,		SpecialityAdmin)
admin.site.register(Skill,		SkillAdmin)
admin.site.register(EventType,		EventTypeAdmin)
admin.site.register(Role,		RoleAdmin)
admin.site.register(Person,		PersonAdmin)
admin.site.register(Org,		OrgAdmin)
admin.site.register(Agent,		AgentAdmin)
admin.site.register(OrgSro,		OrgSroAdmin)
admin.site.register(StageListType,	StageListTypeAdmin)
admin.site.register(StageList,		StageListAdmin)
admin.site.register(PermitStage,	PermitStageAdmin)
admin.site.register(Statement,		StatementAdmin)
admin.site.register(Permit,		PermitAdmin)
