from copy import deepcopy
from logika.igralec import Igralec

def hevristika (igra):
    return igra.polje.preostalih_B - igra.polje.preostalih_A


def alphabeta(globina, alpha, beta, max_igralec, igra):
    if globina <= 0 or igra.zmagovalec():
        return hevristika(igra), igra
    
    if max_igralec:
        value = float('-inf')
        best_move = None
        neki = get_all_moves(Igralec.B, igra)
        if not neki:
            print(1)
        for move in neki:
            evaluation = alphabeta(globina-1, alpha, beta, False, move)[0]
            value = max(evaluation, value)
            alpha = max(alpha, value)
            if beta <= value:
                break
            if value == evaluation:
                best_move = move
        if best_move is None:
            best_move = neki[-1]
        return value, best_move
    else:
        value = float('inf')
        best_move = None
        neki = get_all_moves(Igralec.A, igra)
        if not neki:
            print(1)
        for move in neki:
            evaluation = alphabeta(globina-1, alpha, beta, True, move)[0]
            value = min(evaluation, value)
            beta = min(beta, value)
            if alpha >= value:
                break
            if value == evaluation:
                best_move = move
        if best_move is None:
            best_move = neki[-1]
        return value, best_move


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
                moves.append(nova_igra)
    
    return moves