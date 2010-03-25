# -*- coding: utf-8 -*-

from django import forms

from models import *

class	OrgListForm(forms.Form):
	okato		= forms.ModelChoiceField(queryset=Okato.objects.all(), required=False)
	insurer		= forms.ModelChoiceField(queryset=Insurer.objects.all(), required=False)
	okato.widget.attrs["onchange"]="this.form.submit()"
	insurer.widget.attrs["onchange"]="this.form.submit()"

class	OrgAddForm(forms.ModelForm):
	fullname	= forms.CharField(label='Полное наименование', widget=forms.Textarea)
	egruldate	= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата регистрации в ЕГРЮЛ', required=False)
	laddress	= forms.CharField(label='Юридический адрес', widget=forms.Textarea)
	raddress	= forms.CharField(label='Фактический адрес', widget=forms.Textarea, required=False)
	class	Meta:
		model = Org
		exclude = ('okveds', 'stuffs', 'sro', 'user')

class	OrgEditForm(forms.ModelForm):
	fullname	= forms.CharField(label='Полное наименование', widget=forms.Textarea)
	egruldate	= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата регистрации в ЕГРЮЛ', required=False)
	laddress	= forms.CharField(label='Юридический адрес', widget=forms.Textarea)
	raddress	= forms.CharField(label='Фактический адрес', widget=forms.Textarea, required=False)
	class	Meta:
		model = Org
		exclude = ('okveds', 'stuffs', 'sro', 'user')

class	OrgSroForm(forms.ModelForm):
	regdate		= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата членства в НП', required=False)
	paydate		= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата оплаты взноса в КФ', required=False)
	paydatevv	= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата оплаты вступительного взноса', required=False)
	class	Meta:
		model = OrgSro
		exclude = ('org', 'sro', 'events',)

class	OrgLicenseForm(forms.ModelForm):
	no		= forms.CharField(label='Номер', widget=forms.Textarea)
	datefrom	= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Действует с')
	datedue		= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Действительна до')
	class	Meta:
		model = OrgLicense
		fields = ('no', 'datefrom', 'datedue',)

class	OrgInsuranceForm(forms.ModelForm):
	date		= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата договора')
	datefrom	= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Старховка с', required=False)
	datedue		= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Страховка по', required=False)
	class	Meta:
		model = OrgInsurance
		fields = ('insurer', 'no', 'date', 'sum', 'datefrom', 'datedue',)

class	OrgPhoneForm(forms.ModelForm):
	class	Meta:
		model = OrgPhone
		fields = ('phone',)

class	OrgEmailForm(forms.ModelForm):
	class	Meta:
		model = OrgEmail
		fields = ('URL',)

class	OrgWWWForm(forms.ModelForm):
	class	Meta:
		model = OrgWWW
		fields = ('URL',)

class	OrgStuffForm(forms.ModelForm):
	class	Meta:
		model = OrgStuff
		fields = ('person', 'role', 'leader', 'permanent')

class	OrgStuffForm_Soft(forms.ModelForm):
	person	= forms.ModelChoiceField(queryset=Person.objects.all(), required=False)
	role	= forms.ModelChoiceField(queryset=Role.objects.all(), required=False)
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

class	StageListForm(forms.ModelForm):
	class	Meta:
		model = StageList
		fields = ('type',)

class	StatementForm(forms.ModelForm):
	date	= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата')
	class	Meta:
		model = Statement
		fields = ('date',)

class	StageListListForm(forms.Form):
	type	= forms.ModelChoiceField(queryset=StageListType.objects.all(), required=False)
	#other	= forms.ModelChoiceField(queryset=StageList.objects.all(), required=False) - too slow
	other	= forms.CharField(required=False)

class	PermitForm(forms.ModelForm):
	date	= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата')
	class	Meta:
		model = Permit
		fields = ('no', 'date', 'protocol')

class	PersonMainForm(forms.ModelForm):
	class	Meta:
		model = Person
		fields = ('lastname', 'firstname', 'midname',)

class	PersonSkillForm(forms.ModelForm):
	skilldate	= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label=u'Дата окончания', required=False)
	seniodate	= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label=u'Дата актуальности стажа', required=False)
	tested		= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label=u'Аттестат. Дата выдачи', required=False)
	coursedate	= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label=u'СоПК. Дата выдачи', required=False)
	class	Meta:
		model = PersonSkill
		fields = ('speciality', 'skill', 'year', 'skilldate', 'school', 'seniority', 'seniodate', 'tested', 'courseno', 'coursedate', 'coursename', 'courseschool')

class	PersonSkillAddSpecialityForm(forms.ModelForm):
	class	Meta:
		model = Speciality
		fields = ('name',)

class	PersonSkillAddSkillForm(forms.ModelForm):
	class	Meta:
		model = Skill
