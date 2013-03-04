# -*- coding: utf-8 -*-
from django import forms
from models import *

class   PersonAddressForm(forms.ModelForm):
    #person = forms.ModelChoiceField(queryset=Person.objects.all(), widget=forms.widgets.Select(attrs={'hidden':'hidden'}))
    #person = forms.ModelChoiceField(queryset=Person.objects.all(), required=False, widget=forms.widgets.Select(attrs={'disabled':'disabled'}))
    #person = forms.ModelChoiceField(queryset=Person.objects.all(), widget=forms.widgets.Select())
    class       Meta:
        model = PersonAddress
        #exclude = ('person',)
    #def __init__(self, *args, **kwargs):
        #super(PersonAddressForm, self).__init__(*args, **kwargs)
        #init = getattr(self, 'init', None)
        #if (self.initial):
        #    self.fields['person'].queryset = Person.objects.filter(pk=self.initial['person'].pk)
        #instance = getattr(self, 'instance', None)
        #print "Form: instanse =", instance, "person =", 
        #print "Form:", self.fields['person'].data()
        #if instance and instance.id:
        #self.fields['person'].widget.attrs['disabled'] = True

    #def clean_person(self):
    #    return self.instance.person

class   PersonPhoneForm(forms.ModelForm):
    class       Meta:
        model = PersonPhone

class   PersonEmailForm(forms.ModelForm):
    class       Meta:
        model = PersonEmail

class   PersonDocumentForm(forms.ModelForm):
    class       Meta:
        model = PersonDocument

class   PersonCodeForm(forms.ModelForm):
    class       Meta:
        model = PersonCode
