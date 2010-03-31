# -*- coding: utf-8 -*-
from django import forms

from models import *

class	ToDoCatForm(forms.ModelForm):
	class	Meta:
		model = ToDoCat

class	ToDoForm(forms.ModelForm):
	class	Meta:
		model = ToDo
		#exclude = ('ancestor', 'master', 'author', 'created')
		fields = ('deadline', 'subject', 'description', 'done', 'category')
