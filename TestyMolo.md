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