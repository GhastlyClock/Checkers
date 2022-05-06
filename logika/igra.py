from logika.polje import Polje
from logika.igralec import Igralec


class Igra:
    def __init__(self):
        self._nova_igra()
    
    def _nova_igra(self):
        self.polje = Polje()
        self.na_vrsti = Igralec.A
        self.izbrana_figura = None
        self.poteze_izbrane_figure = []
        self.vse_veljavne_poteze = self.polje.veljavne_poteze_igralca(self.na_vrsti)

    def reset(self):
        self._nova_igra()

    def zmagovalec(self):
        if self.polje.preostalih_A <= 0:
            return Igralec.B
        elif self.polje.preostalih_B <= 0:
            return Igralec.A
        elif not(self.vse_veljavne_poteze):
            return self.na_vrsti.nasprotnik()
        return None

    def _odstrani_izbiro(self):
        self.izbrana_figura = None
        self.poteze_izbrane_figure = []

    def izberi(self, vrsta, stolpec):
        # Dobimo figuro, ki se nahaja na tem mestu
        figura = self.polje.dobi_figuro(vrsta, stolpec)

        if self.izbrana_figura and (vrsta, stolpec) in self.poteze_izbrane_figure:
            # Če je trenutno izbrano polje ni prazno in je v veljavnih potezah, naredi premik
            if self.polje.premik(self.izbrana_figura, vrsta, stolpec) and self.dobi_dodatne_poteze_figure(self.izbrana_figura):
                self.poteze_izbrane_figure = self.vse_veljavne_poteze.get((vrsta, stolpec), [])
            else:
                self.spremeni_igralca()
        elif figura and figura.igralec == self.na_vrsti and (figura.vrsta, figura.stolpec) in self.vse_veljavne_poteze.keys():
            self.izbrana_figura = figura
            self.poteze_izbrane_figure = self.vse_veljavne_poteze.get((vrsta, stolpec), [])
        else:
            self._odstrani_izbiro()
            return False
        return True

    def dobi_dodatne_poteze_figure(self, figura):
        poteze, zastava = self.polje.dobi_veljavne_poteze(figura)
        if zastava:
            self.vse_veljavne_poteze = {(figura.vrsta, figura.stolpec) : poteze}
            return True
        return False

    def spremeni_igralca(self):
        self._odstrani_izbiro()
        self.na_vrsti = self.na_vrsti.nasprotnik()
        self.vse_veljavne_poteze = self.polje.veljavne_poteze_igralca(self.na_vrsti)