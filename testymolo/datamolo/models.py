from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
#from django_mysql.models import ArrayField


fs = FileSystemStorage(location="/media/data")


# DEBUG class
class DATA(models.Model):
    """ temp dev only """
    id = models.CharField(primary_key=True, max_length=20)
    file = models.FileField(storage=fs)



# Create your models here.

class Modulo(models.Model):
    #lvl 1
    id = models.CharField(primary_key=True, max_length=10)  # PK
    ### vazymolo 1 Modo_familiy_id

    activity = models.CharField(verbose_name="ExplorEnz EC classification", max_length=10, blank=True) 
    ### ex: "#.#.#.#" ExplorEnz EC classification

    ModuloFamily_choice = (
        ("UNK", "unkwnow"),
        ("S", "surface"),
        ('F', "functional"),
        ('DISF', "disorder functional"),
        ('M', "matrice"),
        ('IHD', "?"),
        ('HD', "??"),
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

    # Don't get ahead of ourselves
    ## , on_delete=models.CASCADE)
    
    # profile = models.OneToOneField(Profile)  # FK
    # annotation = models.OneToOneField(Annotation)  # FK



class Profile(models.Model):
    """group of sub-sequences --like ModO_limits-- \
        divided for each Modulo 
    """
    #lvl 2
    # id = models.AutoField(primary_key=True)  # PK
    validated = models.BooleanField(default=False)
    modulo = models.OneToOneField(Modulo, on_delete=models.CASCADE) #FK

    # filepath = models.CharField(max_length=300)  # filepath = filefield( ? )



class Organism(models.Model):
    #lvl 1
    #:166
    id = models.IntegerField(primary_key=True)  # Tax_id[PK](int)
    name = models.CharField(verbose_name="abbreviate name", max_length=100)  # shortname (str)
    phylogeny = models.CharField(max_length=200)  # phylogeny absolute path


class Genome(models.Model):
    #lvl 2
    name = models.CharField(max_length=50, blank=True)
    genbank = models.CharField(verbose_name="Genbank accession number", max_length=30)
    organism = models.OneToOneField(Organism, on_delete = models.CASCADE)  #FK


class Protein(models.Model):
    #lvl 2
    #id autofield #PK
    isPP = models.BooleanField(verbose_name="is PolyProtein", default=False)
    derivedFromPP = models.BooleanField(verbose_name="derived_from_PolyProtein", default=False)
    organism = models.ForeignKey(Organism, on_delete=models.PROTECT)  #FK
    genbank = models.CharField(max_length=20, default="")
    name = models.CharField(verbose_name="used name", max_length=100)
    data_ac = models.PositiveIntegerField(verbose_name="VAZyMolO 1 CAZy_DB_id")  #old  #safeKeeping
    header = models.CharField(max_length=30)  #fasta
    sequence = models.TextField(blank=True)  #sequence  #fasta
    #codedBy = models.OneToOneField(CDS, verbose_name="coded by", blank=True, on_delete=models.CASCADE) 


class CDS(models.Model):
    #lvl 3
    protein = models.OneToOneField(Protein, verbose_name="protein product", on_delete=models.PROTECT)  #FK
    genome = models.ForeignKey(Genome, on_delete=models.CASCADE)  #FK
    name = models.CharField(max_length=200)
    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()
    sequence = models.TextField(verbose_name="nucleotide sequence")


class PolyProtein(models.Model):
    #lvl 3
    ## association class
    PP = models.ForeignKey(Protein, related_name="mother", verbose_name="Polyprotein", on_delete=models.CASCADE)  #FK
    protein = models.ForeignKey(Protein, related_name="child", verbose_name="Real Protein", on_delete=models.CASCADE)  #FK
    index = models.PositiveIntegerField()
    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()
    
    
class Subseq(models.Model):
    #lvl 3
    ## association class
    #id autofield #PK
    origin = models.ForeignKey(Protein, on_delete=models.CASCADE)  #FK
    profile = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)  #FK
    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()
    

class Structure(models.Model):
    #lvl 2
    """Structure of reference, but not sure if one-to-one of one-to-many

    For now : one-to-many
    """
    id = models.CharField(verbose_name="PDB accession", primary_key=True, max_length=4)  # PK
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)  # FK
    comment = models.CharField(max_length=200, default="")
    reference = models.BooleanField(default=False)



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
    


"""
class Protein_alt(models.Model):
    
    ### line number in multifasta file
    id = models.IntegerField(primary_key=True, verbose_name="intern accession number")  #PK 

    organism = models.ForeignKey(Organism, on_delete=models.PROTECT)  #FK
    
    name = models.CharField(verbose_name="used name", max_length=100)
    
    data_ac = models.IntegerField(verbose_name="VAZyMolO 1 CAZy_DB_id")  #old  #safeKeeping
"""
