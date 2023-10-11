from django.db import models
from django import forms

import datamolo.models as data


class ProteinForm(forms.ModelForm):
    class Meta:
        model = data.Protein
        fields = '__all__'


class VazyRecord(forms.Form):
    pass