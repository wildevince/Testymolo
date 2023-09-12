import re, os, json
import Bio
import numpy as np

from django.conf import settings


# 
def parse_Protein(Proteins):
    outfile = os.path.join(settings.DATA_DIR,"Protein.temp.json")

    with open(outfile, 'w') as handle:
        txt:list = list([json.dumps(Protein.serialize()) for Protein in Proteins])
        handle.write('[\n'+ ',\n'.join(txt) + ']')
        

def parse_Modulo(Moduli):
    outfile = os.path.join(settings.DATA_DIR,"Modulo.temp.json")

    with open(outfile, 'w') as handle:
        txt:list = list([json.dumps(Modulo.serialize()) for Modulo in Moduli])
        handle.write('[\n'+ ',\n'.join(txt) + ']')
        

def parse_Organism(Organisms):
    outfile = os.path.join(settings.DATA_DIR,"Organism.temp.json")

    with open(outfile, 'w') as handle:
        txt:list = list([json.dumps(org.serialize()) for org in Organisms])
        handle.write('[\n'+ ',\n'.join(txt) + ']')
        