import os
from subprocess import Popen , DEVNULL

from django.conf import settings
import datamolo.models as data
from Bio.Align.Applications import MuscleCommandline


def to_fasta_to_align(data:dict):
    # to_fasta 
    # fasta formating : 60 residues per line
    filepath = data['file']
    with open(filepath, 'w') as handle:
        for fasta in data['subseq']:
            handle.write(">"+fasta['header']+"\n")
            sequence = fasta['sequence']
            while (len(sequence) < 60):
                handle.write(sequence[0:60]+"\n")
                sequence = sequence[60:]
            handle.write(sequence+"\n")
    # to_align
    out_filepath = filepath+'.out'
    command:str = f"muscle -in {filepath} -out {out_filepath} -quiet"
    Popen(command.split(' '), stdout=DEVNULL)  # command must be a list of words
    pass