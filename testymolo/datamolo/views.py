from django.shortcuts import render
from django.http import HttpResponse


import datamolo.scr.add_item_in_model as scr


# Create your views here.

def index(request):

    ## implement Database
    scr.parse_data()

    return HttpResponse("The World !")
