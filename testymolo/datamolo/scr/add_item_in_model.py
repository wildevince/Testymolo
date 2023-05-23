from models import *

import re
import json



def parse_data():
    data:dict = {}
    with open("../../testymolo/media/data/data.json") as handle:
        data = json.load(handle)
    for species in data:
        for sequence in data[species]:
            print(data[species][sequence]["annotation"][0])
            for subseq in data[species][sequence]["subseq"]:
                print(data[species][sequence]["subseq"][subseq])
                return

parse_data()


#Modulo.objects.create()