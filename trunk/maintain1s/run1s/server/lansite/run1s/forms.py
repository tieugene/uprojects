from django import forms
from models import Db

TOPIC_CHOICES = (
	('general', 'General enquiry'),
	('bug', 'Bug report'),
	('suggestion', 'Suggestion'),
)

class	DbAclForm(forms.Form):
	org = forms.CharField()
	type = forms.CharField()
	share = forms.CharField()
	path = forms.CharField()

class	UserAclForm(forms.Form):
	org = forms.ChoiceField(choices=TOPIC_CHOICES)
	type = forms.CharField()
	share = forms.CharField()
	path = forms.CharField()
	comments = forms.CharField()
