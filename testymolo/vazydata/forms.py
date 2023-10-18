from django.db import models
from django import forms

import datamolo.models as data


class OrganismForm(forms.ModelForm):

    id_hide = forms.IntegerField(label='hide', widget=forms.HiddenInput)
    name_hide = forms.CharField(label='hide', max_length=100, widget=forms.HiddenInput)
    abr_hide = forms.CharField(label='hide', max_length=25, widget=forms.HiddenInput)
    phylogeny_hide = forms.CharField(label='hide', max_length=200, widget=forms.HiddenInput)

    class Meta:
        model = data.Organism
        fields = ("id", "name", "abr", "phylogeny",)

class ProteinFrom(forms.ModelForm):
    id = forms.IntegerField(label='id')
    subseqs = forms.IntegerField(label="Nbr. of subseqs attached")
    fasta = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = data.Protein
        fields = ("id", "isPP", "derivedFromPP", "organism", "genbank", "name", "data_ac", "complete")
        
