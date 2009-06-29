# -*- coding: utf-8 -*-

from django import forms

from models import *

class	ImportForm(forms.Form):
	file  = forms.FileField()

class	OrgMainForm(forms.ModelForm):
	#regdate = forms.DateField(widget=widgets.SelectDateWidget())

	class	Meta:
		model = Org
		fields = ('id', 'name', 'fullname', 'regdate', 'inn', 'kpp', 'ogrn', 'laddress', 'raddress', 'sroregdate', 'licno', 'licdue', 'okopf')
