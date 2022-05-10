from copy import deepcopy
from logika.igralec import Igralec

GLOBINA_MINIMAKS = 5

def hevristika (igra, igralec):
    if igralec == Igralec.B:
        return igra.polje.preostalih_B - igra.polje.preostalih_A
    else:
        return igra.polje.preostalih_A - igra.polje.preostalih_B


def minimax(globina, max_igralec, igra, igralec):
    if globina <= 0 or igra.zmagovalec():
        return hevristika(igra, igralec), igra
    
    if max_igralec:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(igralec, igra):
            evaluation = minimax(globina-1, False, move, igralec)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(igralec.nasprotnik(), igra):
            evaluation = minimax(globina-1, True, move, igralec)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        return minEval, best_move


def simulate_move(premik, igra):
    igra.izberi(premik[0], premik[1])
    return igra


def get_all_moves(igralec, igra):
    moves = []
    mozni_premiki = igra.polje.veljavne_poteze_igralca(igralec)

    for (vrsta_figure, stolpec_figure), premiki in mozni_premiki.items():
        for premik in premiki:
            zacasna_igra = deepcopy(igra)
            zacasna_igra.izberi(vrsta_figure, stolpec_figure)
            zacasna_figura = zacasna_igra.izbrana_figura
            if zacasna_figura:
                nova_igra = simulate_move(premik, zacasna_igra)
                # print(nova_igra)
                # print(igralec)
                if nova_igra.na_vrsti == igralec:
                    poteze = get_all_moves(igralec, nova_igra)
                    moves.extend(poteze)
                else:
                    moves.append(nova_igra)
    return moves