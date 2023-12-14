from os import path
import json

from django.db import models
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.conf import settings
#from django_mysql.models import ArrayField

import datamolo.scr.alignments as align
import VazySearch.scr as search


class Session(models.Model):
    # lifetime: 72h
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    protein = models.IntegerField(null=True)  #-> mainfocus figure
    profile = models.IntegerField(null=True)  #-> mainfocus logo
    logo_prot_path = models.FilePathField(null=True)
    module = models.CharField(null=True, max_length=10)  
    subseq = models.IntegerField(null=True)  #-> cardmodule
    phylo = models.IntegerField(null=True)   #-> phylo (wip)
    proteins = models.CharField(null=True, max_length=100)  #-> minus figures

    def set_profile(item, profileId):
        item.profile = profileId
        profile = Profile.objects.get(id=profileId)
        Subseqs:dict = {}
        Subseqs['id'] = profileId
        
        # gather all subseq.sequence when subseq.profile = profile
        subseqs = Subseq.objects.filter(profile=profile)
        
        if(len(subseqs)>0):
            date = timezone.now().strftime('%Y-%m-%d-%H-%M-%S')
            outpath = f"{item.id}_{profileId}_{date}.fasta"
            Subseqs['file'] = path.join(settings.MEDIA_ROOT, 'temp/') + outpath
            item.logo_prot_path = outpath

            Subseqs['subseq']:list = []
            for subseq in subseqs:
                Subseqs['subseq'].append({'header': subseq.header() ,'sequence':subseq.sequence()})

            align.to_fasta_to_align(Subseqs)  # launch fastaformat & run_align(muscle)

    def add_protein_minus(item, *proteinIDs):
        for proteinID in proteinIDs:
            proteinID = str(proteinID)
            if(not item.proteins):
                item.proteins = ' '.join([proteinID])
            proteins:list = item.proteins.split(' ')
            if not proteinID in proteins:
                proteins.append(proteinID)
                proteins.sort()
                item.proteins = ' '.join(proteins)
    
    def supp_protein_minus(item, *proteinIDs):
        for proteinID in proteinIDs:
            proteinID = str(proteinID)
            proteins:list = item.proteins.split(' ')
            if proteinID in proteins:
                proteins.remove(proteinID)
                item.proteins = ' '.join(proteins)


# Create your models here.

class Modulo(models.Model):
    #lvl 1
    id = models.CharField(primary_key=True, max_length=10)  # PK
    ### vazymolo 1 Modo_familiy_id

    ### Vazymolo
    complete = models.BooleanField(default=False)  

    activity = models.CharField(verbose_name="ExplorEnz EC classification", max_length=10, blank=True) 
    ### ex: "#.#.#.#" ExplorEnz EC classification

    ModuloFamily_choice = (
        ("UNK", "unknown"),
        ("S", "surface"),
        ('F', "functional"),
        ('DISF', "disorder functional"),
        ('M', "matrice"),
        ('IHD', "?"),
        ('HD', "hydrophobic domain"),
        ('ITM', "???"),
        ('TM', "trans-membrane"),
        ('LNK', "link"),
        ('IC', "????"),
        ('NF', "?????"),
        ('PS', "peptide signal"),
        ('EX', "??????"),
        ('DIS', "disorder"),
        ('DISS', "disorder surface"),
    )
    moduloFamily = models.CharField(verbose_name="type of molulo",choices=ModuloFamily_choice, max_length=6)

    def Get_Family(id:str):
        result:str = ""
        for i in range(len(id)):
            if not id[i].isdigit():
                result += id[i]
            else:
                break
        return result

    def Do_exist(modulo_id:str):
        for choice in Modulo.ModuloFamily_choice:
            if(modulo_id.startswith(choice[0])):
                return True
        return False

    def serialize(item):
        return {
            "id":item.id,
            "activity":item.activity,
            "moduloFamily":item.moduloFamily,
            "complete":item.complete
        }
    
    @staticmethod
    def SEARCH(kw:str) -> list :
        #return list[tuple(item, score)]
        result:list = []
        for item in Modulo.objects.all():
            score = item.search(kw)
            if score > 0.1:
                result.append(item, score)
        return result.sort()
    
    def search(self, kw:str) -> float:
        #return score
        score:int = 0
        # activity ?
        for k,w in self.ModuloFamily_choice:
            if kw == k:
                score += 1
                return score
            elif k.startswith(kw):
                score += 0.33 
            elif kw in w:
                score += 0.125
        return max(score,1)



class Profile(models.Model):
    """group of sub-sequences --like ModO_limits-- \
        divided for each Modulo 
    """
    #lvl 2
    # id = models.AutoField(primary_key=True)  # PK
    validated = models.BooleanField(default=False)
    modulo = models.OneToOneField(Modulo, on_delete=models.CASCADE) #FK

    ### Vazymolo
    complete = models.BooleanField(default=False)  

    def serialize(item, json=True):
        return {
            'id': item.id,
            'validated': item.validated,
            'modulo': item.modulo.id,  #(str)
            'complete': item.complete
        }
    # filepath = models.CharField(max_length=300)  # filepath = filefield( ? )


class Organism(models.Model):
    #lvl 1
    #:166
    id = models.IntegerField(verbose_name="Tax_id", primary_key=True)  # Tax_id[PK](int)
    name = models.CharField(verbose_name="scientific name", max_length=100)  # realname (str)
    abr = models.CharField(verbose_name="abbreviate name", max_length=25)  # shortname (str)
    group = models.CharField(verbose_name="classification", max_length=50)  # shorten used classification
    phylogeny = models.CharField(max_length=200)  # phylogeny absolute path

    ### Vazymolo
    complete = models.BooleanField(default=False)  

    def serialize(item, complete=True):
        result:dict = {
            "id":item.id,
            "name":item.name,
            "abr":item.abr,
            'group':item.group,
            "phylogeny":item.phylogeny,
        }
        if complete :
            result['complete'] = item.complete
        return result
    
    @staticmethod
    def SEARCH(kw:str) -> list :
        #return list[tuple(item, score)]
        result:list = []
        for item in Modulo.objects.all():
            score = item.search(kw)
            if score > 0.1:
                result.append(item, score)
        return result.sort()
    
    def search(self, kw:str) -> float:
        score:float = 0

        # id
        if kw == str(self.id):
            score += 1
            return score
        
        # group
        align_group:float = search.word_aligner(self.group, kw)
        score += ( 0.20 * align_group )
        
        # name
        align_name:float = search.word_aligner(self.name, kw)
        score += ( 0.35 * align_name )

        # abr
        align_abr:float = search.word_aligner(self.abr, kw, True)
        score += ( 0.55 * align_abr)
        
        # phylo 
        align_phylo:float = search.taxo_aligner(self.phylogeny, kw)
        score += align_phylo

        return max(score, 1,0)
    
    @staticmethod
    def ADD(indata:dict):
        if len(Organism.objects.filter(id=indata['Organism']['id'])) > 0 :
            org = Organism.objects.get(id=int(indata['Organism']['id']))
        else:
            org = Organism.objects.create(complete=True, **indata['Organism'])
        proteins = []
        for prot in indata['Protein']:
            proteins.append(Protein.objects.create(organism=org, data_ac=0, complete=True, **prot))
        for pp in indata['Polyprotein']:
            pp['PP'] = proteins[0]
            pp['protein'] = proteins[pp['protein']]
            PolyProtein.objects.create(**pp)

    
class Genome(models.Model):
    #lvl 2
    name = models.CharField(max_length=50, blank=True)
    genbank = models.CharField(verbose_name="Genbank accession number", max_length=30)
    organism = models.OneToOneField(Organism, on_delete = models.CASCADE)  #FK
    
    ### Vazymolo
    complete = models.BooleanField(default=False)  


class Protein(models.Model):
    #lvl 2
    #id autofield #PK
    isPP = models.BooleanField(verbose_name="is PolyProtein", default=False)
    derivedFromPP = models.BooleanField(verbose_name="derived_from_PolyProtein", default=False)
    organism = models.ForeignKey(Organism, db_column='abr', on_delete=models.PROTECT)  #FK
    genbank = models.CharField(max_length=20, default="")
    name = models.CharField(verbose_name="used name", max_length=100)
    definition = models.CharField(verbose_name="designation", max_length=20, default="")
    data_ac = models.PositiveIntegerField(verbose_name="VAZyMolO 1 CAZy_DB_id")  #old  #safeKeeping
    header = models.CharField(max_length=50)  #fasta
    sequence = models.TextField(blank=True)  #sequence  #fasta
    #codedBy = models.OneToOneField(CDS, verbose_name="coded by", blank=True, on_delete=models.CASCADE) 
    
    ### Vazymolo
    complete = models.BooleanField(default=False)  

    def serialize(item, json=True, **kwargs):
        result:dict =  {
            'id':item.id,
            "isPP":item.isPP,
            "derivedFromPP":item.derivedFromPP,
            "genbank":item.genbank,
            "name":item.name,
            "definition":item.definition,
            "data_ac":item.data_ac,
            'complete':item.complete,
        }
        #kwargs
        for key, val in kwargs.items():
            result[key] = val

        if json :
            result["organism"] = item.organism.id
            result["header"] = item.header
            result["sequence"] = item.sequence
            result["length"] = len(item.sequence)
        else:
            result['organism'] = item.organism
            result['fasta'] = item.header + '\n' + item.sequence
        return result

    @staticmethod
    def SEARCH(kw:str) -> list :
        #return list[tuple(item, score)]
        result:list = []
        for item in Modulo.objects.all():
            score = item.search(kw)
            if score > 0.1:
                result.append(item, score)
        return result.sort()
    
    def search(self, kw:str) -> float:
        score:float = 0

        # isPP
        align_PP:float = search.word_aligner('polyprotein', kw)
        score += ( 0.5 * align_PP )

        # genkank
        score_genbank = 1 if kw == self.genbank.split('.')[0] else 0
        score += score_genbank

        # name
        align_name:float = search.word_aligner(self.name, kw)
        score += ( 0.35 * align_name )

        # definition
        align_def:float = search.word_aligner(self.definition, kw, True)
        score += ( 0.35 * align_def)

        # sequence search for motifs
        regex_motif:bool = search.search_motif(kw, self.sequence)
        regex_motif_score:float = 1.0
        score += regex_motif_score

        return max(score, 1,0)
    

    def random():
        import random
        PROTEINS = Protein.objects.filter(derivedFromPP=False)
        N:int = len(PROTEINS)
        i = random.randint(1, N-1)
        return PROTEINS[i]
    
    def fasta(self):
        return self.header.strip() + '\n'+ self.sequence.strip()
    
    def get_all_nsps(self):
        if(self.isPP):
            nsps:list = PolyProtein.objects.filter(PP=self.id)
            return list([ nsp.protein for nsp in nsps ])
        else:
            return []

    @staticmethod
    def ADD(item:dict, can_modify=False, PP:dict=None):
        item_genbank = item['genbank']
        if not len(Protein.objects.filter(genbank=item_genbank)) > 0:
            if can_modify:
                prot = Protein.objects.get(id=item['id'])
                prot.derivedFromPP = item['derivedFromPP']
                prot.genbank = item['genbank']
                prot.name = item['name']
                prot.organism = Organism.objects.get(id=item['organism'])
                prot.header = item['header']
                prot.sequence = item['sequence']
                prot.definition = item['definition']
                prot.complete = True
                prot.save()
                print(prot.name, 'has been updated !')
                if PP:
                    PolyProtein.UPDATE(PP)
            else:
                prot = Protein.objects.create(**item)
                prot.complete = True
                prot.save()
                print(prot.name, 'has been created !')
                if PP:
                    PolyProtein.UPDATE(PP)

    @staticmethod
    def UPDATE(item:dict, PP:dict=None):
        prot = Protein.objects.get(id=item['id'])
        prot.derivedFromPP = item['derivedFromPP']
        prot.genbank = item['genbank']
        prot.name = item['name']
        prot.organism = Organism.objects.get(id=item['organism'])
        prot.header = item['header']
        prot.sequence = item['sequence']
        prot.definition = item['definition']
        prot.complete = True
        prot.save()
        print(prot.name, 'has been updated !')
        if PP:
            PP['protein'] = prot
            PolyProtein.UPDATE(PP)


class CDS(models.Model):
    #lvl 3
    protein = models.OneToOneField(Protein, verbose_name="protein product", on_delete=models.PROTECT)  #FK
    genome = models.ForeignKey(Genome, on_delete=models.CASCADE)  #FK
    name = models.CharField(max_length=200)
    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()
    sequence = models.TextField(verbose_name="nucleotide sequence")
    
    ### Vazymolo
    complete = models.BooleanField(default=False)  

    def serialize(item):
        return {
            "protein":item.protein.id,
            "name":item.name,
            "start":item.start,
            "end":item.end,
            "sequence":item.sequence,
            "length":len(item.sequence),
            "complete":item.complete
        }


class PolyProtein(models.Model):
    #lvl 3
    ## association class
    PP = models.ForeignKey(Protein, related_name="mother", verbose_name="Polyprotein", on_delete=models.CASCADE)  #FK  #priority
    protein = models.ForeignKey(Protein, related_name="child", verbose_name="Real Protein", on_delete=models.CASCADE)  #FK
    index = models.PositiveIntegerField()
    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()
    
    ### Vazymolo
    complete = models.BooleanField(default=False)  

    @staticmethod
    def UPDATE(item:dict):
        if isinstance(item['PP'], int) :
            item['PP'] = PolyProtein.objects.get(id=item['PP'])
        qq:dict = {'PP': item['PP'], 'index':item['index']}
        result:list = PolyProtein.objects.filter(**qq)
        if len(result) > 0:
            if len(result) > 1:
                for other in result[1:]:
                    other:PolyProtein
                    other.delete()
            pp:PolyProtein = result[0]
            pp.protein = item['protein']
            pp.start = item['start']
            pp.end = item['end']
            pp.save()
            print(pp.PP.id, pp.protein.id, ' has been updated !')
        else:
            # create
            PolyProtein.objects.create(**item)
            print(pp.PP.id, pp.protein.id, ' has been created !')

    @staticmethod
    def CLEAR():
        PolyProtein.objects.all().delete()
    
    @staticmethod
    def LOAD(indata:list):
        PolyProtein.CLEAR()
        #indata (json -> list[dict])
        for item in indata:
            item['PP'] = Protein.objects.get(id=item['PP'])
            item['protein'] = Protein.objects.get(id=item['protein'])
            PolyProtein.objects.create(**item)

    def serialize(item):
        return {
            "PP":item.PP.id,
            "protein":item.protein.id,
            "index":item.index,
            "start":item.start,
            "end":item.end,
        }
        

class Subseq(models.Model):
    #lvl 3
    ## association class
    #id autofield #PK
    origin = models.ForeignKey(Protein, on_delete=models.CASCADE)  #FK
    profile = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)  #FK
    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()
    
    ### Vazymolo
    complete = models.BooleanField(default=False)  

    class Meta:
        ordering = ['origin', 'start']

    def header(item) -> str:
        return f"{item.origin.header[:-1]}.{item.id}):[{item.start}-{item.end}]"

    def sequence(item) -> str:
        return str(item.origin.sequence[item.start-1:item.end])

    def serialize(item, json=True, **kwargs):
        result:dict = {}
        seq = item.origin.sequence[item.start-1:item.end]
        if(item.profile is not None):
            profile = int(item.profile.id)
            module = item.profile.modulo.id
        else:
            profile = -1
            module = 'null'
        if json:
            result = {
                "id": int(item.id),
                "origin": int(item.origin.id),
                "profile": profile,
                "start": int(item.start),
                "end": int(item.end)
            }
        else:
            result = {
                "id":item.id,
                "origin":item.origin.id,
                "profile":profile,
                "module":module,
                "start":item.start,
                "end":item.end,
                "sequence":seq,
                "length":len(seq),
                "complete":item.complete,
            }
        for k,v in kwargs.items():
            result[k] = v
        return result
    

class Structure(models.Model):
    #lvl 2
    """Structure of reference, but not sure if one-to-one of one-to-many

    For now : one-to-many
    """
    id = models.CharField(verbose_name="PDB accession", primary_key=True, max_length=4)  # PK
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)  #FK
    comment = models.CharField(max_length=200, default="")
    reference = models.BooleanField(default=False)
    origin = models.ForeignKey(Protein, on_delete=models.CASCADE)  #FK
    
    ### Vazymolo
    complete = models.BooleanField(default=False)  



class Annotation(models.Model):
    #lvl 4
    Tables_SQL = (
        ("Prot_Infos", "information"),
        ("Prot_MOTIF", "motif"),
        ("Prot_MUT", "mutant"),
        ("Prot_REG", "feature"),
        ("Prot_RI", "interaction"),
        ("CAZy_GB_GP", "genome"),
        ("CAZy_PDB", "structure"),
        ("CAZy_PP", "polyprotein"),
        ("CAZy_SP", "single protein"),
    )

    #id = models.AutoField(primary_key=True)  # PK
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE) # FK
    tab = models.CharField(verbose_name="type of annotation", max_length=10, choices=Tables_SQL)
    data_ac = models.PositiveIntegerField()
    value = models.CharField(max_length=200)
    
    origin = models.ForeignKey(Protein, null=True ,verbose_name="protein of origin", on_delete=models.SET_NULL)  # -> FK(subseq) 

    #numb_origin -> start(int) and end(int)
    start_origin = models.PositiveIntegerField()
    end_origin = models.PositiveIntegerField()

    #numb_profile -> start(int) and end(int)
    start_profile = models.PositiveIntegerField(default=0)
    end_profile = models.PositiveIntegerField(default=0)
    
    ### Vazymolo
    complete = models.BooleanField(default=False)  

   