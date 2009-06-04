# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Var, Org, Dbtype, Host, Share, Db, User

class	VarAdmin(admin.ModelAdmin):
	list_display = ['name', 'value']

class	OrgAdmin(admin.ModelAdmin):
	list_display = ['name', 'comments']

class	DbtypeAdmin(admin.ModelAdmin):
	list_display = ['name', 'comments']

class	HostAdmin(admin.ModelAdmin):
	list_display = ['name', 'comments']
	fields = ['name', 'comments']

class	ShareAdmin(admin.ModelAdmin):
	list_display = ['host', 'name', 'comments']

class	DbAdmin(admin.ModelAdmin):
	list_display = ['org', 'type', 'share', 'path', 'comments']

class	UserAdmin(admin.ModelAdmin):
	list_display = ['login', 'password', 'comments']

admin.site.register(Var,	VarAdmin)
admin.site.register(Org,	OrgAdmin)
admin.site.register(Dbtype,	DbtypeAdmin)
admin.site.register(Host,	HostAdmin)
admin.site.register(Share,	ShareAdmin)
admin.site.register(Db,		DbAdmin)
admin.site.register(User,	UserAdmin)
