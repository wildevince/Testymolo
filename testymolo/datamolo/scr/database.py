import re, os, json
import Bio
import numpy as np
import subprocess as sh

from django.conf import settings

from Bio import Entrez
import Bio.Blast.NCBIXML as BlastXML
from datetime import datetime

Entrez.email = "VIMVer@univ-amu.fr"
data_1_path:str = settings.TABLES_CSV
data_2_path:str = settings.DATA_DIR

# 
def write_to_json(table, objects):
    outfile = os.path.join(settings.DATA_DIR, table+".temp.json")
    with open(outfile, 'w') as handle:
        txt:list = list([json.dumps(item.serialize()) for item in objects])
        handle.write('[\n'+ ',\n'.join(txt) + ']')

def parse_from_json(table:str, param='temp') -> list:
    table += '.'+param
    table += ".json"
    infile = os.path.join(settings.DATA_DIR, table)
    with open(infile) as handle:
        return json.loads(handle.read())

def read_data_1(filename:str):
    with open(os.path.join(data_1_path, filename+".csv")) as handle:
        rows:list = []

        for line in handle.readlines():
            line = line.strip(';') # removing terminal ';' 
            values:list = [] # re-initialize value list
            val:str = "" # current parsing value
            inquote:bool = False # re-initialize in quote : False
            quote_char:str = '' # ' or "
            for c in line:
                if(c == ','): # encounter comma
                    if(not inquote): ## and not in quote
                        val = val.strip("'")
                        val = val.strip('"')
                        if(len(val) > 0):
                            values.append(val)
                        else:
                            values.append(None)
                        val = ""
                        continue
                elif(c == '"' or c == "'"): # encounter quote
                    if(inquote): # already in quote 
                        if(quote_char == c):  # encounter ending quote mark
                            inquote = False
                        else: # encounter the other quote mark 
                            pass
                    else: # encounter starting quote mark
                        inquote = True
                        quote_char = c
                elif((c == ' ' or c == '\n') and not inquote):  # get rid of whitespaces
                    continue
                val += c
            if(len(val)>0):
                val = val.strip("'")
                val = val.strip('"')
                values.append(val)

            if(len(values) > 0):
                rows.append(values)
                #print(values)  
        
        #print("nbr of col", set([len(row) for row in rows]))
        #print("nbr of rows", len(rows))
        return rows
      
def read_data_2(filename:str):
    with open(os.path.join(data_2_path, filename+".json")) as handle:
        return json.loads(handle.read())


def run_taxonkit(taxid:str) -> str:
    # return html content
    var = sh.run(["taxonkit","list", "--show-rank", "--show-name", "--indent", "    ", "--ids", taxid, "-J"], stdout=sh.PIPE, stderr=sh.PIPE, text=True)
    var_json = json.loads(var.stdout)

    def json2html(data:dict) -> str:
        #recursive
        txt:str = ""
        for line, subdata in data.items():
            line:str = line.strip()
            txt += "<li>"+line+"</li>"
            
            if len(subdata) > 0: #sub_clade
                txt += "<ul>" + json2html(subdata) + "</ul>"
        return txt

    return "<ul>"+json2html(var_json)+"</ul>"


def parse_vazy_data_1(Vazy1:dict) -> str:
    text:str = "<p>VaZyMolO.data 1</p>"
    for key, item in Vazy1.items():
        text += "<p>"+key+"</p>"
        text += "<ul>"
        for value in item:
            text += "<li>"+str(value)+"</li>"
        text += "</ul>"
    
    return text


def run_diamond_blastp(fastaseq:str) -> str:
    # return `out.fasta` 
    #         0       1      2   3                                  4   5                   6   7      8 9
    terms = "diamond blastp -d ./viral_protein_db/Nidovirales/nido -q ./protein_test.fasta -o ./var_4 -f 5"
    terms = terms.split(' ')
    infile = os.path.join(settings.MEDIA_ROOT, 'temp', 'protein_test.fasta')
    with open(infile, 'w') as handle:
        handle.write(fastaseq)
        terms[5] = infile
    terms[3] = os.path.join(settings.DATA_DIR, 'viral_protein_db', 'Nidovirales','nido')
    terms[7] = os.path.join(settings.MEDIA_ROOT, 'temp', datetime.now().strftime("%Y-%m-%d")+'.fasta')
    
    diamond_run = sh.run(terms, stderr=sh.PIPE, stdout=sh.PIPE, text=True)
    print(' '.join(terms))

    return terms[7]


def check_blastp_outfile_ready(outfile_name:str):
    outfile_path = os.path.join(settings.MEDIA_ROOT, 'temp', outfile_name)
    try:
        open(outfile_path, 'r')
        return True
    except Exception as e:
        print(e)
        return False
    

def parse_blastp_outfile(outfile:str) -> list:
    answer:list = []
    outfile = os.path.join(settings.MEDIA_ROOT, 'temp', outfile)
    with open(outfile) as handle:
        result = BlastXML.parse(handle)
        for record in result:
            for hit in record.alignments:
                id = hit.hit_id
                definition = hit.hit_def
                start = hit.hsps[0].sbjct_start
                end = hit.hsps[0].sbjct_end
                query_length = record.query_length 
                query_end = hit.hsps[0].query_end
                query_start = hit.hsps[0].query_start
                hit_length = hit.length
                align_length = hit.hsps[0].align_length 
                _query_coverage = str('{:10.2f}'.format((query_end-query_start+1)*100.0/query_length)).strip()
                _hit_coverage = str('{:10.2f}'.format((end-start+1)*100.0/hit_length)).strip()
                identities = hit.hsps[0].identities
                _identities = str('{:10.2f}'.format(identities*100.0/align_length)).strip()
                positives = hit.hsps[0].positives
                _positives = str('{:10.2f}'.format(positives*100.0/align_length)).strip()
                bits = hit.hsps[0].bits
                answer.append({
                    'id': id,
                    'start': start,
                    'end': end,
                    'query_length':query_length,
                    'hit_length':hit_length,
                    'align_length': align_length,
                    'query_coverage':_query_coverage,
                    'hit_coverage':_hit_coverage,
                    'identities': identities,
                    'Identities': _identities,
                    'positives': positives,
                    'Positives': _positives,
                    'bits':bits,
                    'definition':definition
                })
    return answer
