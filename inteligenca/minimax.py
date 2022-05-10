from inteligenca.simulacijaPremikov import *
from inteligenca.hevristika import *

def minimax(globina, max_igralec, igra, igralec):
    if globina <= 0 or igra.zmagovalec():
        return hevristika(igra, igralec), igra
    
    if max_igralec:
        maxEval = PORAZ
        najboljse_stanje = None
        for stanje in generiraj_vse_premike(igra):
            evaluation = minimax(globina-1, False, stanje, igralec)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                najboljse_stanje = stanje
        return maxEval, najboljse_stanje
    else:
        minEval = ZMAGA
        najslabse_stanje = None
        for stanje in generiraj_vse_premike(igra):
            evaluation = minimax(globina-1, True, stanje, igralec)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                najslabse_stanje = stanje
        return minEval, najslabse_stanje