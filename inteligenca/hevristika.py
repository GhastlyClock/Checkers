from logika.igralec import Igralec
from logika.polje import ST_VRST

ZMAGA = float('inf')
PORAZ = float('-inf')


def hevristika (igra, igralec):
    zmagovalec = igra.zmagovalec()
    if zmagovalec:
        if zmagovalec == igralec:
            return 20
        else:
            return -20
    if igralec == Igralec.B:
        return igra.polje.preostalih_B - igra.polje.preostalih_A
    else:
        return igra.polje.preostalih_A - igra.polje.preostalih_B


def hevristika1 (igra, igralec):
    zmagovalec = igra.zmagovalec()
    if zmagovalec:
        if zmagovalec == igralec:
            return 1000000000
        else:
            return -1000000000
    stevilo_kraljev_A, stevilo_kraljev_B, stevilo_figur_zadnja_vrsta_A, stevilo_figur_zadnja_vrsta_B, stevilo_figur_sredina_A, stevilo_figur_sredina_B = preberi_podatke(igra)
    if igralec == Igralec.B:
        return 17 * (igra.polje.preostalih_B - igra.polje.preostalih_A) + 13 * igra.polje.preostalih_B + 6 * (stevilo_kraljev_B - stevilo_kraljev_A) + 3 * stevilo_figur_zadnja_vrsta_B + 1 * stevilo_figur_sredina_B
    else:
        return 17 * (igra.polje.preostalih_A - igra.polje.preostalih_B) + 13 * igra.polje.preostalih_A + 6 * (stevilo_kraljev_A - stevilo_kraljev_B) + 3 * stevilo_figur_zadnja_vrsta_A + 1 * stevilo_figur_sredina_A


def preberi_podatke(igra):
    stevilo_kraljev_A = 0
    stevilo_kraljev_B = 0

    stevilo_figur_zadnja_vrsta_A = 0
    stevilo_figur_zadnja_vrsta_B = 0
    
    stevilo_figur_sredina_A = 0
    stevilo_figur_sredina_B = 0
    for i, vrsta in enumerate(igra.polje.polje):
        for j, figura in enumerate(vrsta):
            if figura:
                if figura.igralec == Igralec.B:
                    if i == 0:
                        stevilo_figur_zadnja_vrsta_B += 1
                    if i == 3 or i == 4 or j in [2,3,4,5]:
                        stevilo_figur_sredina_B += 1
                    if figura.kralj:
                        stevilo_kraljev_B += 1
                elif figura.igralec == Igralec.A:
                    if i == ST_VRST-1:
                        stevilo_figur_zadnja_vrsta_A += 1
                    if i == 3 or i == 4 or j in [2,3,4,5]:
                        stevilo_figur_sredina_A += 1
                    if figura.kralj:
                        stevilo_kraljev_A += 1

    return stevilo_kraljev_A, stevilo_kraljev_B, stevilo_figur_zadnja_vrsta_A, stevilo_figur_zadnja_vrsta_B, stevilo_figur_sredina_A, stevilo_figur_sredina_B


