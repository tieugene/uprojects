# -*- coding: utf-8 -*-

from django import forms

from models import *

class	ImportForm(forms.Form):
	file  = forms.FileField()

class	OrgMainForm(forms.ModelForm):
	fullname	= forms.CharField(label='Полное наименование', widget=forms.Textarea)
	egruldate	= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата регистрации в ЕГРЮЛ', required=False)
	laddress	= forms.CharField(label='Юридический адрес', widget=forms.Textarea)
	raddress	= forms.CharField(label='Фактический адрес', widget=forms.Textarea, required=False)
	sroregdate	= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата членства в НП', required=False)
	paydate		= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата оплаты взноса в КФ', required=False)
	paydatevv	= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата оплаты вступительного взноса', required=False)
	class	Meta:
		model = Org
		exclude = ('okveds', 'events', 'stuffs', 'files')

class	OrgLicenseForm(forms.ModelForm):
	no		= forms.CharField(label='Номер', widget=forms.Textarea)
	datefrom	= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Действует с')
	datedue		= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Действительна до')
	class	Meta:
		model = OrgLicense
		fields = ('no', 'datefrom', 'datedue',)

class	OrgInsuranceForm(forms.ModelForm):
	insdate		= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата договора')
	datefrom	= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Старховка с', required=False)
	datetill	= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Страховка по', required=False)
	class	Meta:
		model = OrgInsurance
		fields = ('insurer', 'insno', 'insdate', 'insum', 'datefrom', 'datetill',)

class	OrgPhoneForm(forms.ModelForm):
	class	Meta:
		model = OrgPhone
		fields = ('phone',)

class	OrgEmailForm(forms.Form):
	email	= forms.EmailField()

class	OrgWWWForm(forms.Form):
	www	= forms.URLField()

class	OrgStuffForm(forms.ModelForm):
	class	Meta:
		model = OrgStuff
		fields = ('person', 'role', 'leader', 'permanent')

class	OrgStuffAddPersonForm(forms.ModelForm):
	class	Meta:
		model = Person
		fields = ('firstname', 'midname', 'lastname')

class	OrgStuffAddRoleForm(forms.ModelForm):
	class	Meta:
		model = Role
		#fields = ('firstname', 'midname', 'lastname')

class	PermitForm(forms.ModelForm):
	date	= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'))
	class	Meta:
		model = Permit
		fields = ('regno', 'date', 'meeting')

class	PersonMainForm(forms.ModelForm):
	class	Meta:
		model = Person
		fields = ('lastname', 'firstname', 'midname',)

class	PersonSkillForm(forms.ModelForm):
	class	Meta:
		model = PersonSkill
		fields = ('speciality', 'skill', 'year', 'school')

class	PersonSkillAddSpecialityForm(forms.ModelForm):
	class	Meta:
		model = Speciality

class	PersonSkillAddSkillForm(forms.ModelForm):
	class	Meta:
		model = Skill
