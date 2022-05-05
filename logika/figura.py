class Figura:
    def __init__(self, vrsta, stolpec, igralec):
        self.vrsta = vrsta
        self.stolpec = stolpec
        self.igralec = igralec
        self.kralj = False
    
    def postani_kralj(self):
        self.kralj = True
    
    def premik(self, vrsta, stolpec, ST_VRST):
        self.vrsta = vrsta
        self.stolpec = stolpec
        # Če smo se premaknili v zadnjo vrsto postanemo kralj
        if vrsta == ST_VRST-1 or vrsta == 0:
            self.postani_kralj()