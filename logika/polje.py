from logika.figura import Figura
from logika.igralec import Igralec
from math import copysign

ST_VRST, ST_STOLPCEV = 8, 8


class Polje:
    def __init__(self):
        self.preostalih_A = self.preostalih_B = 12
        self.polje = []

        # Naselji polje z igralci:
        for row in range(ST_VRST):
            self.polje.append([])
            for col in range(ST_STOLPCEV):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.polje[row].append(Figura(row, col, Igralec.B))
                    elif row > 4:
                        self.polje[row].append(Figura(row, col, Igralec.A))
                    else:
                        self.polje[row].append(None)
                else:
                    self.polje[row].append(None)
    
    def vse_igralceve_figure(self, igralec):
        figure = []
        for vrstica in self.polje:
            for figura in vrstica:
                if not (figura is None) and figura.igralec == igralec:
                    figure.append(figura)
        return figure
    
    def premik(self, figura, vrsta, stolpec):
        trenutna_vrsta = figura.vrsta
        trenutni_stolpec = figura.stolpec

        # Spremeni položaj figure:
        self.polje[trenutna_vrsta][trenutni_stolpec], self.polje[vrsta][stolpec] = None, figura
        figura.premik(vrsta, stolpec, ST_VRST)

        # Odstranimo vse vmesne figure:
        premik_stolpec = int(copysign(1,stolpec-trenutni_stolpec))
        premik_vrsta = int(copysign(1, vrsta-trenutna_vrsta))
        vrste_za_odbris = list(range(trenutna_vrsta+premik_vrsta, vrsta, premik_vrsta))
        stolpci_za_odbris = list(range(trenutni_stolpec+premik_stolpec, stolpec, premik_stolpec))
        for i, j in zip(vrste_za_odbris, stolpci_za_odbris):
            self.odstrani(i,j)
        return (max(abs(trenutna_vrsta - vrsta), abs(trenutni_stolpec - stolpec)) > 1)

    def odstrani(self, vrsta, stolpec):
        figura = self.polje[vrsta][stolpec]
        if not figura:
            return
        if figura.igralec == Igralec.A:
            self.preostalih_A -= 1
        else:
            self.preostalih_B -= 1
        del figura
        self.polje[vrsta][stolpec] = None
        

    def dobi_figuro(self, vrsta, stolpec):
        return self.polje[vrsta][stolpec]

    
    def veljavne_poteze_igralca(self, igralec):
        figure = self.vse_igralceve_figure(igralec)
        poteze = {}
        pomozna_zastava = False
        for figura in figure:
            premiki, zastava = self.dobi_veljavne_poteze(figura)
            if premiki:
                poteze[(figura.vrsta, figura.stolpec)] = (premiki, zastava)
            if zastava:
                pomozna_zastava = True
        rezultat = {}

        for (key, value) in poteze.items():
            if not(pomozna_zastava) or (pomozna_zastava == value[1]):
                rezultat[key] = value[0]
                
        return rezultat

    def dobi_veljavne_poteze(self, figura):
        '''
        Input:
            Figura za katero želimo izraziti vse veljavne poteze
        Output:
            Vse veljavne poteze figure
        '''
        veljavne_poteze, zastava = self._veljavni_premiki(figura.vrsta, figura.stolpec, figura.igralec)
        VP = []

        if figura.igralec == Igralec.A or figura.kralj:
            # Veljavni so premiki navzgor (tj. smer = -1)
            VP += veljavne_poteze.get((-1,1),[]) + veljavne_poteze.get((-1,-1),[])
        if figura.igralec == Igralec.B or figura.kralj:
            # Veljavni so premiki navzdol (tj. smer = 1)
            VP += veljavne_poteze.get((1,1),[]) + veljavne_poteze.get((1,-1),[])
        return (VP, zastava)
    
    def _veljavni_premiki(self, vrsta, stolpec, igralec):
        '''
        Input:
            vrsta ... vrsta v kateri se nahaja figura
            stolpec ... stolpec v katerem se nahaja figura
            smer ... -1 ali 1 odvisno od premika navzdol ali navzgor
        Output:
            Vsa veljavna polja do katerih lahko pridemo iz tega mesta
        '''
        vsi_veljavni_premiki = {}

        def v_polju(v, s):
            return (v >= 0 and v < ST_VRST) and (s >= 0 and s < ST_STOLPCEV)

        zastava = False

        for smer_vrsta in [1, -1]:
            for smer_stolpec in [1, -1]:
                nova_vrsta = vrsta + smer_vrsta
                nov_stolpec = stolpec + smer_stolpec
                if v_polju(nova_vrsta, nov_stolpec):
                    figura = self.polje[nova_vrsta][nov_stolpec]
                    if not (figura):
                        vsi_veljavni_premiki[(smer_vrsta, smer_stolpec)] = ((nova_vrsta, nov_stolpec), False)
                    elif figura.igralec == igralec.nasprotnik():
                        nova_vrsta += smer_vrsta
                        nov_stolpec += smer_stolpec
                        if v_polju(nova_vrsta, nov_stolpec) and (self.polje[nova_vrsta][nov_stolpec] is None):
                            zastava = True
                            vsi_veljavni_premiki[(smer_vrsta, smer_stolpec)] = ((nova_vrsta, nov_stolpec), True)

        rezultat = {}

        for (key, value) in vsi_veljavni_premiki.items():
            if not(zastava) or (zastava == value[1]):
                rezultat[key] = [value[0]]

        return (rezultat, zastava)