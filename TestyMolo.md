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



{% for subseq in data.subseq %}
                    <rect class="subseq" height="20%" y="40%" fill="blue" film-opacity="0.4" 
                        x="" width=""  />
                    <line class="separator" y1="40%" y2="60%" stroke="black" stroke-width="2" 
                        x1="" x2=""  />
            {% endfor %}



<script>
            const data = JSON.parse($('#data'));
            const N = data.protein.length;
            var $svg = $(svg);
            let I = length(data.subseq);
            let i = 0;

            for (subseq in data.subseq) {
                
                $svg.innerhtml += '<rect class="subseq" height="20%" y="40%" fill="blue" fill-opacity="0.4" ';
                $svg.innerhtml += 'x="'+ subseq.start/N*100 +'%" width="'+ (subseq.start-subseq.end)/N*100 +'%"  />';
                
                i ++;
                if (i > I) {
                    $svg.innerhtml += '<line class="separator" y1="40%" y2="60%" stroke="black" stroke-width="2" ';
                    let pos = subseq.end/N*100;
                    $svg.innerhtml += 'x1="'+ pos +'%" x2="'+ pos +'%"  />';
                }                
                
            }
            
            $("rect.subseq").mouseover(function(){
                $(this).att("fill-opacity", "0.8");
            });
            $("rect.subseq").mouseout(function(){
                $(this).att("fill-opacity", "0.4");
            });

        </script>




        {% for protein in data %}
        <svg width="1860" height="400">
            <rect id="background" width="100%" height="100%" fill="grey" fill-opacity="0.1" stroke="black" />
            <rect id="protein" x="0%" y="40%" width="100%" height="20%" fill="blue" fill-opacity="0.1" />
            {{ protein|json_script }}
            {% for subseq in protein.subseq %}
                <rect class="subseq" id={{ subseq.id }} height="20%" y="40%" fill="blue" fill-opacity="0.2" 
                    x="{{ protein.subseq|subseq_rect_xpos:data.protein.length }}%" 
                    width="{{ protein.subseq|subseq_rect_width:data.protein.length }}%"  />
                <text class="module_name" id={{ subseq.id }} font-size='14' y="35%" x="{{ protein.subseq|subseq_rect_xpos:data.protein.length }}%" >{{ subseq.module }}</text>
                <line class="separator" id={{ subseq.id }} y1="40%" y2="60%" stroke="black" stroke-width="2" 
                    x1="{{ protein.subseq|subseq_line_xpos:data.protein.length }}%" 
                    x2="{{ protein.subseq|subseq_line_xpos:data.protein.length }}%"  />
                <text class="numbering" id={{ subseq.id }} font-size='10' y="65%" x="{{ protein.subseq|subseq_rect_xpos:data.protein.length }}%"  >{{ subseq.end }}</text>
            {% endfor %}
        {% endfor %}
        </svg>


        {% load data_extras %}

        <p><button value="false" onclick="switchSize()">size</button></p>

        {% for protein in data %}
            {{ protein|generate_svg }}
            {% endfor %}



## implement Database
        
        ### Organism , Protein , Subseq 
        ###scr.parse_data()  #-> done

        ### Modulo
        ###scr.parse_Modules()  #-> done

        ### Structure
        ### lack info

        ### link between Modulo--Subeq
        ### Subseq --+ Profile -1-1- Modulo   (facile => aggregation && one-to-one )
        ### Subseq +-- Annotation --* Modulo  (difficile => positioning within limits && sorting types of annotation)

        ### Subseq --+ Profile -1-1- Modulo   (facile => aggregation && one-to-one )


        ### need to hard flush and restart 
        #scr.parse_data() 
        
        ### BACKUP

        #Table_names = [tab[0] for tab in data.Annotation.Tables_SQL]
        #scr.parse_Annotations(Table_names) 

        ### BACKUP 2

        ### -> visualization JS tool !
        ### question: protein 375 -> polyprotein 1ab du HCoV