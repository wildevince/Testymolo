import os

from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.http import HttpResponse
# Create your views here.

from VazySearch import forms
from VazySearch import models

import datamolo.views as datamolo
import datamolo.models as data

class SearchEngine(TemplateView):
    
    searchForm_template = os.path.join('vazysearch', 'searchForm.html')
    searchResult_template = os.path.join('vazysearch', 'searchResult.html')

    def searchForm() -> any:
        searchForm = forms.SearchQuery_ModelForm(initial={'option':'protein_id'})
        return searchForm
    
    def search_keywords(request, keywords:list):
        result_Organism_list:list = []
        result_Protein_list:list = []
        # sequence ?
        # activity ?
        for kw in keywords:
            try:
                kw_int = int(kw)
                result = data.Organism.objects.filter(id=kw_int)
                for item in result:
                    if item not in result_Organism_list:
                        result_Organism_list.append(item)
            except:
                pass
            result = data.Organism.objects.filter(name=kw)
            for item in result:
                if item not in result_Organism_list:
                    result_Organism_list.append(item)
            result = data.Organism.objects.filter(abr=kw)
            for item in result:
                if item not in result_Organism_list:
                    result_Organism_list.append(item)
            result = data.Organism.objects.filter(phylogeny=kw)
            for item in result:
                if item not in result_Organism_list:
                    result_Organism_list.append(item)
            #
            result = data.Protein.objects.filter(name=kw)
            for item in result:
                if item not in result_Protein_list:
                    result_Protein_list.append(item)
            result = data.Protein.objects.filter(definition=kw)
            for item in result:
                if item not in result_Protein_list:
                    result_Protein_list.append(item)
            result = data.Protein.objects.filter(genbank=kw)
            for item in result:
                if item not in result_Protein_list:
                    result_Protein_list.append(item)

        return render(request, SearchEngine.searchResult_template, {'result_Organism_list':result_Organism_list, 'result_Protein_list':result_Protein_list})

    
    def post(request):
        if request.method == "POST":
            searchForm = forms.SearchQuery_ModelForm(request.POST)
            if searchForm.is_valid():
                keywords = models.SearchQuery.get_query(searchForm.cleaned_data['query'])
                option = searchForm.cleaned_data['option']
            
                if option == 'keywords':
                    return SearchEngine.search_keywords(request, keywords)

                elif option == 'DB_ac':
                    DB_ac:str = keywords[0]
                    return datamolo.Main.get_mainProtein_from_searchEngine(request, DB_ac=DB_ac)
                
                elif option == 'protein_id':
                    protein_id:str = int(keywords[0])
                    return datamolo.Main.get_mainProtein_from_searchEngine(request, protein_id=protein_id)
                
                elif option == 'Modulo':
                    mod_id:str = keywords[0]
                    return datamolo.Main.get_Module_from_searchEngine(request, Modulo=mod_id)
        
        return HttpResponse("Frek")
