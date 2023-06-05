Testymolo 

Here the main stuff :
test positif control (ex: polymerase)
relation logic
fct proper name
phylogeny
thesauruses and dictionaries
pre-alpha


VAZyMolO 2 pre-alpha 
Data Base  -> Coronavirus
structure
filling
add all annotations 
    -> if necessary delete them all but one
missing elements ?  
structures ...
module proper names 
fct proper names

Back End (scripts)
alignment
search engine

Back End  (django)
views
models oki
forms
urls

Front End
HTML template
JS 



Expected flowline :
inputs: unknown sequence or keywords 
outputs : phylogenic tree or genome/protein data

unknoww 
sequence   -->  multialignment  ---
                                                                   --
                                                                       ----> phylogenic tree
                                                                   --           genome/ protein data
                                                            ---
 keywords -> search engine --- 




        ("Prot_Infos", "information"),
        ("Prot_MOTIF", "motif"),
        ("Prot_MUT", "mutant"),
        ("Prot_REG", "feature"),
        ("Prot_RI", "interaction"),
        ("CAZy_GB_GP", "genome"),
        ("CAZy_PDB", "structure"),
        ("CAZy_PP", "polyprotein"),
        ("CAZy_SP", "single protein"),



    def Make_Annotation(**kwargs):
        elif(len(l_module) == 1):
            module_id = kwargs["modules"][0]
            protein = Protein.objects.get(data_ac = kwargs["CAZy_DB__DB_ac"])
            Annotation.objects.create(
                modulo = Modulo.objects.get(id=module_id),
                tab = kwargs["tab"],
                data_ac = kwargs["data_ac"],
                value = kwargs["value"],  #dict(regex=csv[6], activity=csv[7], phylogeny=csv[8]),
                origin = protein ,
                start_origin = kwargs["start_origin"],
                end_origin = kwargs["end_origin"],
                start_profile = 0,
                end_profile = 0
            )
