from django.db import models
#from django_mysql.models import ArrayField


# Create your models here.


class Modulo(models.Model):
    """annotation (lvl 1)

    Args:
        models (_type_): _description_
    """
    id = models.CharField(primary_key=True, max_length=10)  # PK
    name = models.CharField(max_length=100)



# lvl 1
# le plus fidele possible car tout le reste en depend

class Organism(models.Model):
    #:166
    # Tax_id [PK] (int)
    # Name (str)
    # abr (str):  (=CAZy_DB.abr)
    # Category (str): realm
    # Class (str): genome type ['ssRNA positive-strand viruses' Or 'ssRNA negative-strand viruses']
    # Order (str)
    # Family (str)
    # sFamily (str)
    # Genre (str)
    # Note (text)
    pass


class Mod_Families(models.Model):
    # lots of NULL instances !

    # Family (str) [PK] :
    # Family_Name (str):
    # Family_Activity (str):
    # Family_Taxo (str ArrayField):
    # Clan (str) : = sub families

    # description
    # Family_note (text)
    # Family_Private_note (text)
    # Fold (str) :

    # ModoS_uniqfct (str): bool yes/no
    # ModoS_Activity (text)
    # ModoS_Description (text)
    # ModoS_Fold (text)
    # ModoS_note (text)
    # ModoS_Private_note (text)

    # web_descript (str) : keywords
    # web_status (int) : [0 | 1]
    pass


class Motifs:
    pass


class EC_num:
    #:1
    pass


class Biblio_struct:
    #:2
    pass


class CAZyModO:
    # outdated
    #:2
    pass


# lvl 3
class Sequence(models.Model):
    """old CAZy_DB

    Args:
        models (_type_): _description_
    """
    # [PK] int auto-incrementation

    # id
    # protein
    # DB_name 'nickname' (str): [unused]
    # Organism.Tax_id (int): [FK]

    # ?
    # EC
    # _3D_status (str):

    # sequence
    #length (int)
    #sequence (text)

    # info
    #DB_note (text)
    #Created (date)
    #Modified (date)
    # PP_status (str): bool yes/no (Is sequence from poly-protein ?)
    # Lib_sort (text): list of keywords ?
