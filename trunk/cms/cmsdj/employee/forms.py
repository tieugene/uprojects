# -*- coding: utf-8 -*-
from django import forms
import decimal

class   StaffForm(forms.Form):
    qty = forms.DecimalField(min_value=decimal.Decimal('0.01'), max_digits=5, decimal_places=2)
