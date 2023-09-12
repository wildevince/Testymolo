import os

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.generic import TemplateView
from django.utils.safestring import mark_safe


#import datamolo.scr.add_item_in_model as scr
import datamolo.scr.figures as fig
import datamolo.scr.alignments as align
import datamolo.scr.database as db
import datamolo.tasks as tasks

import datamolo.models as data



# Create your views here.
class Main(TemplateView):
    
    template_name = os.path.join("datamolo", "main.html")
    moduleCard_template = os.path.join("datamolo", "moduleCard.html")

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


    def index(request):

        ###
        #db.parse_Modulo(data.Modulo.objects.all())
        #db.parse_Organism(data.Organism.objects.all())
        #db.parse_Protein(data.Protein.objects.all())
        ###

        context:dict = {}

        sessionID = request.COOKIES.get('session')
        if(sessionID):
            SESSION = data.Session.objects.get(id=sessionID)
            context['SESSION'] = SESSION
            
            if(SESSION.protein):
                protein_id = SESSION.protein
                protein = data.Protein.objects.get(id=protein_id)
                context['Protein'] = mark_safe(fig.generate_mainfigure_protein(protein))

                if(SESSION.subseq):
                    SESSION.module = None
                    SESSION.subseq = None
            
            if(SESSION.proteins):
                proteins = SESSION.proteins.split(' ')
                html:str = ""
                for protein_id in proteins:
                    protein = data.Protein.objects.get(id=protein_id)
                    html += fig.generate_minusfigure_protein(protein) + '\n'
                context['proteins'] = mark_safe(html)
            
            if(SESSION.profile and SESSION.logo_prot_path):
                #context['ProfileLogo'] = mark_safe(fig.generate_mainfigure_profileLogo(SESSION.logo_prot_path))
                pass

        else:
            Main.new_session(request)

        return render(request, Main.template_name, context)


    def load_mainfigure_protein(request):
        # AJAX

        sessionID = request.COOKIES.get('session')
        if(sessionID):
            SESSION = data.Session.objects.get(id=sessionID)

            protein = data.Protein.random()

            SESSION.protein = protein.id
            SESSION.save()

            updated_html:str = ""
            updated_html = fig.generate_mainfigure_protein(protein)

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
            updated_html:str = fig.generate_mainfigure_protein(protein)
        
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
                context['profile_id'] = subseq.profile.id
                context['profile_length'] = len(data.Subseq.objects.filter(profile=subseq.profile))
                context['Structures'] = [structure for structure in data.Structure.objects.filter(modulo=subseq.profile.modulo)]
                context['commun_ancestor'] = "'...'"

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
        for_logo:dict = {"outfile_path":outfile_path,'tempFasta':tempFasta}
        response = HttpResponse(fig.generate_mainfigure_profile(for_logo))
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
