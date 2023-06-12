from django import template
from django.http import JsonResponse

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


chnext:bool = False
chlvl:int = 0
width_min = 350


@register.filter(is_safe=True)
def generate_svg(data:dict):
    L = data["protein"]["length"]

    def each(subseq):
        html = ""
        html += f"<rect class='subseq' id={subseq['id']} height='20%' y='40%' fill='blue' fill-opacity='0.2' "
        w = subseq['length']/ L *100
        x = subseq['end']/L*100
        html += f"x='{x}%' width='{w}%'"

