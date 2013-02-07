# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *

# 1. inlines
class   MedHistoryLine(admin.TabularInline):
    model   = MedHistory
    extra   = 1

class   VisitLine(admin.TabularInline):
    model   = Visit
    extra   = 1

class   MedRecordLine(admin.TabularInline):
    model   = MedRecord
    extra   = 1

class   MedRecordEntryLine(admin.TabularInline):
    model   = MedRecordEntry
    extra   = 1

# 2. ordinar
class	PatientAdmin(admin.ModelAdmin):
    inlines = (MedHistoryLine,)

class	MedHistoryAdmin(admin.ModelAdmin):
    inlines = (VisitLine,)

class	VisitAdmin(admin.ModelAdmin):
    inlines = (MedRecordLine,)

class	MedRecordAdmin(admin.ModelAdmin):
    inlines = (MedRecordEntryLine,)

admin.site.register(Patient,    PatientAdmin)
admin.site.register(MedHistory, MedHistoryAdmin)
admin.site.register(Visit,      VisitAdmin)
admin.site.register(MedRecord,  MedRecordAdmin)
