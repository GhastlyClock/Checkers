# from gui.okno import Okno, VELIKOST_KVADRATOV
from gui.okno import Okno
from logika.igra import Igra
from logika.vrstaIgralca import VrstaIgralca

def main():
    Okno(VrstaIgralca.clovek, VrstaIgralca.racunalnik)

if __name__ == "__main__":
    main()