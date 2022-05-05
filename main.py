# from gui.okno import Okno, VELIKOST_KVADRATOV
from gui.okno import Okno
from logika.igra import Igra

def main():
    igra = Igra()
    Okno(igra)

if __name__ == "__main__":
    main()