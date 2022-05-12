from inteligenca.simulacijaPremikov import *
from inteligenca.hevristika import *
import random

def alphabeta(globina, alpha, beta, max_igralec, igra, igralec):
    if globina <= 0 or igra.zmagovalec():
        return hevristika1(igra, igralec), igra
        # if igralec == Igralec.B:
        #     return hevristika(igra, igralec), igra
        # else:
        #     return hevristika1(igra, igralec), igra
    
    if max_igralec:
        maxEval = PORAZ
        najboljse_stanje = None
        vsi_premiki = generiraj_vse_premike(igra)
        for stanje in vsi_premiki:
            evaluation = alphabeta(globina-1, alpha, beta, False, stanje, igralec)[0]
            if evaluation == maxEval and random.getrandbits(1):
                najboljse_stanje = stanje
            elif evaluation > maxEval:
                maxEval = evaluation
                najboljse_stanje = stanje
            if beta <= maxEval: # To poglej zakaj ne dela prou brez najboljse_stanje
                break
            alpha = max(alpha, maxEval)
        return maxEval, najboljse_stanje
    else:
        minEval = ZMAGA
        najboljse_stanje = None
        vsi_premiki = generiraj_vse_premike(igra)
        for stanje in vsi_premiki:
            evaluation = alphabeta(globina-1, alpha, beta, True, stanje, igralec)[0]
            if evaluation == minEval and random.getrandbits(1):
                najboljse_stanje = stanje
            elif evaluation < minEval:
                minEval = evaluation
                najboljse_stanje = stanje
            if alpha >= minEval: # To poglej zakaj ne dela prou brez najboljse_stanje
                break
            beta = min(beta, minEval)
        return minEval, najboljse_stanje
