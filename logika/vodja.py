from logika.igralec import Igralec
from logika.vrstaIgralca import VrstaIgralca
from inteligenca.minimax import *
from inteligenca.alphabeta import *
from logika.igra import Igra

GLOBINA_MINIMAKS = 4

class Vodja:
    def __init__(self, okno):
        self.okno = okno
        self._nova_igra()

    def _nova_igra(self):
        self.igra = Igra()
        self.igralecA = self.okno.vrstaIgralcaA
        self.igralecB = self.okno.vrstaIgralcaB

    def racunalnikovaPoteza(self):
        _, koncna_igra = alphabeta(GLOBINA_MINIMAKS, float('-inf'), float('inf'), True, self.igra, self.igra.na_vrsti)
        self.igra = koncna_igra

    def clovekovaPoteza(self, poteza):
        self.igra.izberi(poteza[0], poteza[1])

    def igramo(self, poteza=None):
        if (self.igra.na_vrsti == Igralec.A and self.igralecA == VrstaIgralca.racunalnik) or (self.igra.na_vrsti == Igralec.B and self.igralecB == VrstaIgralca.racunalnik):
            self.racunalnikovaPoteza()
        elif poteza:
            self.clovekovaPoteza(poteza)
        return True