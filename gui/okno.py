from logika.polje import ST_STOLPCEV, ST_VRST
from logika.igralec import Igralec
import pygame
from inteligenca.minimax import *

SIRINA, VISINA = 800, 800
VELIKOST_KVADRATOV = SIRINA//ST_STOLPCEV
NOTRANJOST_FIGUR = 12
OBROBA_FIGUR = 5

# rgb
RDECA = (255, 0, 0)
BELA = (255, 255, 255)
CRNA = (0, 0, 0)
MODRA = (0, 0, 255)
SIVA = (128,128,128)
ZELENA = (0, 255, 0)

KRONA = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))

FPS = 60

GLOBINA_MINIMAKS = 5

def dobi_vrsto_stolpec_iz_miske(pos):
    x, y = pos
    row = y // VELIKOST_KVADRATOV
    col = x // VELIKOST_KVADRATOV
    return row, col

def izracunaj_polozaj_figure(figura):
    x = VELIKOST_KVADRATOV * figura.stolpec + VELIKOST_KVADRATOV // 2
    y = VELIKOST_KVADRATOV * figura.vrsta + VELIKOST_KVADRATOV // 2
    return (x, y)

class Okno:
    def __init__(self, igra):
        self.okno = pygame.display.set_mode((SIRINA, VISINA))
        pygame.display.set_caption('Checkers')
        self.igra = igra
        self._zazeni()

    def _zazeni(self):
        run = True
        clock = pygame.time.Clock()
        self.posodobi()
        
        while run:
            clock.tick(FPS)
            
            if self.igra.na_vrsti == Igralec.B:
                _, koncna_igra = minimax(GLOBINA_MINIMAKS, True, self.igra)
                self.igra = koncna_igra


            if self.igra.zmagovalec():
                print(f"Zmagal je igralec {self.igra.zmagovalec()}!")
                run = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    vrsta, stolpec = dobi_vrsto_stolpec_iz_miske(pos)
                    self.igra.izberi(vrsta, stolpec)
            self.posodobi()
        pygame.quit()

    def narisi_veljavne_poteze(self, poteze):
        for poteza in poteze:
            vrsta, stolpec = poteza
            pygame.draw.circle(self.okno, MODRA, (stolpec * VELIKOST_KVADRATOV + VELIKOST_KVADRATOV//2, vrsta * VELIKOST_KVADRATOV + VELIKOST_KVADRATOV//2), 15)

    

    def posodobi(self):
        # Nariši igralno polje:
        self.okno.fill(CRNA)
        
        for row in range(ST_VRST):
            for col in range(row % 2, ST_STOLPCEV, 2):
                pygame.draw.rect(self.okno, SIVA, (row*VELIKOST_KVADRATOV, col *VELIKOST_KVADRATOV, VELIKOST_KVADRATOV, VELIKOST_KVADRATOV))
        
        for row in range(ST_VRST):
            for col in range(ST_STOLPCEV):
                figura = self.igra.polje.dobi_figuro(row, col)
                if figura:
                    # Nariši figuro
                    radius = VELIKOST_KVADRATOV//2 - NOTRANJOST_FIGUR
                    BARVA = SIVA
                    # print(self.izbrana_figura)
                    if self.igra.izbrana_figura and figura.vrsta == self.igra.izbrana_figura.vrsta and figura.stolpec == self.igra.izbrana_figura.stolpec:
                        # Spremenim barvo da se ve kdo je izbran
                        BARVA = MODRA
                    elif figura.igralec == self.igra.na_vrsti and (figura.vrsta, figura.stolpec) in self.igra.vse_veljavne_poteze.keys():
                        # Spremenim barvo da se ve kdo je na vrsti
                        BARVA = ZELENA
                    figura_x, figura_y = izracunaj_polozaj_figure(figura)
                    pygame.draw.circle(self.okno, BARVA, (figura_x, figura_y), radius + OBROBA_FIGUR)
                    if figura.igralec == Igralec.A:
                        barva = RDECA
                    else:
                        barva = BELA
                    pygame.draw.circle(self.okno, barva, (figura_x, figura_y), radius)

                    # Narišemo še krono
                    if figura.kralj:
                        self.okno.blit(KRONA, (figura_x - KRONA.get_width()//2, figura_y - KRONA.get_height()//2))

        # Če imamo izbrano polje narišemo še veljavne poteze
        self.narisi_veljavne_poteze(self.igra.poteze_izbrane_figure)

        # Posodobimo prikazno okno
        pygame.display.update()
