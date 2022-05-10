from logika.figura import Figura
from logika.igralec import Igralec
from math import copysign

ST_VRST, ST_STOLPCEV = 8, 8


class Polje:
    def __init__(self):
        self.preostalih_A = self.preostalih_B = 12
        self.polje = []
        self.stevilo_zaporednih_potez_kralja = 0

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
        if figura.kralj:
            self.stevilo_zaporednih_potez_kralja += 1
        else:
            self.stevilo_zaporednih_potez_kralja = 0
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
            if zastava and premiki:
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
        vsi_veljavni_premiki, zastava_gor, zastava_dol = self._veljavni_premiki(figura)
        
        VP = []

        if figura.igralec == Igralec.A or figura.kralj:
            # Veljavni so premiki navzgor (tj. smer = -1)
            VP += vsi_veljavni_premiki.get((-1,1),[]) + vsi_veljavni_premiki.get((-1,-1),[])
            zastava = zastava_dol
        if figura.igralec == Igralec.B or figura.kralj:
            # Veljavni so premiki navzdol (tj. smer = 1)
            # zastava = zastava_gor if not figura.kralj else zastava_gor or zastava_dol
            zastava = zastava_gor
            VP += vsi_veljavni_premiki.get((1,1),[]) + vsi_veljavni_premiki.get((1,-1),[])
        
        # rezultat = []

        # for (premik, flag) in VP:
        #     if not(zastava) or (zastava == flag):
        #         rezultat.append(premik)

        if figura.kralj:
            zastava = zastava_dol or zastava_gor
        return (VP, zastava)
    
    def _veljavni_premiki(self, figura):
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

        zastava_gor = False
        zastava_dol = False

        for smer_vrsta in [1, -1]:
            for smer_stolpec in [1, -1]:
                nova_vrsta = figura.vrsta + smer_vrsta
                nov_stolpec = figura.stolpec + smer_stolpec
                if v_polju(nova_vrsta, nov_stolpec):
                    polje = self.polje[nova_vrsta][nov_stolpec]
                    if not (polje):
                        vsi_veljavni_premiki[(smer_vrsta, smer_stolpec)] = ((nova_vrsta, nov_stolpec), False)
                    elif polje.igralec == figura.igralec.nasprotnik():
                        nova_vrsta += smer_vrsta
                        nov_stolpec += smer_stolpec
                        if v_polju(nova_vrsta, nov_stolpec) and (self.polje[nova_vrsta][nov_stolpec] is None):
                            if smer_vrsta == 1:
                                zastava_gor = True
                            else:
                                zastava_dol = True
                            vsi_veljavni_premiki[(smer_vrsta, smer_stolpec)] = ((nova_vrsta, nov_stolpec), True)

        rezultat = {}

        for (smer_vrsta, smer_stolpec), ((nova_vrsta, nov_stolpec), zastava) in vsi_veljavni_premiki.items():
            if figura.kralj:
                nova_zastava = zastava_gor or zastava_dol
            else:
                nova_zastava = zastava_gor if smer_vrsta == 1 else zastava_dol
            if not(nova_zastava) or (nova_zastava == zastava):
                rezultat[(smer_vrsta, smer_stolpec)] = [(nova_vrsta, nov_stolpec)]

        return rezultat, zastava_gor, zastava_dol