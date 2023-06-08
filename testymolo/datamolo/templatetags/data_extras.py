from django import template
from django.http import JsonResponse
from datamolo.models import Subseq

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



