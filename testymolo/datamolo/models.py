from django.db import models
#from django_mysql.models import ArrayField


# Create your models here.


class Profile(models.Model):
    """group of sub-sequences --like ModO_limits-- \
        divided for each Modulo 
    """
    id = models.AutoField(primary_key=True)  # PK
    # filepath = models.CharField(max_length=300)  # filepath = filefield( ? )


class Modulo(models.Model):
    id = models.CharField(primary_key=True, max_length=10)  # PK
    # , on_delete=models.CASCADE) Don't get ahead of ourselves

    # name = models.CharField(max_length=100)

    profile = models.OneToOneField(Profile)  # FK
    # annotation = models.OneToOneField(Annotation)  # FK


class Annotation(models.Model):
    Tables_SQL = (
        ("Prot_Infos", "Information"),
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
    tab = models.CharField(max_length=10, choices=Tables_SQL)
    data_ac = models.IntegerField()
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)


class Structure(models.Model):
    """Structure of reference, but not sure if one-to-one of one-to-many

    For now : one-to-many
    """
    id = models.CharField(primary_key=True, max_length=4)  # PK
    modulo_id = models.ForeignKey(Modulo, on_delete=models.CASCADE)  # FK


# lvl 1
# le plus fidele possible car tout le reste en depend

class Organism(models.Model):
    #:166
    id = models.IntegerField(primary_key=True)  # Tax_id[PK](int)
    name = models.CharField(max_length=100)  # shortname (str)
    phylogeny = models.CharField(max_length=200)  # phylogeny absolute path
