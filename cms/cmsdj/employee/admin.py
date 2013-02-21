# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *

# 1. inlines
class   RoomLine(admin.TabularInline):
    model   = Room
    extra   = 1

class   SpecialtyLine(admin.TabularInline):
    model   = Specialty
    extra   = 1

class   StaffListEntryLine(admin.TabularInline):
    model   = StaffListEntry
    extra   = 1

class   RoomScheduleEntryLine(admin.TabularInline):
    model   = RoomScheduleEntry
    extra   = 1

# 2. ordinar
class	DepartmentAdmin(admin.ModelAdmin):
    inlines = (RoomLine, SpecialtyLine,)

class	StaffListAdmin(admin.ModelAdmin):
    inlines = (StaffListEntryLine,)

class	RoomScheduleAdmin(admin.ModelAdmin):
    inlines = (RoomScheduleEntryLine,)

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Room)
admin.site.register(Specialty)
admin.site.register(Employee)
admin.site.register(StaffList, StaffListAdmin)
admin.site.register(RoomSchedule, RoomScheduleAdmin)
