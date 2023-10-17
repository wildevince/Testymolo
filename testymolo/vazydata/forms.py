from django.db import models
from django import forms

import datamolo.models as data


class OrganismForm(forms.ModelForm):
    class Meta:
        model = data.Organism
        fields = ("id", "name", "abr", "phylogeny",)

class ProteinFrom(forms.ModelForm):
    class Meta:
        model = data.Protein
        fields = ("isPP", "derivedFromPP", "organism", "genbank", "name", "data_ac", "header", "sequence", "complete")
