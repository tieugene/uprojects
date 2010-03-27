# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

#class	TaskAdmin(admin.ModelAdmin):
#	pass

admin.site.register(Object,		admin.ModelAdmin)
admin.site.register(AddrShort,		admin.ModelAdmin)
admin.site.register(Address,		admin.ModelAdmin)
admin.site.register(Contact,		admin.ModelAdmin)
admin.site.register(AddrType,		admin.ModelAdmin)
admin.site.register(Person,		admin.ModelAdmin)
admin.site.register(Org,		admin.ModelAdmin)
admin.site.register(Org_RU,		admin.ModelAdmin)
admin.site.register(Task,		admin.ModelAdmin)
