from logika.igralec import Igralec

ZMAGA = float('inf')
PORAZ = float('-inf')


def hevristika (igra, igralec):
    zmagovalec = igra.zmagovalec()
    if zmagovalec:
        if zmagovalec == igralec:
            return ZMAGA
        else:
            return PORAZ
    if igralec == Igralec.B:
        return igra.polje.preostalih_B - igra.polje.preostalih_A
    else:
        return igra.polje.preostalih_A - igra.polje.preostalih_B