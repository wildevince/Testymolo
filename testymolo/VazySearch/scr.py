from numpy import linspace
import re

def word_aligner(referenced_word:str, input_kw:str, small_words:bool=False) -> float:
    """ return float in range(0,1) """

    ### scores
    ident:int =2
    indel:int = max(-1, -2) if(small_words) else min(-1, -2)
    subst:int = min(-1, -2) if(small_words) else max(-1, -2)

    ### initialization
    table:list = []
    vectors:list = []
    for y in range(0, len(input_kw)+1):
        table.append([])
        if y > 0 : 
            vectors.append([])
        for x in range(0, len(referenced_word)+1):
            table[y].append(0) 
            if y > 0 and x > 0:
                vectors[y-1].append(0)
    
    ### filling
    for y in range(1, len(input_kw)+1):
        for x in range(1, len(referenced_word)+1):
            if referenced_word[x-1].lower() == input_kw[y-1].lower():
                optimum = table[y-1][x-1] + ident
                table[y][x] = optimum
                vectors[y-1][x-1] = 0
            else:
                costs:tuple = ((table[y-1][x-1] + subst), (table[y-1][x] + indel), (table[y][x-1] + indel))
                optimum:int = max(costs)
                k:int = costs.index(optimum)
                table[y][x] = optimum
                vectors[y-1][x-1] = k
                
    ### solving
    final_column:list = [ row[-1] for row in table[1:] ]
    optimum_final_column:int = max(final_column)
    index_optimum_final_column:tuple = (final_column.index(optimum_final_column)+1, len(referenced_word))
    final_row:list = table[-1][1:]
    optimum_final_row:int = max(final_row)
    index_optimum_final_row:tuple = (len(input_kw), final_row.index(optimum_final_row)+1)
    indexes:list = [index_optimum_final_column, index_optimum_final_row]
    optimi:list = [optimum_final_column, optimum_final_row]
    global_optimum:int = max(optimi)
    global_index:tuple = indexes[optimi.index(global_optimum)]

    ### scoring
    j,i = global_index  # starting point
    score:int = 0
    while j > 0 and i > 0:
        v = vectors[j-1][i-1]
        if v == 0:
            if referenced_word[i-1].lower() == input_kw[j-1].lower():
                score += 1
            j -= 1
            i -= 1
        elif v == 1:
            i -= 1
        elif v == 2:
            j -= 1
        else:
            raise "out of range"

    ### result
    return float(score)/min(len(referenced_word), len(input_kw))


def taxo_aligner(taxonomy_full:str, kw:str) -> float:
    taxo_list:list = [taxo.strip() for taxo in taxonomy_full.split(';')]
    N:int = len(taxo_list)
    score_space:list = linspace(0.1, 0.5, N)
    result:int = sum([ word_aligner(taxo_list[k], kw, True) for k in range(N)])
    return max(result , 1)


def convert_motif_PROSITE_to_regex(motif):
    regex:str = ""
    prosite_length:int = len(motif)

    if motif.startswith('<'):
        regex = '^'+regex
    
    i:int = 0
    starts:dict   = {'(':'{', '[':'[', '{':'[^'}
    ends:dict   = {'{':'}', '[':']', '[^':']'}
    brackets:dict = {'(':')', '[':']', '{':'}'}

    while i < prosite_length:
        c = motif[i]

        if c in '[{(':
            stop:str = brackets[c]
            j:int = motif.index(stop, i, prosite_length)+1
            term:str = motif[i:j].strip(c).strip(stop)
            start:str = starts[c]
            end:str = ends[start]

            if term.endswith('>'):
                term = term[:-1]
                if c == '{':
                    start = '[^'
                    end = ']?$'
                elif c == '[':
                    if len(term) > 1:
                        start = '['
                        end = ']?$'
                    else:
                        start = ''
                        end = '?$'
            elif c == '(' and term == '0,1':
                term = '?'
                start = ''
                end = ''

            regex += start+term+end
            i = j
            
        elif c in "Xx?":
            regex += '.'
            i += 1

        elif c in '*':
            regex += '.*'
            i += 1
        
        elif c in " -|<>":
            i += 1
            pass
        
        else:
            regex += c
            i += 1

    if motif.endswith('>'):
        regex = regex+'$'
    
    if 'or' in regex:
        regex =  '('+')|('.join(regex.split('or'))+')'

    return regex


def search_motif(pattern:str, string:str) -> bool:
    without_convertion: bool = re.match(pattern, string)
    if not without_convertion:
        return re.match(convert_motif_PROSITE_to_regex(pattern), string)
    return without_convertion
