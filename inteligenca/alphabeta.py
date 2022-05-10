from copy import deepcopy
from inteligenca.simulacijaPremikov import *
from inteligenca.hevristika import *


def alphabeta(globina, alpha, beta, max_igralec, igra, igralec):
    if globina <= 0 or igra.zmagovalec():
        return hevristika(igra, igralec), igra
    
    if max_igralec:
        maxEval = PORAZ
        najboljse_stanje = None
        vsi_premiki = generiraj_vse_premike(igra)
        for stanje in vsi_premiki:
            evaluation = alphabeta(globina-1, alpha, beta, False, stanje, igralec)[0]
            maxEval = max(evaluation, maxEval)
            if maxEval == evaluation:
                najboljse_stanje = stanje
            if beta <= maxEval:
                break
            alpha = max(alpha, maxEval)
        return maxEval, najboljse_stanje
    else:
        minEval = ZMAGA
        najboljse_stanje = None
        vsi_premiki = generiraj_vse_premike(igra)
        for stanje in vsi_premiki:
            evaluation = alphabeta(globina-1, alpha, beta, True, stanje, igralec)[0]
            minEval = min(evaluation, minEval)
            if minEval == evaluation:
                najboljse_stanje = stanje
            if alpha >= minEval:
                break
            beta = min(beta, minEval)
        return minEval, najboljse_stanje