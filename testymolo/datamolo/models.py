from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
#from django_mysql.models import ArrayField


fs = FileSystemStorage(location="/media/data")


# DEBUG class
class DATA(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    file = models.FileField(storage=fs)



# Create your models here.

class Modulo(models.Model):
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

    # Don't get ahead of ourselves
    ## , on_delete=models.CASCADE)
    
    # profile = models.OneToOneField(Profile)  # FK
    # annotation = models.OneToOneField(Annotation)  # FK



class Profile(models.Model):
    """group of sub-sequences --like ModO_limits-- \
        divided for each Modulo 
    """
    # id = models.AutoField(primary_key=True)  # PK
    validated = models.BooleanField(default=False)
    modulo = models.OneToOneField(Modulo, on_delete=models.CASCADE) #FK

    # filepath = models.CharField(max_length=300)  # filepath = filefield( ? )



class Organism(models.Model):
    #:166
    id = models.IntegerField(primary_key=True)  # Tax_id[PK](int)
    name = models.CharField(verbose_name="abbreviate name", max_length=100)  # shortname (str)
    phylogeny = models.CharField(max_length=200)  # phylogeny absolute path



class Protein(models.Model):
    #id autofield #PK
    organism = models.ForeignKey(Organism, on_delete=models.PROTECT)  #FK
    name = models.CharField(verbose_name="used name", max_length=100)
    data_ac = models.IntegerField(verbose_name="VAZyMolO 1 CAZy_DB_id")  #old  #safeKeeping
    header = models.CharField(max_length=30)  #fasta
    sequence = models.TextField(blank=True)  #sequence  #fasta


class Subseq(models.Model):
    #id autofield #PK
    origin = models.ForeignKey(Protein, on_delete=models.CASCADE)  #FK
    profile = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)  #FK
    start = models.IntegerField()
    end = models.IntegerField()
    


class Structure(models.Model):
    """Structure of reference, but not sure if one-to-one of one-to-many

    For now : one-to-many
    """
    id = models.CharField(verbose_name="PDB accession", primary_key=True, max_length=4)  # PK
    modulo_id = models.ForeignKey(Modulo, on_delete=models.CASCADE)  # FK
    reference = models.BooleanField(default=False)



class Annotation(models.Model):
    Tables_SQL = (
        ("Prot_Infos", "information"),
        ("Prot_MOTIF", "motifs"),
        ("Prot_MUT", "mutants"),
        ("Prot_REG", "other regions of interest"),
        ("Prot_RI", "regions of interest"),
        ("CAZy_GB_GP", "genome"),
        ("CAZy_PDB", "structure"),
        ("CAZy_PP", "polyprotein"),
        ("CAZy_SP", "single protein"),
    )

    id = models.AutoField(primary_key=True)  # PK
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE) # FK
    tab = models.CharField(verbose_name="type of annotation", max_length=10, choices=Tables_SQL)
    data_ac = models.IntegerField()
    
    origin = models.ForeignKey(Subseq, null=True ,verbose_name="subseq of origin", on_delete=models.SET_NULL)  # -> FK(subseq) 

    #numb_origin -> start(int) and end(int)
    start_origin = models.IntegerField()
    end_origin = models.IntegerField()

    #numb_profile -> start(int) and end(int)
    start_profile = models.IntegerField()
    end_profile = models.IntegerField()
    



class Protein_alt(models.Model):
    
    ### line number in multifasta file
    id = models.IntegerField(primary_key=True, verbose_name="intern accession number")  #PK 

    organism = models.ForeignKey(Organism, on_delete=models.PROTECT)  #FK
    
    name = models.CharField(verbose_name="used name", max_length=100)
    
    data_ac = models.IntegerField(verbose_name="VAZyMolO 1 CAZy_DB_id")  #old  #safeKeeping

