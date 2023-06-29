import os
from subprocess import Popen 

from django.conf import settings
import datamolo.models as data
from Bio.Align.Applications import MuscleCommandline


def to_fasta_to_align(data:dict):
    # to_fasta
    filepath = os.path.join(settings.MEDIA_ROOT, 'temp/') + "temp.fasta"
    with open(filepath, 'w') as handle:
        for id, fasta in data.items():
            handle.write(">"+fasta['header']+"\n")
            sequence = fasta['sequence']
            while (len(sequence) < 60):
                handle.write(sequence[0:60]+"\n")
                sequence = sequence[60:]
            handle.write(sequence+"\n")
    # to_align
    Popen(str(MuscleCommandline(cmd="muscle -quiet", input=filepath, out=filepath)).split(''))
    pass