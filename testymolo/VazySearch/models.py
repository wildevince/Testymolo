import json
import os

from django.conf import settings
from django.db import models



# Create your models here.
class SearchQuery(models.Model):
        
    options_choices = (
        ('keywords', 'keywords'),
        ('DB_ac', 'DB_ac'),
        ('protein_id', 'protein_id'),
        ('Modulo', 'Modulo'),
    )

    query = models.CharField(max_length=200, verbose_name="keywords")
    option = models.CharField(max_length=25, choices=options_choices, default='DB_ac')

    @staticmethod
    def get_query(query:str):
        #query:str = str(self.query)
        non_words = ['the', 'of', 'for', 'not', 'and', 'or', 'a', 'an']
        Q:list = [w.strip() for w in query.split()]
        QQ:list = [w for w in Q if w not in non_words]
        return QQ
    

class Lexicon(): 

    content:dict = json.loads(open(os.path.join(settings.DATA_DIR, "Lexicon.json")).read())

    @staticmethod
    def get_synonym(q):
        for syn, values in Lexicon.content.items():
            if q in values:
                return syn
        return q
    