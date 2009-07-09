# -*- coding: utf-8 -*-

from django import forms

from models import *

class	ImportForm(forms.Form):
	file  = forms.FileField()

class	OrgMainForm(forms.ModelForm):
	class	Meta:
		model = Org
		#fields = ('regno', 'name', 'fullname', 'regdate', 'inn', 'kpp', 'ogrn', 'laddress', 'raddress', 'sroregdate', 'licno', 'licdue', 'okopf')
		exclude = ('okveds', 'events', 'stuffs', 'files')

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

class	OrgStuffAddPersonForm(forms.ModelForm):
	class	Meta:
		model = Person
		fields = ('firstname', 'midname', 'lastname')

class	OrgStuffAddRoleForm(forms.ModelForm):
	class	Meta:
		model = Role
		#fields = ('firstname', 'midname', 'lastname')

class	PermitForm(forms.ModelForm):
	class	Meta:
		model = Permit
		fields = ('regno', 'date',)
