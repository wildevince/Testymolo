from django import template
from django.http import JsonResponse
from django.utils.safestring import mark_safe

import datamolo.models as data

register = template.Library()


@register.filter(is_safe=True)
def subseq_rect_xpos(subseq, protein_len:int):
    return subseq["start"] / protein_len * 100


@register.filter(is_safe=True)
def subseq_rect_width(subseq, protein_len:int):
    return (subseq["length"]) / protein_len * 100

@register.filter(is_safe=True)
def subseq_line_xpos(subseq, protein_len:int):
    return (subseq["end"]) / protein_len * 100



@register.filter(is_safe=True)
def generate_svg(data:dict):
    WIDTH = 1860
    html:str = ""
    chtext:bool = False
    chlvl:int = 0

    #svg
    html += f"<svg width='{str(WIDTH)}' height='400'> \n"
    html += '<rect id="background" width="100%" height="100%" fill="grey" fill-opacity="0.1" stroke="black" /> \n'
    html += '<rect id="protein" x="0%" y="40%" width="100%" height="20%" fill="blue" fill-opacity="0.1" /> \n'
    text1 = f"name:{data['protein']['name']},    polyprotein:{data['protein']['isPP']},  derived from polyprotein:{data['protein']['derivedFromPP']}"
    text2 = f"organism:{data['protein']['organism']},    acc:{data['protein']['data_ac']},    length:{data['protein']['length']}"
    html += f"<text x='10' y='5%' >{text1}</text>"
    html += f"<text x='10' y='10%' >{text2}</text>"


    L = data["protein"]["length"]

    #features
    i = 0
    for subseq in data['subseq']:
        i += 1

        #rect subseq 
        html += f"<rect class='subseq' id='subseq_{subseq['id']}' height='20%' y='40%' fill='blue' fill-opacity='0.2' "
        w = subseq['length'] / L *100
        x = subseq['start'] / L *100
        html += f"x='{x}%' width='{w}%' />\n"
        if((w /100 *1800) < (WIDTH*0.02)):
            chtext = True
            chlvl += 1  
        else:
            chlvl = chlvl-1 if(chlvl > 0) else 0
        
        #text module_name
        html += f"<text class='module_name' id='module_name_{subseq['id']}' font-size='14' y='35%' "
        x += w*2/5
        html += f"x='{x}%' >{subseq['module']}</text>\n"
        
        #line separator
        html += f"<line class='separator' id='separator_{subseq['id']}' y1='40%' y2='60%' stroke='black' stroke-width='2' "
        x1 = subseq["end"] / L * 100
        html += f"x1='{x1}%' x2='{x1}%' />\n"

        #text numbering
        if(i < len(data['subseq'])):
            y = 65
            if(chtext):
                chtext = False
                y += 5*chlvl
            x = subseq["end"] / L * 100 
        else:
            text_length:int = len(str(subseq['end']))
            y = 75 + 5 *chlvl
            x = (WIDTH - text_length*8)/WIDTH * 100
        html += f"<text class='numbering' id='numbering_{subseq['id']}' font-size='10'  "
        html += f" y='{y}%' x='{x}%' >{subseq['end']}</text>\n"

    html += "</svg>"

    return mark_safe(html)
