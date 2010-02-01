# -*- coding: utf-8 -*-

from django import forms

from models import *

class	ImportForm(forms.Form):
	file  = forms.FileField()

class	OrgListForm(forms.Form):
	okato		= forms.ModelChoiceField(queryset=Okato.objects.all(), required=False)
	insurer		= forms.ModelChoiceField(queryset=Insurer.objects.all(), required=False)
	#okato.widget.attrs["onchange"]="window.location.href='../org_o/1/'"
	okato.widget.attrs["onchange"]="this.form.submit()"
	insurer.widget.attrs["onchange"]="this.form.submit()"

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
		#fields = ('firstname', 'midname', 'lastname')

class	PermitListForm(forms.Form):
	permittype	= forms.ModelChoiceField(queryset=PermitType.objects.all(), required=False)
	otherperm	= forms.ModelChoiceField(queryset=Permit.objects.all(), required=False)

class	PermitForm(forms.ModelForm):
	class	Meta:
		model = Permit
		fields = ('permittype',)

class	PermitOwnForm(forms.ModelForm):
	date	= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'))
	#def	__init__(self, *args, **kwargs):
	#	super(PermitOwnForm, self).__init__(*args, **kwargs)
	#	instance = getattr(self, 'instance', None)
	#	if instance and instance.id:
	#		self.fields['permit'].required = False
	#		self.fields['permit'].widget.attrs['disabled'] = 'disabled'
	#def	clean_permit(self):
	#	# As shown in the above answer.
	#	instance = getattr(self, 'instance', None)
	#	if instance:
	#		return instance.permit
	#	else:
	#		return self.cleaned_data.get('permit', None)
	class	Meta:
		model = PermitOwn
		fields = ('regno', 'date', 'meeting')
		#exclude = ('permit',)
		#readonly = ('permit',)

class	PermitStatementForm(forms.ModelForm):
	date	= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'))
	class	Meta:
		model = PermitStatement
		fields = ('date',)

class	PermitAlienForm(forms.ModelForm):
	date		= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), required=False)
	protodate	= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), required=False)
	class	Meta:
		model = PermitAlien
		fields = ('regno', 'date', 'sro', 'protono', 'protodate')

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
