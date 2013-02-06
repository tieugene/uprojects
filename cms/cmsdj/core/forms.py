# -*- coding: utf-8 -*-
from django import forms
from models import *

class   PersonAddressForm(forms.ModelForm):
    class       Meta:
        model = PersonAddress
