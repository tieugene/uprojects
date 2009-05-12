# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

# 1. inlines
class	OkopfInLine(admin.TabularInline):
	model = Okopf
	extra = 0
#	inlines		= [OkopfInLine,]

class	SkillInLine(admin.TabularInline):
	model = Skill
	extra = 1

class	StageOkdpInLine(admin.TabularInline):
	model = StageOkdp
	extra = 1

class	StageOksoInLine(admin.TabularInline):
	model = StageOkso
	extra = 1

class	PersonSkillInLine(admin.TabularInline):
	model = PersonSkill
	extra = 1

class	PersonFileInLine(admin.TabularInline):
	model = PersonFile
	extra = 1

class	OrgOkvedInLine(admin.TabularInline):
	model = OrgOkved
	extra = 1

class	OrgLOkdpInLine(admin.TabularInline):
	model = OrgLOkdp
	extra = 1

class	OrgSOkdpInLine(admin.TabularInline):
	model = OrgSOkdp
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
	
class	OrgStuffInLine(admin.TabularInline):
	model = OrgStuff
	extra = 1

class	OrgFileInLine(admin.TabularInline):
	model = OrgFile
	extra = 1

class	MeetingOrgInLine(admin.TabularInline):
	model = MeetingOrg
	extra = 1
	
# 2. Odmins

class	OkopfAdmin(admin.ModelAdmin):
	list_display	= ('id', 'name', 'shortname', 'disabled')
	ordering	= ('id',)
	search_fields	= ('shorname',)
	inlines		= [OkopfInLine,]

class	OkvedAdmin(admin.ModelAdmin):
	list_display	= ['id', 'name', 'disabled']

class	OksoAdmin(admin.ModelAdmin):
	list_display	= ('id', 'name', 'disabled')
	ordering	= ('id',)
	search_fields	= ('name',)
	inlines		= [SkillInLine,]

class	OkdpAdmin(admin.ModelAdmin):
	list_display = ['id', 'name']

class	StageAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'hq', 'hs', 'mq', 'ms']
	inlines = [StageOksoInLine,]

class	StageOkdpAdmin(admin.ModelAdmin):
	list_display = ['stage', 'okdp']

class	StageOksoAdmin(admin.ModelAdmin):
	list_display = ['stage', 'okso']

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
	inlines = (PersonSkillInLine, OrgStuffInLine, PersonFileInLine,)

class	PersonSkillAdmin(admin.ModelAdmin):
	list_display = ['person', 'skill']

class	PersonFileAdmin(admin.ModelAdmin):
	list_display = ['person', 'file']

class	OrgAdmin(admin.ModelAdmin):
	list_display = ['name', 'fullname']
	inlines = (OrgOkvedInLine, OrgPhoneInLine, OrgEmailInLine, OrgStuffInLine, OrgFileInLine)

class	OrgEventAdmin(admin.ModelAdmin):
	list_display = ['org', 'type']

class	OrgStuffAdmin(admin.ModelAdmin):
	list_display = ['org', 'role']

class	OrgFileAdmin(admin.ModelAdmin):
	list_display = ['org', 'file']

class	MeetingAdmin(admin.ModelAdmin):
	list_display = ['date', 'agenda']
	inlines = (MeetingOrgInLine,)

admin.site.register(Okopf,	OkopfAdmin)
admin.site.register(Okved,	OkvedAdmin)
admin.site.register(Okso,	OksoAdmin)
admin.site.register(Okdp,	OkdpAdmin)
admin.site.register(Stage,	StageAdmin)
admin.site.register(StageOkdp,	StageOkdpAdmin)
admin.site.register(StageOkso,	StageOksoAdmin)
admin.site.register(Phone,	PhoneAdmin)
admin.site.register(Email,	EmailAdmin)
admin.site.register(EventType,	EventTypeAdmin)
admin.site.register(Role,	RoleAdmin)
admin.site.register(Person,	PersonAdmin)
admin.site.register(PersonSkill,	PersonSkillAdmin)
admin.site.register(PersonFile,	PersonFileAdmin)
admin.site.register(Org,	OrgAdmin)
admin.site.register(OrgEvent,	OrgEventAdmin)
admin.site.register(OrgStuff,	OrgStuffAdmin)
admin.site.register(OrgFile,	OrgFileAdmin)
admin.site.register(Meeting,	MeetingAdmin)
