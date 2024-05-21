import os
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.generic import TemplateView
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


#import datamolo.scr.add_item_in_model as scr
import datamolo.scr.figures as fig
import datamolo.scr.alignments as align
import datamolo.scr.database as db
import datamolo.tasks as tasks

import datamolo.models as data

from VazySearch.views import SearchEngine


# Create your views here.
class Main(TemplateView):
    
    template_name = os.path.join("datamolo", "main.html")
    moduleCard_template = os.path.join("datamolo", "moduleCard.html")
    template_mainFigure = os.path.join("datamolo", "mainFigure_00.html")
    template_mainProfile = os.path.join("datamolo", "mainProfileFigure_00.html")


    def new_session(request):
        # if cookie already exists -> so does Session
        sessionID = request.COOKIES.get('session')
        if(sessionID):
            try: 
                # destroy the previous session
                session = data.Session.objects.get(id=sessionID)
                session.delete()
            except:
                pass
        # new session
        session = data.Session.objects.create()
        response = render(request, Main.template_name, {'SESSION':session})
        response.set_cookie('session', session.id)
        response.delete_cookie('tempFasta')
        return response


    def fixing_starting_points(request):
        def LOAD_protein():
            proteins = db.parse_from_json('Protein')
            for prot in proteins:
                data.Protein.UPDATE(prot)
        def WRITE():
            db.write_to_json('Organism', data.Organism.objects.all())
            db.write_to_json('PolyProtein', data.PolyProtein.objects.all())
            db.write_to_json('Protein', data.Protein.objects.all())
        def WRITE_ALL():
            db.write_to_json('Activity', data.Activity.objects.all())
            db.write_to_json('Modulo', data.Modulo.objects.all())
            db.write_to_json('Profile', data.Profile.objects.all())
            db.write_to_json('Organism', data.Organism.objects.all())
            db.write_to_json('PolyProtein', data.PolyProtein.objects.all())
            db.write_to_json('Protein', data.Protein.objects.all())
            db.write_to_json('Subseq', data.Subseq.objects.all())

                #
        #data.Activity.objects.create()
        
        
        return HttpResponse("C'est Ok !")

    def get_Module_from_searchEngine(request, *args, **kwargs):
        context={}
        mod_id = kwargs['Modulo']

        if(not len(data.Modulo.objects.filter(id=mod_id))>0):
            return HttpResponse("Modulo not found")
        
        module = data.Modulo.objects.get(id=mod_id)
        profile = data.Profile.objects.get(modulo=module)
        ## ModuloCard
        mod_context:dict = {}
        mod_context['module'] = module
        mod_context['method'] = "Aligned"
        mod_context['profile_id'] = profile.id
        mod_context['profile_length'] = len(data.Subseq.objects.filter(profile=profile))
        mod_context['Structures'] = [structure for structure in data.Structure.objects.filter(modulo=module)]
        mod_context['common_ancestor'] = profile.LastCommonAncestor()
        context["Module"] = render_to_string(request=request, template_name=Main.moduleCard_template, context=mod_context)

        ## ProfileLogo
        outfile_path = os.path.join(settings.DATA_DIR, 'profiles', mod_id+".aln.fasta")
        ProfileLogo_context = {'profile': fig.generate_mainfigure_profile(outfile_path, "Aligned" )}
        context["ProfileLogo"] = render_to_string(request=request, template_name=Main.template_mainProfile, context=ProfileLogo_context)

        # check SESSION
        sessionID = request.COOKIES.get('session')
        new_session:bool = True
        if not sessionID:
            SESSION = data.Session.objects.create()
        else:
            SESSION = data.Session.objects.get(id=sessionID)
            new_session = False
        context['SESSION'] = SESSION
        SESSION.save()

        # render HTML
        print('searchEngine result', mod_id)
        context['searchForm'] = SearchEngine.searchForm()
        responseHTML = render(request, Main.template_name, context)
        if new_session:
            responseHTML.set_cookie('session', SESSION.id)
            responseHTML.delete_cookie('tempFasta')
        return responseHTML


    def get_mainProtein_from_searchEngine(request, *args, **kwargs):
        context:dict = kwargs.get('context', {})
        
        # generate protein figure
        if 'DB_ac' in kwargs:
            DB_ac = kwargs['DB_ac']
            proteins = data.Protein.objects.filter(data_ac=DB_ac, derivedFromPP=False)
            if len(proteins) == 0:
                context["searchError"] = 'DB_ac : ' + str(DB_ac) + " Does not exist yet !"
                #print(DB_ac, "Does not exist yet !")
                protein_id:int = -1
            else :
                protein_id:int = proteins[0].id
        
        elif 'protein_id' in kwargs:
            protein_id = kwargs['protein_id']
            proteins = data.Protein.objects.filter(id=protein_id)
            if len(proteins) == 0:
                context["searchError"] = 'The protein id : ' + str(protein_id) + " Does not exist yet !"
                #print(protein_id, "Does not exist yet !")
                protein_id:int = -1
            else :
                protein_id:int = proteins[0].id
     
        # Get protein
        if protein_id >= 0:
            protein = data.Protein.objects.get(id=protein_id)
            context['Protein'] = Main.generate_mainfigure_protein(protein)
        
        # check SESSION
        sessionID = request.COOKIES.get('session')
        new_session:bool = True
        if not sessionID:
            SESSION = data.Session.objects.create()
        else:
            SESSION = data.Session.objects.get(id=sessionID)
            new_session = False
        context['SESSION'] = SESSION
        if protein_id >= 0:
            SESSION.protein = protein.id
        SESSION.save()

        # render HTML
        print('searchEngine result', protein_id)
        context['searchForm'] = SearchEngine.searchForm()
        responseHTML = render(request, Main.template_name, context)
        if new_session:
            responseHTML.set_cookie('session', SESSION.id)
            responseHTML.delete_cookie('tempFasta')
        return responseHTML


    def index(request):

        context:dict = {}

        sessionID = request.COOKIES.get('session')
        new_session:bool = True
        if(sessionID):
            SESSION = data.Session.objects.get(id=sessionID)
            new_session = False
            context['SESSION'] = SESSION
            print('session', SESSION.id)
            
            if(SESSION.protein):
                print('session protein.id', SESSION.protein)
                protein_id = SESSION.protein
                protein = data.Protein.objects.get(id=protein_id)
            else:
                protein = data.Protein.random()
                print('random protein.id', protein.id)
                pass

            context['Protein'] = Main.generate_mainfigure_protein(protein)
            if(SESSION.subseq):
                SESSION.module = None
                SESSION.subseq = None
            
            if(SESSION.proteins):
                proteins = SESSION.proteins.split(' ')
                print('proteins', len(proteins))
                html:str = ""
                for protein_id in proteins:
                    protein = data.Protein.objects.get(id=protein_id)
                    html += fig.generate_minusfigure_protein(protein) + '\n'
                context['proteins'] = mark_safe(html)
            
            if(SESSION.profile and SESSION.logo_prot_path):
                context['ProfileLogo'] = mark_safe(fig.generate_mainfigure_profileLogo(SESSION.logo_prot_path))
                pass
        else:
            SESSION = data.Session.objects.create()
            context['SESSION'] = SESSION
        
        context['searchForm'] = SearchEngine.searchForm()
        responseHTTP = render(request, Main.template_name, context)

        if new_session:
            responseHTTP.set_cookie('session', SESSION.id)
            responseHTTP.delete_cookie('tempFasta')
        return responseHTTP


    def generate_mainfigure_protein(protein:data.Protein) -> dict:
        """ Calculate all parameters of each feature of the given protein into a dict \\
            It is passed to a sub-template included in the Main template """
        return fig.generate_mainfigure_protein(protein, showhide_allnsp=False) #new
        #return render_to_string(Main.template_mainFigure, {'figure':fig.generate_mainfigure_protein(protein, True)}) #new #broken
        #return {'Protein': fig.generate_mainfigure_protein_old(protein)}


    def load_mainfigure_protein(request):
        # AJAX

        sessionID = request.COOKIES.get('session')
        if(sessionID):
            SESSION = data.Session.objects.get(id=sessionID)

            #protein = data.Protein.random()
            protein = list(data.Protein.objects.filter(isPP=True, data_ac=0))[-1]

            SESSION.protein = protein.id
            SESSION.save()

            updated_html:str = ""
            updated_html = Main.generate_mainfigure_protein(protein)

            return HttpResponse(updated_html)
        return HttpResponse(mark_safe("<p>session not valid : please accept our cookies</p>"))


    def load_plusfigure_protein(request, protein_id):
        # display minus protein in mainfocus
        #ajax POST
        sessionID = request.COOKIES.get('session')
        if(sessionID):
            SESSION = data.Session.objects.get(id=sessionID)
            SESSION.protein = protein_id
            SESSION.save()

            protein = data.Protein.objects.get(id=protein_id)
            updated_html:str = Main.generate_mainfigure_protein(protein)
        
            return HttpResponse(updated_html)
        return HttpResponse(mark_safe("<p>session not valid : please accept our cookies</p>"))
        

    def load_minusfigure_protein(request):
        # place the mainfocused protein in minusfocus
        #Ajax
        sessionID = request.COOKIES.get('session')
        if(sessionID):
            SESSION = data.Session.objects.get(id=sessionID)
            
            if(SESSION.protein):
                protein = data.Protein.objects.get(id=SESSION.protein)
                SESSION.add_protein_minus(protein.id)
                SESSION.save()

                updated_html:str= ""
                updated_html = fig.generate_minusfigure_protein(protein)

                return HttpResponse(updated_html)
            else:
                print("wut !")
                return mark_safe("wut !")
        return HttpResponse(mark_safe("<p>session not valid : please accept our cookies</p>"))


    def load_card_module(request, subseq_id):
        #ajax
        sessionID = request.COOKIES.get('session')
        if(sessionID):
            SESSION = data.Session.objects.get(id=sessionID)
            context:dict = {}
            SESSION.subseq = subseq_id
            SESSION.save()

            subseq = data.Subseq.objects.get(id=subseq_id)
            if(subseq.profile):
                module_id = subseq.profile.modulo.id
                module = data.Modulo.objects.get(id=module_id)
                context['module'] = module
                context['subseq'] = subseq
                context['method'] = subseq.profile.method
                context['profile_id'] = subseq.profile.id
                context['profile_length'] = len(data.Subseq.objects.filter(profile=subseq.profile))
                context['Structures'] = [structure for structure in data.Structure.objects.filter(modulo=subseq.profile.modulo)]
                context['common_ancestor'] = subseq.profile.LastCommonAncestor()

            return render(request, Main.moduleCard_template, context)
        return HttpResponse(mark_safe("<p>session not valid : please accept our cookies</p>"))


    def get_mainfigure_profile(request, profile_id):
        """ profile info when profile link is clicked on module card """      
        # initate the sequence alignment and setting cookie to notify that the process has begun  
        #ajax
        ## 
        #+ [event : request POST] : AJAX : get_profile(request, profile_id)
        # input is profile (already aligned) : data.profile.aligned (bool) == true
        #   \-> read aligned fasta file
        # :: 
        # align sequences prot with muscle (task)
        #   \-> [event : repeated call] : AJAX : read aligned  outfile
        # => fig.msaViewer(aligned file: string or fileHandler or filePath)
        # # 
        sessionID = request.COOKIES.get('session')
        if(sessionID):
            SESSION = data.Session.objects.get(id=sessionID)
            SESSION.set_profile(profile_id)  # launch fastaformat & run_align(muscle)
            SESSION.save()

            # set up a cookie
            response = HttpResponse("")
            response.set_cookie('tempFasta', SESSION.logo_prot_path)

            # set up a task
            #file_path = os.path.join(settings.MEDIA_ROOT, 'temp', SESSION.logo_prot_path)
            #tasks.wait_for_muscle_outfile(file_path)

            # immediate response
            return response
        return HttpResponse(mark_safe("<p>session not valid : please accept our cookies</p>"))
    
    
    def check_mainfigure_profile(request):
        # AJAX GET 
        # read cookie 'tempFasta'
        tempFasta = request.COOKIES.get('tempFasta')
        
        # if task is ready
        outfile_path = os.path.join(settings.MEDIA_ROOT, 'temp', tempFasta) + '.out'
        task = tasks.check_outfile_ready(outfile_path)
        if(task == True):
            return Main.load_mainfigure_profile(request, tempFasta)
        else:
            response = HttpResponse("<p>Please wait few seconds more.</p>")
            return response


    def load_mainfigure_profile(request, tempFasta):
        outfile_path = os.path.join(settings.MEDIA_ROOT, 'temp', tempFasta) + '.out'
        outfile_path = outfile_path
        context = {'profile': fig.generate_mainfigure_profile(outfile_path, 'OnTheFly')}
        response = render(request, Main.template_mainProfile, context)
        response.delete_cookie('tempFasta')
        return response
        

    # works !
    def download(request):
        dirpath = os.path.join(settings.MEDIA_ROOT, 'data', 'sequences.fasta')
        if(os.path.exists(dirpath)):
            handle = open(dirpath, 'r')
            response = HttpResponse(handle, content_type=dirpath)
            response['Content-Disposition'] = f"attachment; filename=sequences.fasta"
            return response
        return HttpResponse("not found")


########################################################################################
########################################################################################
########################################################################################
