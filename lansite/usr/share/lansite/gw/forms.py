# -*- coding: utf-8 -*-
from django import forms

from models import *

class	ToDoCatForm(forms.ModelForm):
	class	Meta:
		model = ToDoCat
		fields = ('name',)

class	ToDoForm(forms.ModelForm):
	class	Meta:
		model = ToDo
		#exclude = ('ancestor', 'master', 'author', 'created')
		fields = ('deadline', 'subject', 'description', 'done', 'category')

class	ToDoOfCatForm(forms.ModelForm):
	class	Meta:
		model = ToDo
		fields = ('deadline', 'subject', 'description', 'done',)

class	AssignCatForm(forms.ModelForm):
	class	Meta:
		model = AssignCat

class	AssignForm(forms.ModelForm):
	class	Meta:
		model = Assign
		fields = ('deadline', 'subject', 'description', 'category', 'importance', 'assignee')

class	UserListForm(forms.Form):
	user	= forms.ModelChoiceField(queryset=GwUser.objects.all(), required=True)

class	LineCommentForm(forms.Form):
	comment	= forms.CharField(label='Причина')

class	AssignDupForm(forms.Form):
	assign	= forms.ModelChoiceField(queryset=Assign.objects.all(), required=True)
