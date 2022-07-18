from django.contrib import admin

from . import models


# 1. inlines
class QuestInLine(admin.TabularInline):
    model = models.Quest
    extra = 1


@admin.register(models.Poll)
class ContractAdmin(admin.ModelAdmin):
    ordering = ('date0', 'title')
    list_display = ('title', 'date0', 'date1', 'comments',)
    inlines = (QuestInLine,)
