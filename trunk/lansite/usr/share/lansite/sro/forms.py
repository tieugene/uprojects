# -*- coding: utf-8 -*-

from django import forms

from models import *

class	ImportForm(forms.Form):
	file  = forms.FileField()

class	OrgMainForm(forms.ModelForm):
	class	Meta:
		model = Org
		fields = ('name', 'fullname', 'regdate', 'inn', 'kpp', 'ogrn', 'laddress', 'raddress', 'sroregdate', 'licno', 'licdue', 'okopf')

class	OrgPhoneForm(forms.ModelForm):
	class	Meta:
		model = OrgPhone
		fields = ('country', 'trunk', 'phone', 'ext',)

class	OrgEmailForm(forms.Form):
	email	= forms.EmailField()

class	OrgStuffForm(forms.ModelForm):
	class	Meta:
		model = OrgStuff
		fields = ('person', 'role', 'leader')

class	PermitForm(forms.ModelForm):
	class	Meta:
		model = Permit
		fields = ('id', 'date',)
