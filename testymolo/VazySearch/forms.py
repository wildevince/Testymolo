from django import forms

from VazySearch.models import *


class SearchQuery_ModelForm(forms.ModelForm):
    
    class Meta:
        model = SearchQuery
        fields = ("query",)





