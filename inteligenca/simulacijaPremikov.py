from copy import deepcopy

def simuliraj_premik(premik, igra):
    igra.izberi(premik[0], premik[1])
    return igra


def generiraj_vse_premike(igra):
    vsi_premiki = []
    mozni_premiki = igra.polje.veljavne_poteze_igralca(igra.na_vrsti)

    for (vrsta_figure, stolpec_figure), premiki in mozni_premiki.items():
        for premik in premiki:
            zacasna_igra = deepcopy(igra)
            zacasna_igra.izberi(vrsta_figure, stolpec_figure)
            zacasna_figura = zacasna_igra.izbrana_figura
            if zacasna_figura:
                nova_igra = simuliraj_premik(premik, zacasna_igra)
                if nova_igra.na_vrsti == igra.na_vrsti:
                    poteze = generiraj_vse_premike(nova_igra)
                    vsi_premiki.extend(poteze)
                else:
                    vsi_premiki.append(nova_igra)
    return vsi_premiki