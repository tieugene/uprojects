from django.contrib import admin
from admirarchy.toolbox import HierarchicalModelAdmin   # optional
from . import models


class DepartInlineAdmin(admin.TabularInline):
    model = models.Depart
    extra = 1


class PersonInlineAdmin(admin.TabularInline):
    model = models.Person
    extra = 1


class MembersInlineAdmin(admin.TabularInline):
    model = models.Membership
    extra = 1


class PhoneInlineAdmin(admin.TabularInline):
    model = models.Phone
    extra = 1


class EmailInlineAdmin(admin.TabularInline):
    model = models.EMail
    extra = 1


class SnVKInlineAdmin(admin.TabularInline):
    model = models.SnVK
    extra = 1


class SnFBInlineAdmin(admin.TabularInline):
    model = models.SnFB
    extra = 1


@admin.register(models.Org)
class OrgAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    inlines = (DepartInlineAdmin,)


@admin.register(models.Depart)
# ordinar admin
# class DepartAdmin(admin.ModelAdmin):
# admirarchy
class DepartAdmin(HierarchicalModelAdmin):
    hierarchy = True
    # /admirarchy
    list_display = ('pk', 'name', 'qty')
    inlines = (DepartInlineAdmin,)  # MembersInlineAdmin
    # list_select_related = ('persons',)

    @staticmethod
    def qty(obj) -> str:
        return obj.person_qty()


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'last_name', 'first_name', 'mid_name')
    readonly_fields = ('date_joined', 'last_login', 'updated_at', 'statemod_at')
    # 'username' cannot be disabled due uniq
    exclude = ('password', 'is_superuser', 'is_staff', 'groups', 'user_permissions')
    inlines = (PhoneInlineAdmin, EmailInlineAdmin, SnVKInlineAdmin, SnFBInlineAdmin, MembersInlineAdmin)
