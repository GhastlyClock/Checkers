from logika.igralec import Igralec
from inteligenca.simulacijaPremikov import *
from inteligenca.hevristika import *

GLOBINA_MINIMAKS = 5

ZMAGA = float('inf')
PORAZ = float('-inf')

def hevristika (igra, igralec):
    if igralec == Igralec.B:
        return igra.polje.preostalih_B - igra.polje.preostalih_A
    else:
        return igra.polje.preostalih_A - igra.polje.preostalih_B


def minimax(globina, max_igralec, igra):
    zmagovalec = igra.zmagovalec()
    if zmagovalec:
        if zmagovalec == igra.na_vrsti:
            return ZMAGA, igra
        else:
            return PORAZ, igra
    if globina <= 0:
        return hevristika(igra, igra.na_vrsti), igra
    
    if max_igralec:
        maxEval = PORAZ
        best_move = None
        for move in generiraj_vse_premike(igra):
            evaluation = minimax(globina-1, False, move)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        return maxEval, best_move
    else:
        minEval = ZMAGA
        best_move = None
        for move in generiraj_vse_premike(igra):
            evaluation = minimax(globina-1, True, move)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        return minEval, best_move