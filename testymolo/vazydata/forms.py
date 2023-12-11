from django import forms

import datamolo.models as data


class OrganismForm(forms.Form):
    id = forms.IntegerField()
    name = forms.CharField()
    abr = forms.CharField(max_length=25)
    phylogeny = forms.CharField(max_length=200)
    
    id_hide = forms.IntegerField(label='hide', widget=forms.HiddenInput)
    name_hide = forms.CharField(label='hide', max_length=100, widget=forms.HiddenInput)
    abr_hide = forms.CharField(label='hide', max_length=25, widget=forms.HiddenInput)
    phylogeny_hide = forms.CharField(label='hide', max_length=200, widget=forms.HiddenInput)

    
class ProteinFrom(forms.Form):
    id = forms.IntegerField(label='id', required=False)
    subseqs = forms.IntegerField(label="Nbr. of subseqs attached", required=False)
    fasta = forms.CharField(widget=forms.Textarea, required=False)
    isPP = forms.BooleanField(required=False)
    derivedFromPP = forms.BooleanField(required=False)
    organism = forms.ModelChoiceField(queryset=data.Organism.objects.all(), required=False)
    genbank = forms.CharField(max_length=20, required=False)
    name = forms.CharField(max_length=100, required=False)
    definition = forms.CharField(max_length=20, required=False)
    data_ac = forms.IntegerField(required=False)
    complete = forms.BooleanField(required=False)

    fasta_hide = forms.CharField(label='hide', required=False, widget=forms.HiddenInput)
    genbank_hide = forms.CharField(label='hide', max_length=20, required=False, widget=forms.HiddenInput)
    name_hide = forms.CharField(label='hide', max_length=100, required=False, widget=forms.HiddenInput)
    definition_hide = forms.CharField(label='hide', max_length=100, required=False, widget=forms.HiddenInput)

"""
class ProteinFrom(forms.ModelForm):
    id = forms.IntegerField(label='id')
    subseqs = forms.IntegerField(label="Nbr. of subseqs attached")
    fasta = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = data.Protein
        fields = ("id", "isPP", "derivedFromPP", "organism", "genbank", "name", "data_ac", "complete")
"""
