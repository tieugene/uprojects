# -*- coding: utf-8 -*-
from django import forms

class	ImportForm(forms.Form):
	file  = forms.FileField()
