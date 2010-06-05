# -*- coding: utf-8 -*-


from sro2.models import checkuser
from django import template

register = template.Library()

@register.filter
def	chkuser(obj, user):
	return checkuser(obj, user)

@register.filter_function
def	order_by(queryset, args):
	args = [x.strip() for x in args.split(',')]
	return queryset.order_by(*args)
