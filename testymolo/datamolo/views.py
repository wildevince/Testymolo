import os

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.generic import TemplateView
from django.utils.safestring import mark_safe


#import datamolo.scr.add_item_in_model as scr
import datamolo.scr.figures as fig
import datamolo.scr.alignments as align

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
        response = render(request, Main.template_name, {})
        response.set_cookie('session', session.id)
        return response


    def index(request):

        context:dict = {}

        sessionID = request.COOKIES.get('session')
        if(sessionID):
            SESSION = data.Session.objects.get(id=sessionID)
            
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
            
            if(SESSION.profile):
                context['ProfileLogo'] = "<p>work in progress</p>" 
                #fig.generate_mainfigure_profileLogo(sessionID)

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


    def load_mainfigure_profile(request, profile_id):
        #ajax
        sessionID = request.COOKIES.get('session')
        if(sessionID):
            SESSION = data.Session.objects.get(id=sessionID)
            SESSION.profile = profile_id
            SESSION.save()

            Subseqs:dict = {}
            Subseqs['id'] = profile_id
            profile = data.Profile.objects.get(id=profile_id)
            # gather all subseq.sequence when subseq.profile = profile
            for subseq in data.Subseq.objects.filter(profile=profile):
                Subseqs[str(subseq.id)] = {'header': subseq.header() ,'sequence':subseq.sequence}

            align.to_fasta_to_align(Subseqs)  # launch fastaformat & run_align(muscle)

            # to_model
            temp = data.TempFasta.objects.create(
                path = os.path.join(settings.MEDIA_ROOT, 'temp/') + "temp.fasta",
                filename = "temp.fasta",
                profile_id = profile_id
            )
            response = HttpResponse(f"<div class='logo' id='{profile_id}'></div>")
            response.set_cookie('tempFasta', temp.id)

            return response
        return HttpResponse(mark_safe("<p>session not valid : please accept our cookies</p>"))


    def load_mainfigure_logo(request):

        sessionID = request.COOKIES.get('session')
        tempFastaID = request.COOKIES.get('tempFasta')
        if(sessionID and tempFastaID):
            ### Is the alignment ready yet ?
            ### -> yes -> fig.generate_logo(...)
            return mark_safe("<p>The World !</p>")
        else:
            # errors
            return HttpResponse(mark_safe("<p>session not valid : please accept our cookies</p>"))


    # works !
    def download(request):
        dirpath = os.path.join(settings.MEDIA_ROOT, 'data', 'sequences.fasta')
        if(os.path.exists(dirpath)):
            handle = open(dirpath, 'r')
            response = HttpResponse(handle, content_type=dirpath)
            response['Content-Disposition'] = f"attachment; filename=sequences.fasta"
            return response
        return HttpResponse("not found")