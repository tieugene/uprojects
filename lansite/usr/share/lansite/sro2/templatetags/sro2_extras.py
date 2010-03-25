# -*- coding: utf-8 -*-


from sro2.models import checkuser
from django import template

register = template.Library()

@register.filter
def	chkuser(obj, user):
	return checkuser(obj, user)
