from logika.igralec import Igralec
ZMAGA = float('inf')
PORAZ = float('-inf')


def hevristika (igra):
    zmagovalec = igra.zmagovalec()
    if zmagovalec:
        if zmagovalec == igra.na_vrsti:
            return ZMAGA
        else:
            return PORAZ
    if igra.na_vrsti == Igralec.B:
        return igra.polje.preostalih_B - igra.polje.preostalih_A
    else:
        return igra.polje.preostalih_A - igra.polje.preostalih_B