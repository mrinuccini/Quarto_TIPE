##Instanciation de la pièce de jeu
class Piece:
    "Instanciation d'une pièce de jeu"
    def __init__(self, couleur: int, forme: int, dessus: int, taille:int) -> None:
        """Paramètres :
                couleur : 0 ou 1, couleur de la pièce (0=blanc, 1=noir)
                forme : 0 ou 1, forme de la pièce (0=carré, 1=rond)
                dessus : 0 ou 1, dessus de la pièce (0=lisse, 1=creusé)
                taille : 0 ou 1, taille de la pièce (0=petite, 1=grande)
        """
        assert(couleur in (0,1))
        assert(forme in (0,1))
        assert(dessus in (0,1))
        assert(taille in (0,1))
        self.couleur = couleur
        self.forme = forme
        self.dessus = dessus
        self.taille = taille

    def __repr__(self):
        "Affichage de la pièce et de ses caractéristiques"
        str = ""

        if self.couleur == 0:
                str += "⬜" if self.forme == 0 else "⚪"
        else:
              str += "⬛" if self.forme == 0 else "⚫"  

        if self.dessus == 0:
                str += " (#)" if self.taille == 0 else " (###)"
        else:
                str += " (@)" if self.taille == 0 else " (@@@)"

        """
        str = "pièce"
        str += " blanche" if self.couleur == 0 else " noire"
        str += " carrée" if self.forme == 0 else " ronde"
        str += " lisse" if self.dessus == 0 else " creusée"
        str += " petite" if self.taille == 0 else " grande"
        """

        return str


##Fonctions sur les pièces
def comp(L):
    """ Compare une liste de pièces, renvoie True si toutes les pièces ont 
    au moins une caractéristique en commun
    Paramètres :
        L : liste de piece, non vide
    Sortie :
        booléen
    """
    assert(L!=[])
    assert(type(L)==list)

    if None in L:
         return False
    
    if all(p.couleur == L[0].couleur for p in L[1:]):
            return True
    if all(p.forme == L[0].forme for p in L[1:]):
            return True
    if all(p.dessus == L[0].dessus for p in L[1:]):
            return True
    if all(p.taille == L[0].taille for p in L[1:]):
            return True
    
    return False