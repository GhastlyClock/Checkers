# from gui.okno import Okno, VELIKOST_KVADRATOV
from gui.okno import Okno
from logika.vrstaIgralca import VrstaIgralca

def main():
    Okno(VrstaIgralca.racunalnik, VrstaIgralca.racunalnik)

if __name__ == "__main__":
    main()